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
import inquirer
from lib.core import *
from lib.case import *
from lib.sshEditor import *

def menu_select():
    questions = [
    inquirer.List('selection',
                    message="What size do you need?",
                    choices=['Create Identity', 'Change Identity', 'Exit'],
                ),
            ]
    answers = inquirer.prompt(questions)
    return answers['selection']

def select_identity_prompt(profiles):
    choices = []
    for profile in profiles:
        choices.append(profile["username"])

    questions = [
    inquirer.List('selection',
                    message="Choose the Github Account",
                    choices=choices,
                ),
            ]
    answers = inquirer.prompt(questions)
    return answers['selection']

def create_identity_prompt():
    questions = [
        inquirer.Text('githubName',
                    message="What's your Github username?"),
        inquirer.Text('githubEmail',
                    message="What's your e-mail address associated with {githubName}?")
                ]

    return inquirer.prompt(questions)

def execute_shell_prompt():
    questions = [
        inquirer.Confirm('confirm',
                    message="Run the command manually or not?", default=True),
                ]

    return inquirer.prompt(questions)

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
                selection = select_identity_prompt(profiles)
                cmd = "~/.ssh/id_rsa_{uname}".format(uname=selection)
                print("\nYou selected {uname}".format(uname=selection))
                print("You need to follow these steps:")
                print("(1) If you haven't added the SSH public key to your Github account, then do it now!")
                print("(2) Now the ssh-agent on your machine needs to add the key to the credential manager, you have following options:")
                print("\t(i) Run following command: ssh-add {cmd}".format(cmd=cmd))
                print("\t(ii) Use the automated key adder (BETA)\n")

                if(execute_shell_prompt()['confirm']):
                    if sys.platform in (('linux', 'linux2')):
                        os.system("eval `ssh-agent -s`")
                        os.system("ssh-add {cmd}".format(cmd=selection))
                    elif sys.platform == "win32":
                        run_git_bash_agent("id_rsa_{uname}".format(uname=selection))
                    print("Done executing the commands. If it did not work, try entering the commands manually!")
                else:
                    print("Make sure to do all the steps")

                print("Editing ssh configuration file")
                cfg_path = get_folder() + "/config"
                changeHost(cfg_path, selection)
                print("Done!")
                break
            if case("Exit"):
                print("Goodbye!")
                sys.exit()


if __name__ == "__main__":
    main()
