from os.path import dirname, realpath
from re import compile as re_compile

from lxml import etree


class IndexedTuple(tuple):
    def __hash__(self):
        return hash(self[0])


class ApiParser:
    __slots__ = ["__type_split_regex", "__primitive_types", "__extract_text", "__extract_all_text"]

    def __init__(self):
        self.__type_split_regex = re_compile(" or ")

        # primitive types
        self.__primitive_types = {"Float", "Integer", "String", "Array", "Boolean"}

        # function to extract the text from the node
        self.__extract_text = etree.XPath("string()")

        # function to extract the text from the node and the descendant nodes
        extract_all_text_list = etree.XPath("descendant-or-self::text()")
        self.__extract_all_text = lambda node: "".join(extract_all_text_list(node))

    def __extract_type_list(self, cell, extract_all_text):
        return tuple(
            # normalize "Float number" to "Float"
            ("Float",) if _type.startswith("Float") else tuple(reversed(_type.split(" of ")))
            # gets the text if the node is only text, extracts the text if the node contains tags (e.g. links)
            # then splits it to get all the types (if there is more than one)
            for _type in extract_all_text(cell).split(" or ")
        )

    def __add_entity(self, _type, name, params, endpoints, types):
        if _type == 0:
            endpoints.append((name, params))
        elif _type == 1:
            types[name] = (name, params)

    def parse(self, source: str):
        # avoid too much getattr machinery
        primitive_types = self.__primitive_types
        extract_text = self.__extract_text
        extract_all_text = self.__extract_all_text
        extract_type_list = self.__extract_type_list
        add_entity = self.__add_entity

        # parse the HTML source
        tree = etree.HTML(source)

        # get the version
        version = tree.xpath('//*[@id="dev_page_content"]/p[1]/strong')[0].text
        version = version.rsplit(" ", 1)[1]

        # node from where to start the parsing (the available methods section)
        starting_node = tree.xpath('//*[@id="dev_page_content"]/h3[text()="Getting updates"]')[0]

        # -1 is not valid, 0 is endpoint, 1 is type
        endpoints = []
        types = {}
        entity_type = -1

        # Main Type -> [Subtypes]
        aliases = {}

        # Subtype -> Main Type
        reversed_aliases = {}

        # loop variables
        name = None
        params = None

        for el in starting_node.itersiblings():
            # the telegram API page is very unfriendly to parse in some way:
            # you would expect each endpoint definition to be contained in a div or something but it's not, it's just a
            # stream of tags so we have to delimit a sequence of tags that makes sense
            if el.tag == "h4":
                # <h4> signals a new entity
                # put the current entity in the correct array, if applicable
                add_entity(entity_type, name, params, endpoints, types)

                # h4 tags are structured like <h4><a>link</a>ENDPOINT_NAME</a>
                # since we want that "ENDPOINT_NAME" part extracting text by XPath does that
                name = extract_text(el)
                if " " in name:
                    entity_type = -1
                    continue

                # if the name begins with a lower letter it's an endpoint, else it's a type (bool(True) = 1)
                entity_type = int(name[0].isupper())

                params = ()
            elif el.tag == "p":
                # get description
                pass
            elif el.tag == "h3":
                # <h3> signals an end of section: append the current entity
                add_entity(entity_type, name, params, endpoints, types)

                # avoid appending anything else later
                entity_type = -1
            elif el.tag == "ul":
                # entities with an "ul" are lists of names that should be used instead of it
                # insert everything inside the aliases dict
                if entity_type == -1:
                    continue

                # each <li> contains an <a>
                aliases[name] = [alias[0].text for alias in el.iterchildren()]
                reversed_aliases.update((alias[0].text, name) for alias in el.iterchildren())

                # don't append the type since we have it already
                entity_type = -1
            elif el.tag == "table":
                # get the <tbody>
                table = el[1]

                # normalize the entity into an array of tuples (name, type list, required ? True : False)
                if entity_type:
                    # entity_type = 1 --> type
                    # row[0] = name
                    # row[1] = type
                    # row[2] = description (begins with "Optional" if optional)
                    params = tuple(
                        # fmt: off
                        IndexedTuple((
                            row[0].text,
                            extract_type_list(row[1], extract_all_text),
                            not ((desc_cell := row[2]).text or extract_all_text(desc_cell)).startswith("Optional"),
                        ))
                        # fmt: on
                        for row in table.iterchildren()
                    )
                else:
                    # entity_type = 0 --> endpoint
                    # row[0] = name
                    # row[1] = type
                    # row[2] = Yes if required, Optional if optional
                    # row[3] = description
                    params = tuple(
                        # fmt: off
                        IndexedTuple((
                            row[0].text,
                            extract_type_list(row[1], extract_all_text),
                            row[2].text == "Yes"
                        ))
                        # fmt: on
                        for row in table.iterchildren()
                    )

        # append the last one
        add_entity(entity_type, name, params, endpoints, types)

        # actually used types (in correct order)
        used_types_deduped = []

        # get alias common params
        for alias, type_names in aliases.items():
            # build a set with the first type params
            _, first_type_params = types[type_names[0]]
            common_params = set(first_type_params)

            # keep only the intersection with each alias
            for type_name in type_names[1:]:
                _, params = types[type_name]
                common_params.intersection_update(params)

            used_types_deduped.append((alias, common_params))

            # remove common params from child classes
            for type_name in type_names:
                _, params = types[type_name]
                params = set(params)
                params.difference_update(common_params)
                types[type_name] = (type_name, params)

        # keep only the types that are actually used
        used_types = []

        used_type_names = set(
            base_type
            for endpoint in endpoints
            for param in endpoint[1]
            for _type in param[1]
            if (base_type := _type[0]) not in primitive_types
        )
        _used_type_names = set()

        used_type_names_arr = [used_type_names, _used_type_names]
        used_type_names_idx = 0

        # keep track of the types used by the types to process them later
        while used_type_names:
            for type_name in used_type_names:
                if (type_aliases := aliases.get(type_name, None)) :
                    # if the type has aliases we process it and add the aliases
                    _used_type_names.update(alias for alias in type_aliases)

                elif (_type := types.get(type_name, None)) :
                    # if we have found a definition add the definition and process other custom types (if there's any)
                    used_types.append(_type)
                    _used_type_names.update(
                        base_type
                        for param in _type[1]
                        for param_type in param[1]
                        if (base_type := param_type[0]) not in primitive_types
                    )

            # iterate over the remaining types
            used_type_names_idx = 1 - used_type_names_idx
            used_type_names.clear()
            used_type_names = used_type_names_arr[used_type_names_idx]
            _used_type_names = used_type_names_arr[1 - used_type_names_idx]

        # we insert each type an a list and deduplicate them later to keep them in the correct order
        used_types_deduped.extend(
            _type
            for _type in reversed(used_types)
            if not ((name := _type[0]) in used_type_names or used_type_names.add(name))
        )

        return version, endpoints, used_types_deduped, reversed_aliases
