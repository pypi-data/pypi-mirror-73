#!/usr/bin/env python

import itertools
import os.path
import pathlib
import re
import sys
import textwrap
from typing import List, Union

import betterproto
from betterproto.compile.importing import get_type_reference
from betterproto.compile.naming import (
    pythonize_class_name,
    pythonize_field_name,
    pythonize_method_name,
)

try:
    # betterproto[compiler] specific dependencies
    import black
    from google.protobuf.compiler import plugin_pb2 as plugin
    from google.protobuf.descriptor_pb2 import (
        DescriptorProto,
        EnumDescriptorProto,
        FieldDescriptorProto,
    )
    import google.protobuf.wrappers_pb2 as google_wrappers
    import jinja2
except ImportError as err:
    missing_import = err.args[0][17:-1]
    print(
        "\033[31m"
        f"Unable to import `{missing_import}` from betterproto plugin! "
        "Please ensure that you've installed betterproto as "
        '`pip install "betterproto[compiler]"` so that compiler dependencies '
        "are included."
        "\033[0m"
    )
    raise SystemExit(1)


def py_type(package: str, imports: set, field: FieldDescriptorProto) -> str:
    if field.type in [1, 2]:
        return "float"
    elif field.type in [3, 4, 5, 6, 7, 13, 15, 16, 17, 18]:
        return "int"
    elif field.type == 8:
        return "bool"
    elif field.type == 9:
        return "str"
    elif field.type in [11, 14]:
        # Type referencing another defined Message or a named enum
        return get_type_reference(package, imports, field.type_name)
    elif field.type == 12:
        return "bytes"
    else:
        raise NotImplementedError(f"Unknown type {field.type}")


def get_py_zero(type_num: int) -> Union[str, float]:
    zero: Union[str, float] = 0
    if type_num in []:
        zero = 0.0
    elif type_num == 8:
        zero = "False"
    elif type_num == 9:
        zero = '""'
    elif type_num == 11:
        zero = "None"
    elif type_num == 12:
        zero = 'b""'

    return zero


def traverse(proto_file):
    def _traverse(path, items, prefix=""):
        for i, item in enumerate(items):
            # Adjust the name since we flatten the heirarchy.
            item.name = next_prefix = prefix + item.name
            yield item, path + [i]

            if isinstance(item, DescriptorProto):
                for enum in item.enum_type:
                    enum.name = next_prefix + enum.name
                    yield enum, path + [i, 4]

                if item.nested_type:
                    for n, p in _traverse(path + [i, 3], item.nested_type, next_prefix):
                        yield n, p

    return itertools.chain(
        _traverse([5], proto_file.enum_type), _traverse([4], proto_file.message_type)
    )


def get_comment(proto_file, path: List[int], indent: int = 4) -> str:
    pad = " " * indent
    for sci in proto_file.source_code_info.location:
        # print(list(sci.path), path, file=sys.stderr)
        if list(sci.path) == path and sci.leading_comments:
            lines = textwrap.wrap(
                sci.leading_comments.strip().replace("\n", ""), width=79 - indent
            )

            if path[-2] == 2 and path[-4] != 6:
                # This is a field
                return f"{pad}# " + f"\n{pad}# ".join(lines)
            else:
                # This is a message, enum, service, or method
                if len(lines) == 1 and len(lines[0]) < 79 - indent - 6:
                    lines[0] = lines[0].strip('"')
                    return f'{pad}"""{lines[0]}"""'
                else:
                    joined = f"\n{pad}".join(lines)
                    return f'{pad}"""\n{pad}{joined}\n{pad}"""'

    return ""


