""" Python application to help clean up VSCode Profiles saved in github gists"""
__author__ = "Squizzy"
__copyright__ = "Copyright 2024-now, Squizzy"
__credits__ = "MS for VSCode, all the extensions devs, all who give out advice"
__license__ = "GPLv2"
__version__ = "0.2"
__maintainer__ = "Squizzy"

import os
import sys
import json
import xmltodict # type: ignore
# import tkinter as tk
from tkinter import filedialog, messagebox #, ttk
# from pydantic import BaseModel
from abc import ABC, abstractmethod
from pprint import pprint

class IFileIO(ABC):
    """Interface file for the file manager"""
    @abstractmethod
    def load_vscode_profile_to_modify(self) -> bool:
        """Acquire the json data from the VSCode profile to be processed.
        - Either use command line argument or query which file should be loaded
        - Loads the serialised JSON data into 'profile_data'

        returns:
            (bool): True if valid JSON data was loaded into 'profile data', false otherwise
        """
        pass

class FileIO(IFileIO):
    """File manager to read and write the profiles and extensions data"""
    _local_vscode_registered_profiles: dict[str, str]
    
    _local_profiles_folders: list[str]
    
    # _local_extensions_paths: list[str]
    _local_extensions_from_folders: dict[str, tuple[str, str]] # key: foldername, values: (extension name, version)
    _local_extensions_from_file: dict[str, tuple[str, str]] # key: foldername, values: (extension name, version)
    _local_obsolete_extensions: dict[str, bool] # key: extension name, value: is obsolete
    
    _local_extensions_settings_keys: dict[str, list[str]] # key: extension name, value: list of settings key values
    
    _profile_to_modify_filepath: str
    _profile_to_modify_data: str

    def __init__(self):
        self._local_vscode_registered_profiles = {}
        
        self._full_path_to_local_profiles: str
        self._local_profiles_folders = []
        self._local_profiles_names = []
        
        self._full_path_to_local_extensions: str
        self._local_extensions_from_folders = {}
        self._local_extensions_from_file = {}
        self._local_obsolete_extensions = {}
        
        self._local_extensions_settings_keys = {}
        
        self._profile_to_modify_filepath = ""
        self._profile_to_modify_data = ""
        pass

    @property
    def profile_data(self) -> str:
        return self._profile_to_modify_data

    def _get_vscode_registered_vscode_profiles(self) -> bool:
        """Retrieve the list of profiles that vscode has registered internally
        
        profile names and associated folders names are listed in globalStorage storage.json:
        WINDOWS:    C:\\Users\\PROFILE_NAME\\AppData\\Roaming\\Code\\User\\globalStorage\\storage.json
        
        returns:
            (bool): True is the list of profiles that vscode has registered internally has been recovered
        """
        globalStorage_storage_json = ""
        
        # Set the path for the OS we are currently working with
        if os.name == 'nt':
            WINDOWS_GLOBAL_STORAGE_FILE: str = os.path.join(str(os.getenv('APPDATA')), "Code", "User", "globalStorage", "storage.json")
            globalStorage_storage_json = WINDOWS_GLOBAL_STORAGE_FILE
        elif os.name == 'darwin':
            MACOS_GLOBAL_STORAGE_FILE: str = os.path.join(os.environ['HOME'], "Library", "Application Support", "Code", "User", "globalStorage", "storage.json")
            globalStorage_storage_json = MACOS_GLOBAL_STORAGE_FILE
        elif os.name == 'posix':
            LINUX__GLOBAL_STORAGE_FILE: str = os.path.join(os.environ['HOME'], ".config", "Code", "User", "profilesglobalStorage", "storage.json")
            globalStorage_storage_json = LINUX__GLOBAL_STORAGE_FILE
        else:
            print("Unsupported operating system")
            return False
        
        
        if not os.path.isfile(globalStorage_storage_json):
            print("No VSCode globalStorage storage.json, aborting")
            return False
        
        with open(globalStorage_storage_json, 'r') as globalStorage_storage:
            storage = json.load(globalStorage_storage)
        
        # The link vscode profile name and vscode folder name are stored in userDataProfiles in storage.json
        # in a list of dictionaries that contain {location: 'vscode folder name', 'name': 'vscode profile name'}
        if "userDataProfiles" not in storage:
            print("No VSCode userDataProfiles found in globalStorage storage.json, aborting")
            return False
        
        # Check if there are any profile registered in userDataProfiles
        if storage["userDataProfiles"] == []:
            print("No VSCode profile has been registered in vscode (eg no profile has been created yet), aborting")
        
        # If so, then load them
        for profile in storage["userDataProfiles"]:
            self._local_vscode_registered_profiles[profile['location']] = profile['name']
        
        print(f"found {len(self._local_vscode_registered_profiles)} vscode profiles registered in vscode")
        
        return True

    def _get_vscode_local_profiles(self) -> bool:
        """Retrieve all VSCode profiles on the current machine
        profiles are stored in the following locations:
        Windows:    %APPDATA%\\Code\\User\\profiles
        macOS       $HOME/Library/Application\\ Support/Code/User/profiles.
        Linux       $HOME/.config/Code/User/profiles.
        """
        local_profiles_path: str
        local_profiles: list[str]       
         
        # Get the profile names associated to the profiles folder names registered in vscode
        if not self._get_vscode_registered_vscode_profiles():
            return False
        
        # Set the local profiles path for the OS we are currently working with
        if os.name == 'nt':
            WINDOWS_PATH: str = os.path.join(str(os.getenv('APPDATA')), "Code", "User", "profiles")
            local_profiles_path = WINDOWS_PATH
        elif os.name == 'darwin':
            MACOS_PATH: str = os.path.join(os.environ['HOME'], "Library", "Application Support", "Code", "User", "profiles")
            local_profiles_path = MACOS_PATH
        elif os.name == 'posix':
            LINUX_PATH: str = os.path.join(os.environ['HOME'], ".config", "Code", "User", "profiles")
            local_profiles_path = LINUX_PATH
        else:
            print("Unsupported operating system")
            return False 
        
        self._full_path_to_local_profiles = local_profiles_path
        
        # Check that the folder for the local profiles exists
        if not os.path.isdir(local_profiles_path):
            print("No local profiles folder found, aborting")
        
        # Check that there are local profiles stored in the local profiles folder
        local_profiles = os.listdir(local_profiles_path)
        if local_profiles == []:
            print("No local profiles found, aborting")

        # check that all the local profile folders identified in the local profiles folder the same as that 
        # registered in vscode in globalStorage storage.json
        for local_profile in local_profiles:
            if local_profile not in self._local_vscode_registered_profiles.keys():
                print(f"vscode profile {local_profile} not registered in vscode, aborting")
                return False
        
        self._local_profiles_folders = local_profiles
        print(f"found {len(self._local_profiles_folders)} local profiles")
        
        return True

    def _get_vscode_profile_filename_from_command_line(self) -> bool:
        """Parses the command line argument and returns the location of the profile data, if any
        
        returns:
            (str): The location of the file containing the json of the VSCode profile
        """
        prefix_found: bool = False
        filename_arg_expected: bool = False

        for arg in sys.argv:
            if arg == "-f":
                if not prefix_found:
                    prefix_found = True
                    filename_arg_expected = True
                    continue
                else:
                    print("-f requires a file name to be provided. ignoring.")
                    return False
            elif filename_arg_expected:
                # TODO: need to check that arg is a file that is reachable
                self._profile_to_modify_filepath = arg
                break
            else:
                print("command line argument not recognised. ignoring it.")
                return False
            
        return True
        
    def _get_vscode_profile_filename_from_popup(self) -> bool:
        """Use a popup to let the user select the file to process
        """
        file_path: str

        file_path = filedialog.askopenfilename(
            title="Select the VSCode profile to be processed",
            filetypes=[("JSON files", "*.json")])
        
        if file_path:
            self._profile_to_modify_filepath = file_path
            return True
        else:
            print("No file selected, aborting.")
            return False

            # # self.profile = load_profile(filename)



            # self.settings = extract_settings(self.profile)
            # self.extensions = extract_extensions(self.profile)
            # self.globalstate = extract_globalstate(self.profile)
            # self.display_settings()
            # self.display_extensions()
            # self.display_globalstate()
            # self.save_button.config(state='normal')

    def _get_vscode_profile_from_available_local_profiles(self) -> bool:
        # Currently trying not to mess up with the current vscode...
        # should provide a list of the profiles available and allow the user to select one
        return False

    def _load_vscode_profile_data(self) -> bool:
        """Attempt to load the data from the file selected by the user
        
        return:
            (bool): True if the file is a valid JSON, False otherwise
        """

        # Check if user is ok to load a large file
        MAX_FILE_SIZE: int = 100_000
        
        file_size = os.path.getsize(self._profile_to_modify_filepath)
        
        if file_size > MAX_FILE_SIZE:
            load_anyway: bool = messagebox.askyesno(title="Large file size detected", 
                                                    message=f"""File is more than {MAX_FILE_SIZE} bytes
                                                                This seems rather large.
                                                                Load anyway?""")
            if load_anyway == messagebox.NO:
                print("file too large, user aborted")
                return False        

        # Load the data
        retrieved_data: str
        try:
            with open(self._profile_to_modify_filepath, 'r') as vscode_profile_json_file:
                retrieved_data = vscode_profile_json_file.read(file_size)
        except FileNotFoundError:
            print(f"File {self._profile_to_modify_filepath} not found, aborting")
            return False
        
        # Check the data is json compliant before accepting
        try:
            self._profile_to_modify_data = json.loads(retrieved_data)
        except json.JSONDecodeError:
            # could be done more gracefully with requesting another file for example
            print(f"Problem with file {self._profile_to_modify_filepath}: Not a proper VSCode Profile file (json format expected), aborting")
            return False
        
        return True
        
    def load_vscode_profile_to_modify(self) -> bool:
        """Retrieve the content of a vscode profile file or URL following different logic for selecting the file to load
        
        returns:
            (str): the json raw data from the profile
        """

        if len(sys.argv) > 0:
            # use command line arguments
            if not self._get_vscode_profile_filename_from_command_line():

                if not self._get_vscode_profile_filename_from_popup():
                    print("No file selected, aborting.")
                    return False

        if not self._load_vscode_profile_data():
            print("No data found in the profile file, or not a proper VSCode profile file, aborting")
            return False
        
        return True


    def _get_local_extensions_list_from_json_file(self) -> bool:
        """Reads the local extensions list from a JSON file
        the file is located under:
        WINDOWS:    %USERPROFILE%\\.vscode\\extensions
        MACOS:      ~/.vscode/extensions
        LINUX:      ~/.vscode/extensions
        """
        extensions_from_file: dict[str, tuple[str, str]] = {}
        
        # Set the path for the OS we are currently working with
        if os.name == 'nt':
            WINDOWS_EXTENSIONS_FOLDER: str = os.path.join(str(os.getenv('USERPROFILE')), ".vscode", "extensions")
            local_extensions_folder = WINDOWS_EXTENSIONS_FOLDER
        elif os.name == 'darwin':
            MACOS_EXTENSIONS_FOLDER: str = os.path.join(os.environ['HOME'], ".vscode", "extensions")
            local_extensions_folder = MACOS_EXTENSIONS_FOLDER
        elif os.name == 'posix':
            LINUX_EXTENSIONS_FOLDER: str = os.path.join(os.environ['HOME'], ".vscode", "extensions")
            local_extensions_folder = LINUX_EXTENSIONS_FOLDER
        else:
            print("Unsupported operating system")
            return False

        # Check that the folder for the local extensions exists
        if not os.path.isdir(local_extensions_folder):
            print("No local extensions folder found, aborting")
            return False
        
        # Check if the extensions.json file exist
        EXTENSIONS_JSON = "extensions.json"
        extensions_json_path = os.path.join(local_extensions_folder, EXTENSIONS_JSON)
        if not os.path.isfile(extensions_json_path):
            print(f"File {extensions_json_path} not found, aborting")
            return False
        
        # load the extensions data from extensions_file
        with open(extensions_json_path, 'r', encoding='utf8') as extensions_json_file:
            extensions_json_data = json.load(extensions_json_file)
        
        # Populate the dictionary with only the interesting info
        for extension in extensions_json_data:
            extension_folder_name = os.path.basename(extension['location']['path'])
            extensions_from_file[extension_folder_name] = (extension['identifier']['id'], 
                                                           extension['version'])
        
        self._local_extensions_from_file = extensions_from_file
        print(f"found {len(self._local_extensions_from_file)} local extensions from extensions.json file")
        
        return True
    
    def _get_local_extensions_list_from_folders(self) -> bool:
        """Generates the list of the extensions that have been locally installed
        Extensions are stored under:
        WINDOWS:    %USERPROFILE%\\.vscode\\extensions
        MACOS:      ~/.vscode/extensions
        LINUX:      ~/.vscode/extensions
        """
        local_extensions_folder: str
        extensions_list: dict[str, tuple[str, str]] = {}
        obsolete_count: int = 0

        self._get_local_extensions_list_from_json_file()

        # Set the path for the OS we are currently working with
        if os.name == 'nt':
            WINDOWS_EXTENSIONS_FOLDER: str = os.path.join(str(os.getenv('USERPROFILE')), ".vscode", "extensions")
            local_extensions_folder = WINDOWS_EXTENSIONS_FOLDER
        elif os.name == 'darwin':
            MACOS_EXTENSIONS_FOLDER: str = os.path.join(os.environ['HOME'], ".vscode", "extensions")
            local_extensions_folder = MACOS_EXTENSIONS_FOLDER
        elif os.name == 'posix':
            LINUX_EXTENSIONS_FOLDER: str = os.path.join(os.environ['HOME'], ".vscode", "extensions")
            local_extensions_folder = LINUX_EXTENSIONS_FOLDER
        else:
            print("Unsupported operating system")
            return False

        self._full_path_to_local_extensions = local_extensions_folder

        # Check that the folder for the local extensions exists
        if not os.path.isdir(local_extensions_folder):
            print("No local extensions folder found, aborting")
            return False

        # Check that there are local extensions stored in the local extensions folder
        local_extensions = os.listdir(local_extensions_folder)
        if local_extensions == []:
            print("No local extensions found, aborting")
            return False
        
        # Remove the .obsolete and the extensions.json files from this list (if exist)
        if '.obsolete' in local_extensions:
            local_extensions.remove('.obsolete')
        if 'extensions.json' in local_extensions:
            local_extensions.remove('extensions.json')
        
        # From the local extensions path, open the .obsolete file and make a list of the obsolete extensions
        obsolete_extensions: dict[str, bool]
        obsolete_filepath: str = os.path.join(local_extensions_folder, ".obsolete")
        with open(obsolete_filepath, 'r', encoding='utf8') as obsolete_file:
            obsolete_extensions = json.load(obsolete_file)
        
        # For each local extension, recover the <DisplayName> and the Version value from the .vsixmanifest file
        # This file has more reliable information that the extension's package.json file
        # Unfortunately, it is an XML, not a JSON file...
        #
        # Store the information in a dictionary with the <extension folder name> as key and (<extension name>,<version>,<Obsolete status>)) value 
        for local_extension in local_extensions:
            local_extension_vsixmanifest_file = os.path.join(local_extensions_folder, local_extension, ".vsixmanifest")

            if os.path.isfile(local_extension_vsixmanifest_file):
                
                with open(local_extension_vsixmanifest_file, 'r', encoding="utf8") as package_json_file:
                    try:
                        package_json = xmltodict.parse(package_json_file.read())
                        # check if the extension has been declared as obsolete
                        # These should disappear if vscode is restarted
                        if local_extension in obsolete_extensions:
                            if obsolete_extensions[local_extension]: # added in case the obsolete file contains a False? - not sure why it should
                                obsolete_count += 1
                        else:
                            extensions_list[local_extension] = (package_json["PackageManifest"]["Metadata"]["DisplayName"], 
                                                                package_json["PackageManifest"]["Metadata"]["Identity"]["@Version"])
                            
                    except ValueError:
                        print(local_extension_vsixmanifest_file)
                        print("Problem: Not a proper Vsixmanifest XML , skipping")

        self._local_extensions_from_folders = extensions_list
        print(f"found {len(self._local_extensions_from_folders)} local extensions and skilled {obsolete_count} obsolete(s)")
        
        self._local_obsolete_extensions = obsolete_extensions
        print(f"found {len(self._local_obsolete_extensions)} obsolete extensions from the extensions file")
        
        for extension in self._local_extensions_from_folders:
            if extension not in self._local_extensions_from_file:
                
                print(f"NOT FOUND in extensions.json: {extension}")
            if extension in obsolete_extensions:
                # print(f"BUT found in .obsolete file: {extension}")
                pass
        
        return True
            
    def _get_extensions_settings_keys(self) -> bool:
        """Extract the settings keys for each extension"""
        print("PROCESSING EXTENSIONS")
        extensions_settings_keys: dict[str, list[str]] = {}
        
        PACKAGE_JSON_FILE = "package.json"
        
        for extension in self._local_extensions_from_folders:
            package_json_path = os.path.join(self._full_path_to_local_extensions, extension, PACKAGE_JSON_FILE)
            
            if not os.path.isfile(package_json_path):
                print(f"File {package_json_path} not found, skipping")
                continue
            
            with open(package_json_path, 'r', encoding='utf8') as package_json_file:
                try:
                    package_json = json.load(package_json_file)
                except json.JSONDecodeError as e:
                    print(f"Error decoding package.json for {extension}: {e} - skipping")
                    continue

            if "properties" not in str(package_json):
                print("{extension} has no property for settings - skipping")
                continue

            # in here, all package.json contain a "properties".
            # all seem to contain a "contribute", "configuration" too (from the ones I have tested)
            # "properties" however are either a dictionary, or a list of dictionaries
            else:
                extensions_settings_keys[extension] = []

                if "configuration" in package_json["contributes"].keys():

                    # sometimes the properties are a dictionary under contributes > configuration
                    if type(package_json["contributes"]["configuration"]) == type({}):
                        for key in package_json["contributes"]["configuration"]["properties"].keys():
                            extensions_settings_keys[extension].append(key)

                    # otherwise they are a list of dictionaries at the same location
                    elif type(package_json["contributes"]["configuration"]) == type([]):
                        for item in package_json["contributes"]["configuration"]:
                            if "properties" in str(item):
                                for key in item["properties"].keys():
                                    extensions_settings_keys[extension].append(key)   

                    # not yet encountered another possibility, but trapping it just in case
                    else:
                        print(f"{extension}: properties are neither a dictionary or a list. skipping")                            


        total_extensions_keys = 0
        for extension in extensions_settings_keys:
            total_extensions_keys += len(extensions_settings_keys[extension])

        print(f"Found {len(extensions_settings_keys)} extensions with settings keys, for a total of {total_extensions_keys} settings keys")

        self._local_extensions_settings_keys = extensions_settings_keys
        return True
    
            
    def save_profile(self):
        pass
        # kept_settings = {key: self.settings[key] for key, var in self.setting_vars.items() if var.get()}
        # kept_extensions = [ext for ext in self.extensions if self.extension_vars[ext['identifier']['id']].get()]
        # kept_globalstate = {key: self.globalstate[key] for key, var in self.globalstate_vars.items() if var.get()}
        # # update_profile(self.profile, kept_settings, kept_extensions, kept_globalstate)

        # filename = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])
        # if filename:
        #     self._save_profile(self.profile, filename)
        #     messagebox.showinfo("Success", "Profile saved successfully!")
        #     self.changes_made = False

    def _save_profile(self, profile, filename):
        ...
        # with open(filename, 'w') as json_file:
        #     json.dump(profile, json_file, indent=2)


def main():
    print("Nothing implemented")

if __name__ == "__main__":
    main()
