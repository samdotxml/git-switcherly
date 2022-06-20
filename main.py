#!/usr/bin/env python3
"""
Description:
This is a simple program that allows you to switch users in git very easily.
The switching is done by editing the ~/.ssh/config file and simply changing the rsa key path
The program has a small interactive command line interface

Command: python3 main.py

Author: samdotxml @github
License: MIT
"""
import sys
from lib.core import *
from lib.case import *
from lib.sshEditor import *
from lib.prompts import *

def main():
    """ Main entry point of the app """
    if(not folder_exist()):
        print("Failed to find ~/.ssh folder. Can't continue")
        sys.exit()

    while(True):
        selection = menu_select()
        while switch(selection):
            if case("Create Identity"):
                details = create_identity_prompt()
                create_keys(details)
                if not check_file_existence(details["githubName"]):
                    print("The SSH Keys were not saved to ~/.ssh folder. Ending script")
                    sys.exit()
                print("\n[Success] Created SSH Keys")
                print("[Information] Make sure to change your identity\n")
                break
            if case("Change Identity"):
                profiles = get_profiles()
                if(len(profiles) == 0):
                    print("No accounts in your config")
                    break
                selected_username = select_identity_prompt(profiles)
                print("\nYou selected {uname}".format(uname=selected_username))
                
                print("Editing ssh configuration file")
                cfg_path = get_folder() + "/config"
                change_host(cfg_path, selected_username)
                
                print("Changing git global config (set username and email)")
                email = get_email(selected_username)
                edit_git_globaconfig(selected_username, email)

                print("Done!")
                break
            if case("Exit"):
                print("Goodbye!")
                sys.exit()


if __name__ == "__main__":
    main()
