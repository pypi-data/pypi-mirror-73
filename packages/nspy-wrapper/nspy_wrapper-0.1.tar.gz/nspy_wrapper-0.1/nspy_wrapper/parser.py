from .nspy_wrapper_exceptions import *
from xml.etree.ElementTree import fromstring, Element, XMLParser
from warnings import warn


class nsParser:
    @staticmethod
    def data_to_etree(data):
        """ Takes a returned "data" object from the NationStates API and parses it into an XML ElementTree.

        :param data: data from the NationStates API
        :return: <ElementTree.Element> the root element of the XML data
        """
        try:
            decoded_data = data.decode("utf-8")
            prep_data = str(decoded_data).replace('\n', "")
        except IndexError:
            warn("Unable to strip non-XML characters from returned data", MalformedXML)
            return data

        resp_data = fromstring(prep_data, XMLParser(encoding="utf-8"))
        return resp_data

    @staticmethod
    def etree_to_dict(etree):
        """ Takes an ElementTree object from the NationStates API and crudely parses it into a dict

        :param etree: a parsed ElementTree.Element from the NS API. See function data_to_etree.
        :return: <dict> a dict/list structure containing the data in a more readable format.
        """
        if type(etree) == Element:
            if etree.text is not None:
                final_dict = {etree.tag: etree.text}
            else:
                tags = [child.tag for child in etree]
                duplicates = [dupe for dupe in tags if tags.count(dupe) > 1]
                list_of_children = list(APIParser.etree_to_dict(child) for child in etree)

                if duplicates:
                    if tags == duplicates:
                        final_dict = {etree.tag: list_of_children}
                    else:
                        list_of_not_dupes = list(
                            APIParser.etree_to_dict(single) for single in etree if single.tag not in duplicates)
                        list_of_just_dupes = list(
                            APIParser.etree_to_dict(dupe) for dupe in etree if dupe.tag in duplicates)
                        dupe_list_tag = duplicates[0]

                        output = {}
                        for x in list_of_not_dupes:
                            output.update(x)

                        output.update({dupe_list_tag + "S": list_of_just_dupes})
                        final_dict = {etree.tag: output}
                else:
                    output = {} 
                    for x in list_of_children:
                        output.update(x)
                    final_dict = {etree.tag: output}

            if etree.attrib is not None:
                final_dict.update(('@' + k, v) for k, v in etree.attrib.items())

            return final_dict
        else:
            return etree

    @staticmethod
    def data_to_dict(data):
        etree = APIParser.data_to_etree(data)
        dictionary = APIParser.etree_to_dict(etree)

        return dictionary
