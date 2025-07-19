""" Python application to help clean up VSCode Profiles saved in github gists"""
__author__ = "Squizzy"
__copyright__ = "Copyright 2024, Squizzy"
__credits__ = "Cursor code editor (/VSCode), Claude-AI"
__license__ = "GPL"
__version__ = "0.1"
__maintainer__ = "Squizzy"

import os
import sys
import json
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from pydantic import BaseModel
from abc import ABC, abstractmethod
from pprint import pprint

class VSCodeProfile(BaseModel):
    ...

# class IFileIO(ABC):
#     @abstractmethod
#     def load_vscode_profile_to_modify(self) -> bool:
#         """Acquire the json data from the VSCode profile to be processed.
#         - Either use command line argument or query which file should be loaded
#         - Loads the serialised JSON data into 'profile_data'

#         returns:
#             (bool): True if valid JSON data was loaded into 'profile data', false otherwise
#         """
#         pass

# class FileIO(IFileIO):
#     _local_vscode_registered_profiles: dict[str, str]
    
#     _local_profiles: list[str]
    
#     _local_extensions: list[str]
    
#     _filename: str
#     _profile_data: str

#     def __init__(self):
#         self._local_vscode_registered_profiles = {}
        
#         self._local_profiles_path = ""
#         self._local_profiles = []
#         self._local_profiles_names = []
        
#         self._filename = ""
#         self._profile_data = ""
#         pass
    

#     @property
#     def profile_data(self) -> str:
#         return self._profile_data

#     def _get_vscode_registered_vscode_profiles(self) -> bool:
#         """Retrieve the list of profiles that vscode has registered internally
        
#         profile names and associated folders names are listed in globalStorage storage.json:
#         WINDOWS:    C:\\Users\\PROFILE_NAME\\AppData\\Roaming\\Code\\User\\globalStorage\\storage.json
        
#         returns:
#             (bool): True is the list of profiles that vscode has registered internally has been recovered
#         """
#         globalStorage_storage_json = ""
        
#         # Set the path for the OS we are currently working with
#         if os.name == 'nt':
#             WINDOWS_GLOBAL_STORAGE_FILE: str = os.path.join(os.getenv('APPDATA'), "Code", "User", "globalStorage", "storage.json")
#             globalStorage_storage_json = WINDOWS_GLOBAL_STORAGE_FILE
#         elif os.name == 'darwin':
#             MACOS_GLOBAL_STORAGE_FILE: str = os.path.join(os.environ['HOME'], "Library", "Application Support", "Code", "User", "globalStorage", "storage.json")DER: str = os.path.join(os.environ['HOME'], ".vscode", "extensions")
#             globalStorage_storage_json = MACOS_EXTENSIONS_FOLDER
#         elif os.name == 'posix':
#             LINUX__GLOBAL_STORAGE_FILE: str = os.path.join(os.environ['HOME'], ".vscode", "extensions")
#             globalStorage_storage_json = LINUX__GLOBAL_STORAGE_FILE
#         else:
#             print("Unsupported operating system")
#             return False
        
        
#         if not os.path.isfile(globalStorage_storage_json):
#             print("No VSCode globalStorage storage.json, aborting")
#             return False
        
#         with open(globalStorage_storage_json, 'r') as globalStorage_storage:
#             storage = json.load(globalStorage_storage)
        
#         # The link vscode profile name and vscode folder name are stored in userDataProfiles in storage.json
#         # in a list of dictionaries that contain {location: 'vscode folder name', 'name': 'vscode profile name'}
#         if "userDataProfiles" not in storage:
#             print("No VSCode userDataProfiles found in globalStorage storage.json, aborting")
#             return False
        
#         # Check if there are any profile registered in userDataProfiles
#         if storage["userDataProfiles"] == []:
#             print("No VSCode profile has been registered in vscode (eg no profile has been created yet), aborting")
        
#         # If so, then load them
#         for profile in storage["userDataProfiles"]:
#             self._local_vscode_registered_profiles[profile['location']] = profile['name']
        
#         print(f"found {len(self._local_vscode_registered_profiles)} vscode profiles registered in vscode")
        
#         return True

#     def _get_vscode_local_profiles(self) -> bool:
#         """Retrieve all VSCode profiles on the current machine
#         profiles are stored in the following locations:
#         Windows:    %APPDATA%\\Code\\User\\profiles
#         macOS       $HOME/Library/Application\\ Support/Code/User/profiles.
#         Linux       $HOME/.config/Code/User/profiles.
#         """
#         local_profile_path: str = ""
#         local_profile: list[str]       
         
