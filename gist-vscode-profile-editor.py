""" Python application to help clean up VSCode Profiles saved in github gists"""
__author__ = "Squizzy"
__copyright__ = "Copyright 2024, Squizzy"
__credits__ = "Cursor code editor (/VSCode), Claude-AI"
__license__ = "GPL"
__version__ = "0.1"
__maintainer__ = "Squizzy"

import sys
import json
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from pydantic import BaseModel
from abc import ABC, abstractmethod

class VSCodeProfile(BaseModel):
    ...

class IFileIO(ABC):
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
    _filename: str
    _profile_data: str

    def __init__(self):
        self._filename = None
        self._profile_data = None
        pass
    

    @property
    def profile_data(self) -> str:
        return self._profile_data

    def load_vscode_profile_to_modify(self) -> bool:
        """Retrieve the content of a vscode profile file or URL
        
        returns:
            (str): the json raw data from the profile
        """

        if len(sys.argv) > 0:
            # use command line arguments
            self._filename = self._get_vscode_profile_filename_from_command_line()

        if self._filename == None:
            self._get_vscode_profile_filename_from_popup()

        if self._filename == None:
            print("No file selected, aborting.")
            return False
        
        self._load_vscode_profile_data() 
        if self._profile_data is None:
            print("No data found in the profile file, or not a proper VSCode profile file, aborting")
            return False
        
        return True

    def _get_vscode_profile_filename_from_command_line(self) -> str | None:
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
                    return
            elif filename_arg_expected:
                # TODO: need to check that arg is a file that is reachable
                return arg
            else:
                print("command line argument not recognised. ignoring it.")
        
    def _get_vscode_profile_filename_from_popup(self) -> None:
        """Use a popup to let the user select the file to process
        """
        file_path: str

        file_path = filedialog.askopenfilename(
            title="Select the VSCode profile to be processed",
            filetypes=[("JSON files", "*.json")])
        
        if file_path:
            self._filename = file_path

            # # self.profile = load_profile(filename)



            # self.settings = extract_settings(self.profile)
            # self.extensions = extract_extensions(self.profile)
            # self.globalstate = extract_globalstate(self.profile)
            # self.display_settings()
            # self.display_extensions()
            # self.display_globalstate()
            # self.save_button.config(state='normal')
            
    def _load_vscode_profile_data(self) -> None:
        """Attempt to load the data from the file selected by the user
        
        """

        MAX_FILE_SIZE: int = 100_000
        retrieved_data: str

        with open(self._filename, 'r') as vscode_profile_json_file:
            file_length = len(vscode_profile_json_file)

            if file_length > MAX_FILE_SIZE:
                load_anyway = messagebox.askyesno(title="Large file size detected", message=f"File is more than {MAX_FILE_SIZE} bytes, which seems large. \nuse anyway?")
                if load_anyway == messagebox.NO:
                    print("file too large, user aborted")
                    return
                
            retrieved_data = vscode_profile_json_file.read(file_length)
        
        try:
            self._profile_data = json.load(retrieved_data)
        except json.JSONDecodeError as e:
            # could be done more gracefully with requesting another file
            print(f"Problem with file {self._filename}: Not a proper VSCode Profile file (json format expected), aborting")
            self._profile_data = None
            return
    
            # return json.load(json_file)
            # return json_file
        
    def save_profile(self):
        kept_settings = {key: self.settings[key] for key, var in self.setting_vars.items() if var.get()}
        kept_extensions = [ext for ext in self.extensions if self.extension_vars[ext['identifier']['id']].get()]
        kept_globalstate = {key: self.globalstate[key] for key, var in self.globalstate_vars.items() if var.get()}
        update_profile(self.profile, kept_settings, kept_extensions, kept_globalstate)

        filename = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])
        if filename:
            save_profile(self.profile, filename)
            messagebox.showinfo("Success", "Profile saved successfully!")
            self.changes_made = False

    def save_profile(self, profile, filename):
        with open(filename, 'w') as json_file:
            json.dump(profile, json_file, indent=2)


class IVSCodeProfileProcessor(ABC):
    @abstractmethod
    def get_vscodeprofile_object_from_file_data(self) -> VSCodeProfile:
        """Generate the VSCodeProfile object from the file data"""
        pass


class VSCodeProfileProcessor(IVSCodeProfileProcessor):
    _profile_data: str
    _settings_dict: Any

    def __init__(self, profile_data: str):
        self._profile_data = profile_data

    def get_vscodeprofile_object_from_file_data(self) -> VSCodeProfile:
        self._extract_settings()
        pass

    def _extract_settings():
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
            save_profile(self.profile, filename)
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
