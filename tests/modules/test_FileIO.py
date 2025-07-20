import pytest
from src.modules.FileIO import FileIO
import sys

fileIO = FileIO()

def test_get_vscode_registered_vscode_profiles():
    assert (fileIO._get_vscode_registered_vscode_profiles()) == True

def test_get_vscode_local_profiles_folder_names():
    assert(fileIO._get_vscode_local_profiles_folder_names()) == False

def test_get_vscode_registered_vscode_profiles():
    assert(fileIO._get_vscode_registered_vscode_profiles()) == True

def test_get_vscode_profile_filename_from_command_line():
    assert(fileIO._get_vscode_profile_filename_from_command_line(["", "-f", "/home"])) == True
    assert(fileIO._get_vscode_profile_filename_from_command_line(["", "-f", ""])) == False
    assert(fileIO._get_vscode_profile_filename_from_command_line(["", "-f"])) == False
    assert(fileIO._get_vscode_profile_filename_from_command_line([""])) == False