#         # Get the profile names associated to the profiles folder names registered in vscode
#         if not self._get_vscode_registered_vscode_profiles():
#             return False
        
#         # Set the local profiles path for the OS we are currently working with
#         if os.name == 'nt':
#             WINDOWS_PATH: str = os.path.join(os.getenv('APPDATA'), "Code", "User", "profiles")
#             local_profiles_path = WINDOWS_PATH
#         elif os.name == 'darwin':
#             MACOS_PATH: str = os.path.join(os.environ['HOME'], "Library", "Application Support", "Code", "User", "profiles")
#             local_profiles_path = MACOS_PATH
#         elif os.name == 'posix':
#             LINUX_PATH: str = os.path.join(os.environ['HOME'], ".config", "Code", "User", "profiles")
#             local_profiles_path = LINUX_PATH
#         else:
#             print("Unsupported operating system")
#             return False 
        
#         # Check that the folder for the local profiles exists
#         if not os.path.isdir(local_profiles_path):
#             print("No local profiles folder found, aborting")
        
#         # Check that there are local profiles stored in the local profiles folder
#         local_profiles = os.listdir(local_profiles_path)
#         if local_profiles == []:
#             print("No local profiles found, aborting")

#         # check that all the local profile folders identified in the local profiles folder are registered in vscode
#         for local_profile in self._local_profiles:
#             if local_profile not in self._local_vscode_registered_profiles.keys():
#                 print(f"vscode profile {local_profile} not registered in vscode, aborting")
#                 return False
        
#         self._local_profiles = local_profiles
#         print(f"found {len(self._local_profiles)} local profiles")
        
#         return True

#     def _get_vscode_profile_filename_from_command_line(self) -> bool:
#         """Parses the command line argument and returns the location of the profile data, if any
        
#         returns:
#             (str): The location of the file containing the json of the VSCode profile
#         """
#         prefix_found: bool = False
#         filename_arg_expected: bool = False

#         for arg in sys.argv:
#             if arg == "-f":
#                 if not prefix_found:
#                     prefix_found = True
#                     filename_arg_expected = True
#                     continue
#                 else:
#                     print("-f requires a file name to be provided. ignoring.")
#                     return False
#             elif filename_arg_expected:
#                 # TODO: need to check that arg is a file that is reachable
#                 self._filename = arg
#                 break
#             else:
#                 print("command line argument not recognised. ignoring it.")
#                 return False
            
#         return True
        
#     def _get_vscode_profile_filename_from_popup(self) -> bool:
#         """Use a popup to let the user select the file to process
#         """
#         file_path: str

#         file_path = filedialog.askopenfilename(
#             title="Select the VSCode profile to be processed",
#             filetypes=[("JSON files", "*.json")])
        
#         if file_path:
#             self._filename = file_path
#             return True
#         else:
#             print("No file selected, aborting.")
#             return False

#             # # self.profile = load_profile(filename)



#             # self.settings = extract_settings(self.profile)
#             # self.extensions = extract_extensions(self.profile)
#             # self.globalstate = extract_globalstate(self.profile)
#             # self.display_settings()
#             # self.display_extensions()
#             # self.display_globalstate()
#             # self.save_button.config(state='normal')

#     def _get_vscode_profile_from_available_local_profiles(self) -> bool:
#         # Currently trying not to mess up with the current vscode...
#         # should provide a list of the profiles available and allow the user to select one
#         return False

#     def _load_vscode_profile_data(self) -> bool:
#         """Attempt to load the data from the file selected by the user
        
#         return:
#             (bool): True if the file is a valid JSON, False otherwise
#         """

#         # Check if user is ok to load a large file
#         MAX_FILE_SIZE: int = 100_000
        
#         file_size = os.path.getsize(self._filename)
        
#         if file_size > MAX_FILE_SIZE:
#             load_anyway: bool = messagebox.askyesno(title="Large file size detected", 
#                                                     message=f"""File is more than {MAX_FILE_SIZE} bytes
#                                                                 This seems rather large.
#                                                                 Load anyway?""")
#             if load_anyway == messagebox.NO:
#                 print("file too large, user aborted")
#                 return False        

#         # Load the data
#         retrieved_data: str
#         try:
#             with open(self._filename, 'r') as vscode_profile_json_file:
#                 retrieved_data = vscode_profile_json_file.read(file_size)
#         except FileNotFoundError:
#             print(f"File {self._filename} not found, aborting")
#             return False
        
