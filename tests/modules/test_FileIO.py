import pytest
from src.modules.FileIO import FileIO
import sys

fileIO = FileIO()

# TODO: Test that values are correctly loaded into fileIO object where needed

def test_get_vscode_registered_vscode_profiles():
    assert (fileIO._get_vscode_registered_vscode_profiles()) == True

def test_get_vscode_local_profiles_folder_names():
    assert(fileIO._get_vscode_local_profiles_folder_names()) == True

def test_get_vscode_registered_vscode_profiles():
    assert(fileIO._get_vscode_registered_vscode_profiles()) == True

def test_get_vscode_profile_filename_from_command_line():
    if sys.platform == "win32":
        assert(fileIO._get_vscode_profile_filename_from_command_line(["", "-f", "c:\\"])) == True
        assert(fileIO._get_vscode_profile_filename_from_command_line(["", "-f", "c:\\nonexistantfolder"])) == False
    elif sys.platform == "darwin":
        assert(fileIO._get_vscode_profile_filename_from_command_line(["", "-f", "/"])) == True
        assert(fileIO._get_vscode_profile_filename_from_command_line(["", "-f", "/nonexistantfolder"])) == False
    elif sys.platform == "linux":
        assert(fileIO._get_vscode_profile_filename_from_command_line(["", "-f", "/"])) == True
        assert(fileIO._get_vscode_profile_filename_from_command_line(["", "-f", "/nonexistantfolder"])) == False
    else:
        pass
    assert(fileIO._get_vscode_profile_filename_from_command_line(["", "-f", "/"])) == True
    assert(fileIO._get_vscode_profile_filename_from_command_line(["", "-f", ""])) == False
    assert(fileIO._get_vscode_profile_filename_from_command_line(["", "-f"])) == False
    assert(fileIO._get_vscode_profile_filename_from_command_line([""])) == False

def test_get_vscode_profile_filename_from_filedialog():
    # These tests require interaction to select a file, or cancel the selection
    # So hidden for now until a method to automate this can be implemented
    if False: 
        print("select a proper settings.json file")
        assert(fileIO._get_vscode_profile_filename_from_filedialog()) == True
        print("Cancel the operation")
        assert(fileIO._get_vscode_profile_filename_from_filedialog()) == False

def test_get_vscode_profile_from_available_local_profiles():
    # TODO: Change this once method is implemented
    assert(fileIO._get_vscode_profile_from_available_local_profiles()) == False

def test_load_vscode_profile_data():
    fileIO = None
    fileIO = FileIO()
    # When no file is set, this should fail gracefully
    assert(fileIO._load_vscode_profile_data()) == False
    
    # but work with a file presented
    fileIO._profile_to_modify_filepath = 'tests/modules/test_settings_small.json'
    assert(fileIO._load_vscode_profile_data()) == True

    # should fail with an empty file
    fileIO._profile_to_modify_filepath = 'tests/modules/test_settings_empty.json'
    assert(fileIO._load_vscode_profile_data()) == False

    # should fail with a non-compliant file
    fileIO._profile_to_modify_filepath = 'tests/modules/test_settings_non_compliant.json'
    assert(fileIO._load_vscode_profile_data()) == False

    # should ask the user if want to use a large file, and should load it if accept
    # as requires user interaction, hidden until needed
    if False:
        tmp = fileIO._max_settings_file_size
        fileIO._max_settings_file_size = 10
        fileIO._profile_to_modify_filepath = 'tests/modules/test_settings_large.json'
        assert(fileIO._load_vscode_profile_data()) == True
        fileIO._max_settings_file_size = tmp

def test_load_vscode_profile_to_modify():
    fileIO = FileIO()
    assert(fileIO.load_vscode_profile_to_modify()) == True


def test_list_gist_profiles():
    # TODO:  need to be reviewed when/if method is implemented
    pass

def test_load_gist_profile_data():
    assert(fileIO.load_gist_profile_data('')) == False
    # real key open online (https://gist.github.com/pyxelr/760dac032d0427377ecc1bb195499d9b)
    # not sure what the best key to use should be really.
    # used for test
    assert(fileIO.load_gist_profile_data('760dac032d0427377ecc1bb195499d9b')) == True


def test_get_local_extensions_list_from_json_file():
    # Assumes the json file exists!
    # There must be a way to make this more robust
    assert(fileIO._get_local_extensions_list_from_json_file()) == True

def test_get_local_extensions_list_from_folders():
    # Assumes there are extensions in the folder
    # There must be a way to make this more robust
    assert(fileIO._get_local_extensions_list_from_folders()) == True

def test_load_extensions_settings_keys():
    assert(fileIO.load_extensions_settings_keys()) == True