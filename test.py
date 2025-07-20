from modules.FileIO import FileIO

def main():
    file_io = FileIO()
    # file_io.load_vscode_profile_to_modify()
    # file_io._get_vscode_registered_vscode_profiles()
    # file_io._get_local_extensions_list_from_folders()
    # file_io._get_local_extensions_list_from_json_file()
    # file_io._get_extensions_settings_keys()
    # print(file_io.profile_data)
    # file_io.load_vscode_profile_to_modify()
    # print(file_io.profile_data)
    # file_io._list_gist_profiles()
    file_io.load_gist_profile_data("<some existing GITHUB gist key>")

if __name__ == "__main__":
    main()