#         # Check the data is json compliant before accepting
#         try:
#             self._profile_data = json.loads(retrieved_data)
#         except json.JSONDecodeError:
#             # could be done more gracefully with requesting another file for example
#             print(f"Problem with file {self._filename}: Not a proper VSCode Profile file (json format expected), aborting")
#             return False
        
#         return True
        
#     def load_vscode_profile_to_modify(self) -> bool:
#         """Retrieve the content of a vscode profile file or URL following different logic for selecting the file to load
        
#         returns:
#             (str): the json raw data from the profile
#         """

#         if len(sys.argv) > 0:
#             # use command line arguments
#             if not self._get_vscode_profile_filename_from_command_line():

#                 if not self._get_vscode_profile_filename_from_popup():
#                     print("No file selected, aborting.")
#                     return False

#         if not self._load_vscode_profile_data():
#             print("No data found in the profile file, or not a proper VSCode profile file, aborting")
#             return False
        
#         return True


#     def _get_local_extensions_list(self) -> bool:
#         """Generates the list of the extensions that have been locally installed
#         Extensions are stored under:
#         WINDOWS:    %USERPROFILE%\\.vscode\\extensions
#         MACOS:      ~/.vscode/extensions
#         LINUX:      ~/.vscode/extensions
#         """
        

#         # Set the path for the OS we are currently working with
#         if os.name == 'nt':
#             WINDOWS_EXTENSIONS_FOLDER: str = os.path.join(os.getenv('USERPROFILE'), ".vscode", "extensions")
#             self._local_extensions_folder = WINDOWS_EXTENSIONS_FOLDER
#         elif os.name == 'darwin':
#             MACOS_EXTENSIONS_FOLDER: str = os.path.join(os.environ['HOME'], ".vscode", "extensions")
#             self._local_extensions_folder = MACOS_EXTENSIONS_FOLDER
#         elif os.name == 'posix':
#             LINUX_EXTENSIONS_FOLDER: str = os.path.join(os.environ['HOME'], ".vscode", "extensions")
#             self._local_extensions_folder = LINUX_EXTENSIONS_FOLDER
#         else:
#             print("Unsupported operating system")
#             return False

#         # Check that the folder for the local extensions exists
#         if not os.path.isdir(self._local_extensions_folder):
#             print("No local extensions folder found, aborting")
#             return False

#         # Check that there are local extensions stored in the local extensions folder
#         local_extensions = os.listdir(self._local_extensions_folder)
#         if local_extensions == []:
#             print("No local extensions found, aborting")
#             return False
        
#         print(local_extensions)
#         return True
            
#     def save_profile(self):
#         kept_settings = {key: self.settings[key] for key, var in self.setting_vars.items() if var.get()}
#         kept_extensions = [ext for ext in self.extensions if self.extension_vars[ext['identifier']['id']].get()]
#         kept_globalstate = {key: self.globalstate[key] for key, var in self.globalstate_vars.items() if var.get()}
#         update_profile(self.profile, kept_settings, kept_extensions, kept_globalstate)

#         filename = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])
#         if filename:
#             self._save_profile(self.profile, filename)
#             messagebox.showinfo("Success", "Profile saved successfully!")
#             self.changes_made = False

#     def _save_profile(self, profile, filename):
#         with open(filename, 'w') as json_file:
#             json.dump(profile, json_file, indent=2)


class IVSCodeProfileProcessor(ABC):
    @abstractmethod
    def get_vscodeprofile_object_from_file_data(self) -> VSCodeProfile:
        """Generate the VSCodeProfile object from the file data"""
        pass


class VSCodeProfileProcessor(IVSCodeProfileProcessor):
    _profile_data: str
    _settings_dict: dict

    def __init__(self, profile_data: str):
        self._profile_data = profile_data

    def get_vscodeprofile_object_from_file_data(self) -> VSCodeProfile:
        self._extract_settings()
        #FIXME
        return VSCodeProfile()
        pass

    def _extract_settings(self):
        self._settings_dict = json.loads(self._profile_data['settings'])
        # return json.loads(settings_dict["settings"])

    def extract_extensions(profile):
        return json.loads(profile['extensions'])

    def extract_globalstate(profile):
        globalstate = json.loads(profile['globalState'])
        return globalstate['storage']




