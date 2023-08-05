from black import FileMode, format_file_contents

from telegen import __version__


class PythonApiGenerator:
    __slots__ = [
        "__space",
        "__custom_types",
        "__custom_endpoints",
        "__type_to_type_map",
        "__name_to_type_map",
        "__name_to_value_map",
        "__imports_str",
    ]

    def __init__(self):
        self.__space = " " * 4
        SPACE = self.__space

        # types that must be implemented by hand
        self.__custom_types = {
            # InputFile and related
            "InputFile",
            # ReplyMarkup
            "InlineKeyboardMarkup",
            "ReplyKeyboardMarkup",
            "ReplyKeyboardRemove",
            "ForceReply",
            # consequences of ReplyMarkup
            "KeyboardButton",
            "InlineKeyboardButton",
        }

        self.__custom_endpoints = {"sendMediaGroup", "editMessageMedia"}

        # maps a Telegram APi param *type* into a Python type
        self.__type_to_type_map = {
            "String": "str",
            "Integer": "int",
            "Float": "float",
            "Boolean": "bool",
        }

        # maps a Telegram API param *name* to a Python type
        self.__name_to_type_map = {
            # InputFile
            "animation": "InputFile",
            "audio": "InputFile",
            "certificate": "InputFile",
            "document": "InputFile",
            "photo": "InputFile",
            "png_sticker": "InputFile",
            "sticker": "InputFile",
            "tgs_sticker": "InputFile",
            "thumb": "InputFile",
            "video": "InputFile",
            "video_note": "InputFile",
            "voice": "InputFile",
            # the media field is announced as String, good job telegram monkeys!
            "media": "InputFile",
            # other types
            "parse_mode": "ParseMode",
        }

        # maps a Telegram API param name to his value (e.g. a property on an object)
        self.__name_to_value_map = {
            # InputFile
            "animation": 'animation("animation", files)',
            "audio": 'audio("audio", files)',
            "certificate": 'certificate("certificate", files)',
            "document": 'document("document", files)',
            "photo": 'photo("photo", files)',
            "png_sticker": 'png_sticker("png_sticker", files)',
            "sticker": 'sticker("sticker", files)',
            "tgs_sticker": 'tgs_sticker("tgs_sticker", files)',
            "thumb": 'thumb("thumb", files, attach="thumb")',
            "video": 'video("video", files)',
            "video_note": 'video_note("video_note", files)',
            "voice": 'voice("voice", files)',
            # other types
            "parse_mode": "parse_mode.name",
            "reply_markup": "json_dumps(reply_markup.serialized, check_circular=False)",
        }

        # added to the beginning of the generated file
        self.__imports_str = (
            f"from json import dumps as json_dumps\n"
            f"from typing import List, Optional, Tuple, Union\n\n"
            f"try:\n"
            f"{SPACE}from typing import TypedDict\n"
            f"except:\n"
            f"{SPACE}try:\n"
            f"{SPACE}{SPACE}from mypy_extensions import TypedDict\n"
            f"{SPACE}except:\n"
            f"{SPACE}{SPACE}TypedDict = dict\n\n"
            f"from .multipart_encoder import MultipartEncoder\n"
            f"from .types import *\n\n"
            f"\n"
        )

    def __build_param_definition(self, name, types, type_to_type_map, name_to_type_map, name_to_value_map):
        if len(types) > 1:
            # if the types array has length > 1 it's a Union
            type_def = name_to_type_map.get(
                # check if the name is associated to a type
                name,
                # or compose the type using the definitions:
                # if the single type has length > 1 it's a List[Type]
                # e.g. for length = 3 the type is a List[List[Type]]
                # for each type use the corresponding Python type if there's one (e.g. String --> str)
                # or use the name itself if not
                (
                    "Union["
                    + ", ".join(
                        f"List[" * (size := len(_type) - 1)
                        + type_to_type_map.get((base_type := _type[0]), base_type)
                        + "]" * size
                        for _type in types
                    )
                    + "]"
                ),
            )
        else:
            _type = types[0]
            base_type = _type[0]
            type_def = name_to_type_map.get(
                name, f"List[" * (size := len(_type) - 1) + type_to_type_map.get(base_type, base_type) + "]" * size
            )

        # derive the actual value from the value of the parameter
        # print(types[])
        value = name_to_value_map.get(
            name, f"json_dumps({name}, check_circular=False)" if types[0][0] not in type_to_type_map else name,
        )

        return type_def, value

    def generate(self, version, endpoints, types, reversed_aliases):
        # avoid too much getattr machinery
        SPACE = self.__space
        custom_types = self.__custom_types
        custom_endpoints = self.__custom_endpoints
        type_to_type_map = self.__type_to_type_map
        name_to_type_map = self.__name_to_type_map
        name_to_value_map = self.__name_to_value_map
        imports = self.__imports_str
        build_param_definition = self.__build_param_definition

        endpoint_defs = []
        for endpoint in endpoints:
            _name, params = endpoint

            if _name in custom_endpoints:
                continue

            required_params = []
            optional_params = []
            params_decl = []
            after_params = []
            body = []

            input_file_pre = ""
            input_file_post = ""

            input_media = ""

            for param in params:
                name, _types, required = param

                type_def, value = build_param_definition(
                    name, _types, type_to_type_map, name_to_type_map, name_to_value_map
                )

                # ugly special cases
                # see the descriptions in the constructor and the InputFile definition and you'll get how this works
                if type_def == "InputFile":
                    # if the method has an InputFile or InputMedia there will be some params that fill files if the media is not an url or id
                    input_file_pre = f"{SPACE}files: List[Tuple[bytes, bytes, bytes, bytes]] = []\n\n"

                    # if the media are filled we must send a POST request, else we return the usual GET
                    input_file_post = (
                        f"{SPACE}if files:\n"
                        f"{SPACE}{SPACE}headers = {{}}\n"
                        f"{SPACE}{SPACE}encoder = MultipartEncoder(files=files)\n"
                        f'{SPACE}{SPACE}headers["content-type"], body = encoder.encode()\n'
                        f'{SPACE}{SPACE}return "POST", "{_name}", headers, params, body\n'
                        f"{SPACE}else:\n{SPACE}"
                    )

                    attach = '"thumb"' if name == "thumb" else "None"

                    if required:
                        required_params.append(f"{name}: {type_def}")
                        after_params.append(f'{SPACE}{name}("{name}", files, params, attach={attach})\n\n')
                    else:
                        optional_params.append(f"{name}: Optional[{type_def}] = None")
                        after_params.append(
                            f"{SPACE}if {name} is not None:\n"
                            f'{SPACE}{SPACE}{SPACE}{name}("{name}", files, params, attach={attach})\n\n'
                        )
                else:
                    if required:
                        # if the type is required there's no default
                        required_params.append(f"{name}: {type_def}")

                        # add the param to the dict initialization
                        params_decl.append(f'{SPACE}{SPACE}"{name}": {value}')
                    else:
                        # if the type is optional his default value is None
                        optional_params.append(f"{name}: Optional[{type_def}] = None")

                        # add the param to the dict if there's no default
                        # don't format the following lines for clarity
                        # fmt: off
                        body.append(
                            f"{SPACE}if {name} is not None:\n"
                            f'{SPACE}{SPACE}params["{name}"] = {value}\n\n'
                        )
                        # fmt: on

            if required_params:
                # if there are required parameters we build the dict and init it with the values
                params_return_var = "params"
                params_decl = f"{SPACE}params: dict = {{\n" + f",\n".join(params_decl) + f"\n{SPACE}}}\n\n"

                # the only defference from the "only optional" case is that here we put a "," after the required params
                # and before the optional params (if there are any)
                required_params = ", ".join(required_params)
                optional_params = (", *, " + ", ".join(optional_params)) if optional_params else ""
            elif optional_params:
                # if there are only optional parameters we create the dict but return None if the dict is not good
                params_return_var = "params or None"
                params_decl = f"{SPACE}params: dict = {{}}\n\n"

                required_params = ""
                optional_params = "*, " + ", ".join(optional_params)
            else:
                # if there are no params we return None and don't even create the dict
                params_return_var = "None"
                params_decl = ""
                required_params = ""
                optional_params = ""

            body = "".join(body)
            after_params = "".join(after_params)

            endpoint_defs.append(
                f"def {_name}({required_params}{optional_params}) -> EndpointCall:\n"
                f"{input_file_pre}"
                f"{input_media}"
                f"{params_decl}"
                f"{after_params}"
                f"{body}"
                f"{input_file_post}"
                f'{SPACE}return "GET", "{_name}", None, {params_return_var}, None\n'
            )
            # print(endpoint_defs[-1])

        type_defs = []
        for _type in types:
            _name, params = _type

            if _name in custom_types:
                continue

            required_params = []
            optional_params = []

            for param in params:
                name, _types, required = param

                type_def, value = build_param_definition(
                    name, _types, type_to_type_map, name_to_type_map, name_to_value_map
                )

                if required:
                    required_params.append(f"{SPACE}{name}: {type_def}")
                else:
                    optional_params.append(f"{SPACE}{name}: Optional[{type_def}]")

            if required_params:
                required_params = "\n".join(required_params)
                optional_params = ("\n" + "\n".join(optional_params)) if optional_params else ""
            else:
                required_params = ""
                optional_params = "\n".join(optional_params) or f"{SPACE}pass"

            base_class = reversed_aliases.get(_name, "TypedDict")

            # fmt: off
            type_defs.append(
                f"class {_name}({base_class}, total=False):\n"
                f"{required_params}"
                f"{optional_params}\n"
            )
            # fmt: on

        code = imports + "".join(type_defs) + "".join(endpoint_defs)
        code = format_file_contents(code, fast=False, mode=FileMode())

        return {"telegen_definitions/generated.py": code, "version.txt": f"{version}.{__version__}"}
