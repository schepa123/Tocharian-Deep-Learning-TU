import xml.etree.ElementTree as ET
import os
from pathlib import Path
import re
import json
from os import walk


def get_namespace(element):
  """
  Return the namespace of a xml file

  Keyword arguments:
  element -- an xml file
  """
  m = re.match('\{.*\}', element.tag)
  return m.group(0) if m else ''


def check_file_desc(element, entry):
    """
    Search the tag fileDesc in the xml file for meta information of the fragment and saves it in a dictionary

    Keyword arguments:
    element -- first element of the root of the xml tree, tag fileDesc
    entry -- a dictionary, in which the informations are saved
    """
    for child_element in list(element):
        key_value = element.tag.split("}")[1] + "_" + child_element.tag.split("}")[1]
        if not list(child_element):
            if not child_element.attrib:
                entry[key_value] = child_element.text
            else:
                if element.tag.split("}")[1] == "keywords":
                    key_value = key_value + "_[" + child_element.attrib["type"] + "]"
                if child_element.text is None:
                    if child_element.tag.split("}")[1] == "prefixDef":
                        continue  # Not needed for Task
                    entry[key_value] = {}
                    entry[key_value]["value"] = ""
                    entry[key_value]["attribute"] = child_element.attrib
                else:
                    entry[key_value] = {}
                    entry[key_value]["value"] = child_element.text
                    entry[key_value]["attribute"] = child_element.attrib

        else:
            check_file_desc(element=child_element, entry=entry)


def check_source_doc(element, entry):
    """
    Search the tag encodingDesc in the xml file for information on the surface of the fragment, aka the text and saves it in a dictionary

    Keyword arguments:
    element -- second element of the root of the xml tree, tag encodingDesc
    entry -- a dictionary, in which the informations are saved
    """
    for child_element in list(element):
        key_value = element.tag.split("}")[1] + "_" + child_element.tag.split("}")[1]
        if not list(child_element):
            if not child_element.attrib:
                entry[key_value] = child_element.text
            else:
                if key_value in entry:
                    entry[str(key_value)]["attribute"].update(child_element.attrib)
                else:
                    if element.tag.split("}")[1] == "line":
                        child_tag_temp = child_element.tag.split("}")[1]
                        if child_tag_temp == "gap" or child_tag_temp == "unclear" or child_tag_temp == "space":
                            continue
                        key_value = key_value + "_[" + child_element.attrib["points"] + "]"

                    if child_element.text is None:
                        entry[key_value] = {}
                        entry[key_value]["value"] = ""
                        entry[key_value]["attribute"] = child_element.attrib
                    else:
                        entry[key_value] = {}
                        entry[key_value]["value"] = child_element.text
                        entry[key_value]["attribute"] = child_element.attrib

        else:
            if list(element) and element.attrib:
                key_value = key_value + "_[" + child_element.attrib["points"] + "]"
                entry[key_value] = {}
                if child_element.text is not None:
                    entry[key_value] = child_element.text
                else:
                    entry[key_value] = ""
                if child_element.attrib is not None:
                    entry[key_value] = child_element.attrib
                else:
                    entry[key_value] = {}
            check_source_doc(element=child_element, entry=entry)

def check_if_zones_present(element):
    """
    Check if the xml file has points associated with the characters on the fragment. If yes return True otherwise False.
    :param element: The root of xml-tree
    """
    zone_boolean = False
    namespace = get_namespace(element)
    if not element.findall(".//" + namespace + "line"):
        return False
    for children in list(element.findall(".//" + namespace + "line"))[0]:
        if "points" in children.attrib:
            zone_boolean = True
        else:
            return False
        return zone_boolean

def get_fragements_with_zone(path):
    """
    Return only the files with zones associated with the characters of the fragment
    :param path: Path of the fragments
    """
    fragments_with_zones = []
    files_in_path = []
    for (dirpath, dirnames, filenames) in walk(path):
        files_in_path.extend(filenames)
    for fragment in files_in_path:
        p = Path(os.path.join(path, fragment))
        myTree = ET.parse(p)
        myroot = myTree.getroot()
        if check_if_zones_present(myroot):
            fragments_with_zones.append(fragment)
    return fragments_with_zones

def save_information_of_fragments_zones(fragments_path, fragments, output):
    for fragment in fragments:
        p = Path(os.path.join(fragments_path, fragment))
        myTree = ET.parse(p)
        myRoot = myTree.getroot()
        entry = {}
        check_file_desc(element=myRoot[0], entry=entry)
        check_source_doc(element=myRoot[1], entry=entry)

        with open(os.path.join(output, fragment.split(".")[0] + ".json"), "w", encoding="utf-8") as f:
            json.dump(entry, f, ensure_ascii=False, indent=4)



good_fragments = get_fragements_with_zone("../data/xml_files")
save_information_of_fragments_zones("../data/xml_files", good_fragments, "../data/fragments_zone")



























