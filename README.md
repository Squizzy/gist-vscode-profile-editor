"# gist-vscode-profile-editor"  
https://github.com/Squizzy/gist-vscode-profile-editor

# Version history
- 0.1: First working app, not extensively tested.

# What is it?
## A tool to edit/cleanup the vscode profile in a github gist when multiple vscode profiles were created from a clogged up Default profile.

This happens when you start programming and have no idea about profiles at first, you load as many extensions as you need to play with multiple languages, have multiple settings, and all get messy.  

Then you discover VSCode profiles and how you can save then in github gists, and have one for Python, one for C, one for Java, etc... depending on your preferences. But these are generally created from the Default profile and a lot of cruft remains.

This app allows you to clean each profile individually.

# How to use? - step by step
- Go to ```gist.github.com``` and log on with your github account.
    - find the gist profile content for the profile you want to clean up.
    - copy the content into a local text file.
    - Save the file (eg: \<name\>.json (extension .json is not necessary but it is a json content))  

- Run the gist-vscode-profile-editor.py (Needs python3):
    - ```python3 gist-vscode-profile-editor.py```

- Follow the logic of the app:
    - Click "load profile" button and select the \<name\>.json file you just created
    - Deselect the items which you know for sure are not related to the programming language profile you are targeting
    - Select "save profile" 
    - Choose a filename for your saved profile (eg \<name\>-updated.json) to be saved locally
    - Close the application   

- Update the github gist:
    - Copy and paste the textual content of \<name\>-updated.json  
       - __IMPORTANT: Copy the content inside, after opening the file with a text editor, not the file itself or the filename!__
    - In gist.github.com:
        - go back to the gist you are updating
        - click the "edit" button on the top right
        - overwrite the content with that from <name>-updated.json.  

# IMPORTANT NOTES:
- Use at your own risk
    - No guarantee it will work properly, it's only been tested on Windows but should run on MacOS and Linux just as well
- Made for python3
    - However, no particular non-standard modules needed (using json and tkinter modules only)
- Application was entirely made using Cursor and Claude-3.5-Sonnet AI, free version
    - Development stopped when no more token were available
    - Almost all code provided b Claude-AI
- GistPad seems to be a convenient VSCode/Cursor extension for editing gists without having to go into gist.github.com
    - Can be helpful here but not essential. 
    - Was used at the time of putting this code together

# Improvements to this app:
- Leave comments under issues, and this can be considered for improvements in the future.
    - ```https://github.com/Squizzy/gist-vscode-profile-editor/issues```
    - This includes comments on the README.md
- Feel free to fork (Leave original attribution but modify at will)
- There is tons of potential improvements possible, and testing.
    - if some testing has been done, then please report under issue and I'll add into comments