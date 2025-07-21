from abc import ABC, abstractmethod
import json
# from jsoncomment import JsonComment
from pprint import pprint
from icecream import ic
# import ast
# from pydantic import 

# class VSCodeProfileSetting:
#     ...

class GistVSCodePofile:
    name: str
    extensions: list
    globalState: dict
    
    def __init__(self, name: str, extension: list, globalState: dict):
        self.name = name
        self.extensions = extension
        self.globalState = globalState

class IVSCodeProfileSettings(ABC):
    """Convert the VSCode Profile Settings File into a json object"""
    
    @classmethod
    @abstractmethod
    def parse_local_vscode_profile_to_json(cls, settings_source_json: str, extensions_source_json: str) -> json:
        pass

    # @staticmethod
    @classmethod
    @abstractmethod
    def parse_gist_vscode_profile_to_json(cls, gist_source_json: str) -> GistVSCodePofile:
        pass


class VSCodeProfileSettingsParser(IVSCodeProfileSettings):

    def __init__(self):
        pass

    @classmethod
    def parse_local_vscode_profile_to_json(cls, source_json: str) -> json:
        
        # If no data received, return empty JSON object
        if source_json == "":
            return json.loads("{}")

        # The raw text content is received from the file

        # 1) remove 
        #       - Commented lines with "//"" which vscode allows but the JSON standard does not
        #       - Empty lines
        split_source_json:list[str] = source_json.splitlines()
        split_source_json_cleaned: list[str] = []

        for line in split_source_json:
            if str(line).strip()[0:2] == "//":
                continue
            if str(line).strip() == "":
                continue
            # options to deal with eg /* */ ?
            split_source_json_cleaned.append(line)


        # # 2) remove 
        # #       The trailing comma to the last element
        # # JSON standard does not allow the trailing comma after the last element
        # #   Here is a weak kludge to remove that comma if it exists
        # #   It seems to work on the few profiles I tested with
        # #   There has to be a safer way!
        last_element_end: str = split_source_json_cleaned[len(split_source_json_cleaned) - 2]

        if last_element_end[len(last_element_end) - 1] == ",":
            last_element_end = last_element_end[0:len(last_element_end) - 1]
            split_source_json_cleaned[len(split_source_json_cleaned) - 2] = last_element_end


        # Turn the data back into a string
        cleaned_json = str("".join([str(line + '\n') for line in split_source_json_cleaned]))

        # Load this string that *SHOULD* now be json compliant
        final_json = json.loads(cleaned_json)
        # ic(final_json.keys())

        return final_json

    @classmethod
    def parse_gist_vscode_profile_to_json(cls, source_json: json) -> GistVSCodePofile:

        # If no data received, return empty JSON object
        if source_json == "":
            print("Source data is empty, aborting")
            return json.loads("{}")

        # Space for potential additional verification / modifications
        ic(source_json.keys())

        gist_json = source_json

        details: GistVSCodePofile = cls._extract_extensions_from_gist(gist_json)
        return details

    @classmethod
    def _extract_extensions_from_gist(cls, gist_json: json) ->  GistVSCodePofile:
        
        # ic(type(gist_json["files"][list(gist_json["files"].keys())[0]]["content"]))
        useful_data = json.loads(gist_json["files"][list(gist_json["files"].keys())[0]]["content"])

        # ic(useful_data.keys())

        gist_profile_name = useful_data["name"]
        gist_profile_extensions = json.loads(useful_data["extensions"])
        gist_profile_globalState = json.loads(useful_data["globalState"])
        
        # ic(gist_profile_extensions)
        # ic(type(gist_profile_name))
        # ic(type(gist_profile_extensions))
        # ic(type(gist_profile_globalState))

        return GistVSCodePofile(name=gist_profile_name, 
                                extension=gist_profile_extensions, 
                                globalState=gist_profile_globalState)