def update_profile(profile, settings, extensions, globalstate):
    settings_dict = json.loads(profile['settings'])
    settings_dict["settings"] = json.dumps(settings)
    profile['settings'] = json.dumps(settings_dict)
    profile['extensions'] = json.dumps(extensions)
    globalstate_dict = json.loads(profile['globalState'])
    globalstate_dict['storage'] = globalstate
    profile['globalState'] = json.dumps(globalstate_dict)



            

class ProfileEditor:
    def __init__(self, master):
        self.master = master
        self.master.title("VSCode Profile Editor")
        self.master.geometry("800x600")

        self.profile = None
        self.settings = None
        self.extensions = None
        self.globalstate = None
        self.setting_vars = {}
        self.extension_vars = {}
        self.globalstate_vars = {}
        self.changes_made = False

        self.create_widgets()

    def create_widgets(self):
        self.load_button = ttk.Button(self.master, text="Load Profile", command=self.load_profile)
        self.load_button.pack(pady=10)

        self.notebook = ttk.Notebook(self.master)
        self.notebook.pack(expand=True, fill='both')

        self.settings_frame = ttk.Frame(self.notebook)
        self.extensions_frame = ttk.Frame(self.notebook)
        self.globalstate_frame = ttk.Frame(self.notebook)

        self.notebook.add(self.settings_frame, text='Settings')
        self.notebook.add(self.extensions_frame, text='Extensions')
        self.notebook.add(self.globalstate_frame, text='Global State')

        for frame in (self.settings_frame, self.extensions_frame, self.globalstate_frame):
            self.create_scrollable_frame(frame)

        button_frame = ttk.Frame(self.master)
        button_frame.pack(pady=10)

        self.save_button = ttk.Button(button_frame, text="Save Profile", command=self.save_profile)
        self.save_button.pack(side='left', padx=5)
        self.save_button.config(state='disabled')

        self.quit_button = ttk.Button(button_frame, text="Quit", command=self.quit_app)
        self.quit_button.pack(side='left', padx=5)

    def create_scrollable_frame(self, parent):
        canvas = tk.Canvas(parent)
        scrollbar = ttk.Scrollbar(parent, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        return scrollable_frame

    def create_checkbox(self, parent, text, var):
        cb = ttk.Checkbutton(parent, text=text, variable=var, command=self.on_checkbox_change)
        cb.pack(anchor='w')

    def on_checkbox_change(self):
        self.changes_made = True



    def display_settings(self):
        scrollable_frame = self.settings_frame.winfo_children()[0].winfo_children()[0]
        for widget in scrollable_frame.winfo_children():
            widget.destroy()

        for key in self.settings:
            var = tk.BooleanVar(value=True)
            self.setting_vars[key] = var
            self.create_checkbox(scrollable_frame, key, var)

    def display_extensions(self):
        scrollable_frame = self.extensions_frame.winfo_children()[0].winfo_children()[0]
        for widget in scrollable_frame.winfo_children():
            widget.destroy()

        for ext in self.extensions:
            var = tk.BooleanVar(value=True)
            self.extension_vars[ext['identifier']['id']] = var
            # self.create_checkbox(scrollable_frame, ext['identifier']['id'], var, text=ext['displayName'])
            self.create_checkbox(scrollable_frame, ext['displayName'], var)

    def display_globalstate(self):
        scrollable_frame = self.globalstate_frame.winfo_children()[0].winfo_children()[0]
        for widget in scrollable_frame.winfo_children():
            widget.destroy()

        for key, value in self.globalstate.items():
            var = tk.BooleanVar(value=True)
            self.globalstate_vars[key] = var
            label_text = f"{key}: {value}"
            self.create_checkbox(scrollable_frame, label_text, var)

    def save_profile(self):
        kept_settings = {key: self.settings[key] for key, var in self.setting_vars.items() if var.get()}
        kept_extensions = [ext for ext in self.extensions if self.extension_vars[ext['identifier']['id']].get()]
        kept_globalstate = {key: self.globalstate[key] for key, var in self.globalstate_vars.items() if var.get()}
        update_profile(self.profile, kept_settings, kept_extensions, kept_globalstate)

        filename = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])
        if filename:
            self._save_profile(self.profile, filename)
            messagebox.showinfo("Success", "Profile saved successfully!")
            self.changes_made = False

    def quit_app(self):
        if self.changes_made:
            if messagebox.askyesno("Save Changes", "Do you want to save your changes before quitting?"):
                self.save_profile()
        self.master.quit()

def main():
    root = tk.Tk()
    app = ProfileEditor(root)
    root.mainloop()

if __name__ == "__main__":
    main()