def generate_code(request, response):
    plugin_options = request.parameter.split(",") if request.parameter else []

    env = jinja2.Environment(
        trim_blocks=True,
        lstrip_blocks=True,
        loader=jinja2.FileSystemLoader("%s/templates/" % os.path.dirname(__file__)),
    )
    template = env.get_template("template.py.j2")

    output_map = {}
    for proto_file in request.proto_file:
        if (
            proto_file.package == "google.protobuf"
            and "INCLUDE_GOOGLE" not in plugin_options
        ):
            continue

        output_file = str(pathlib.Path(*proto_file.package.split("."), "__init__.py"))

        if output_file not in output_map:
            output_map[output_file] = {"package": proto_file.package, "files": []}
        output_map[output_file]["files"].append(proto_file)

    # TODO: Figure out how to handle gRPC request/response messages and add
    # processing below for Service.

    for filename, options in output_map.items():
        package = options["package"]
        # print(package, filename, file=sys.stderr)
        output = {
            "package": package,
            "files": [f.name for f in options["files"]],
            "imports": set(),
            "datetime_imports": set(),
            "typing_imports": set(),
            "messages": [],
            "enums": [],
            "services": [],
        }

        for proto_file in options["files"]:
            item: DescriptorProto
            for item, path in traverse(proto_file):
                data = {"name": item.name, "py_name": pythonize_class_name(item.name)}

                if isinstance(item, DescriptorProto):
                    # print(item, file=sys.stderr)
                    if item.options.map_entry:
                        # Skip generated map entry messages since we just use dicts
                        continue

                    data.update(
                        {
                            "type": "Message",
                            "comment": get_comment(proto_file, path),
                            "properties": [],
                        }
                    )

                    for i, f in enumerate(item.field):
                        t = py_type(package, output["imports"], f)
                        zero = get_py_zero(f.type)

                        repeated = False
                        packed = False

                        field_type = f.Type.Name(f.type).lower()[5:]

                        field_wraps = ""
                        match_wrapper = re.match(
                            r"\.google\.protobuf\.(.+)Value", f.type_name
                        )
                        if match_wrapper:
                            wrapped_type = "TYPE_" + match_wrapper.group(1).upper()
                            if hasattr(betterproto, wrapped_type):
                                field_wraps = f"betterproto.{wrapped_type}"

                        map_types = None
                        if f.type == 11:
                            # This might be a map...
                            message_type = f.type_name.split(".").pop().lower()
                            # message_type = py_type(package)
                            map_entry = f"{f.name.replace('_', '').lower()}entry"

                            if message_type == map_entry:
                                for nested in item.nested_type:
                                    if (
                                        nested.name.replace("_", "").lower()
                                        == map_entry
                                    ):
                                        if nested.options.map_entry:
                                            # print("Found a map!", file=sys.stderr)
                                            k = py_type(
                                                package,
                                                output["imports"],
                                                nested.field[0],
                                            )
                                            v = py_type(
                                                package,
                                                output["imports"],
                                                nested.field[1],
                                            )
                                            t = f"Dict[{k}, {v}]"
                                            field_type = "map"
                                            map_types = (
                                                f.Type.Name(nested.field[0].type),
                                                f.Type.Name(nested.field[1].type),
                                            )
                                            output["typing_imports"].add("Dict")

                        if f.label == 3 and field_type != "map":
                            # Repeated field
                            repeated = True
                            t = f"List[{t}]"
                            zero = "[]"
                            output["typing_imports"].add("List")

                            if f.type in [1, 2, 3, 4, 5, 6, 7, 8, 13, 15, 16, 17, 18]:
                                packed = True

                        one_of = ""
                        if f.HasField("oneof_index"):
                            one_of = item.oneof_decl[f.oneof_index].name

                        if "Optional[" in t:
                            output["typing_imports"].add("Optional")

                        if "timedelta" in t:
                            output["datetime_imports"].add("timedelta")
                        elif "datetime" in t:
                            output["datetime_imports"].add("datetime")

                        data["properties"].append(
                            {
                                "name": f.name,
                                "py_name": pythonize_field_name(f.name),
                                "number": f.number,
                                "comment": get_comment(proto_file, path + [2, i]),
                                "proto_type": int(f.type),
                                "field_type": field_type,
                                "field_wraps": field_wraps,
                                "map_types": map_types,
                                "type": t,
                                "zero": zero,
                                "repeated": repeated,
                                "packed": packed,
                                "one_of": one_of,
                            }
                        )
                        # print(f, file=sys.stderr)

                    output["messages"].append(data)
                elif isinstance(item, EnumDescriptorProto):
                    # print(item.name, path, file=sys.stderr)
                    data.update(
                        {
                            "type": "Enum",
                            "comment": get_comment(proto_file, path),
                            "entries": [
                                {
                                    "name": v.name,
                                    "value": v.number,
                                    "comment": get_comment(proto_file, path + [2, i]),
                                }
                                for i, v in enumerate(item.value)
                            ],
                        }
                    )

                    output["enums"].append(data)

            for i, service in enumerate(proto_file.service):
                # print(service, file=sys.stderr)

                data = {
                    "name": service.name,
                    "py_name": pythonize_class_name(service.name),
                    "comment": get_comment(proto_file, [6, i]),
                    "methods": [],
                }

                for j, method in enumerate(service.method):
                    input_message = None
                    input_type = get_type_reference(
                        package, output["imports"], method.input_type
                    ).strip('"')
                    for msg in output["messages"]:
                        if msg["name"] == input_type:
                            input_message = msg
                            for field in msg["properties"]:
                                if field["zero"] == "None":
                                    output["typing_imports"].add("Optional")
                            break

                    data["methods"].append(
                        {
                            "name": method.name,
                            "py_name": pythonize_method_name(method.name),
                            "comment": get_comment(proto_file, [6, i, 2, j], indent=8),
                            "route": f"/{package}.{service.name}/{method.name}",
                            "input": get_type_reference(
                                package, output["imports"], method.input_type
                            ).strip('"'),
                            "input_message": input_message,
                            "output": get_type_reference(
                                package,
                                output["imports"],
                                method.output_type,
                                unwrap=False,
                            ).strip('"'),
                            "client_streaming": method.client_streaming,
                            "server_streaming": method.server_streaming,
                        }
                    )

                    if method.client_streaming:
                        output["typing_imports"].add("AsyncIterable")
                        output["typing_imports"].add("Iterable")
                        output["typing_imports"].add("Union")
                    if method.server_streaming:
                        output["typing_imports"].add("AsyncIterator")

                output["services"].append(data)

        output["imports"] = sorted(output["imports"])
        output["datetime_imports"] = sorted(output["datetime_imports"])
        output["typing_imports"] = sorted(output["typing_imports"])

        # Fill response
        f = response.file.add()
        f.name = filename

        # Render and then format the output file.
        f.content = black.format_str(
            template.render(description=output),
            mode=black.FileMode(target_versions=set([black.TargetVersion.PY37])),
        )

    # Make each output directory a package with __init__ file
    output_paths = set(pathlib.Path(path) for path in output_map.keys())
    init_files = (
        set(
            directory.joinpath("__init__.py")
            for path in output_paths
            for directory in path.parents
        )
        - output_paths
    )

    for init_file in init_files:
        init = response.file.add()
        init.name = str(init_file)

    for filename in sorted(output_paths.union(init_files)):
        print(f"Writing {filename}", file=sys.stderr)


def main():
    """The plugin's main entry point."""
    # Read request message from stdin
    data = sys.stdin.buffer.read()

    # Parse request
    request = plugin.CodeGeneratorRequest()
    request.ParseFromString(data)

    # Create response
    response = plugin.CodeGeneratorResponse()

    # Generate code
    generate_code(request, response)

    # Serialise response message
    output = response.SerializeToString()

    # Write to stdout
    sys.stdout.buffer.write(output)


if __name__ == "__main__":
    main()
