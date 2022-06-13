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
from core import *
from case import *
from sshEditor import *
from sys import platform
import inquirer

def menuSelect():
    questions = [
    inquirer.List('selection',
                    message="What size do you need?",
                    choices=['Create Identity', 'Change Identity', 'Exit'],
                ),
            ]
    answers = inquirer.prompt(questions)
    return answers['selection']

def selectIdentity(profiles):
    choices = []
    for x in profiles:
        choices.append(x["username"])
    
    questions = [
    inquirer.List('selection',
                    message="Choose the Github Account",
                    choices=choices,
                ),
            ]
    answers = inquirer.prompt(questions)
    return answers['selection']

def createIdentity():
    questions = [
        inquirer.Text('githubName',
                    message="What's your Github username?"),
        inquirer.Text('githubEmail',
                    message="What's your e-mail address associated with {githubName}?")
                ]

    return inquirer.prompt(questions)

def executeShell():
    questions = [
        inquirer.Confirm('confirm',
                    message="Run the command manually or not?", default=True),
                ]
    
    return inquirer.prompt(questions)

def main():
    """ Main entry point of the app """
    if(not folderExist()):
        print("Failed to find ~/.ssh folder. Can't continue")
        exit()
    
    while(True):
        selection = menuSelect()
        while switch(selection):
            if case("Create Identity"):
                details = createIdentity()
                createKeys(details)
                if not checkFileExistence(details["githubName"]):
                    print("The SSH Keys were not saved to ~/.ssh folder. Ending script")
                    exit()
                print("\n[Success] Created SSH Keys")
                print("[Information] Make sure to change your identity\n")
                break
            if case("Change Identity"):
                profiles = getProfiles()
                if(len(profiles) == 0):
                    print("No accounts in your config")
                    break
                selection = selectIdentity(profiles)
                cmd = "~/.ssh/id_rsa_{uname}".format(uname=selection)
                print("\nYou selected {uname}".format(uname=selection))
                print("You need to follow these steps:")
                print("(1) If you haven't added the SSH public key to your Github account, then do it now!")
                print("(2) Now the ssh-agent on your machine needs to add the key to the credential manager, you have following options:")
                print("\t(i) Run following command: ssh-add {cmd}".format(cmd=cmd))
                print("\t(ii) Use the automated key adder (BETA)\n")
                
                if(executeShell()['confirm']):
                    if platform == "linux" or platform == "linux2":
                        os.system("eval `ssh-agent -s`")
                        os.system("ssh-add {cmd}".format(uname=selection))
                    elif platform == "win32":
                        runGitBashAgent("id_rsa_{uname}".format(uname=selection))
                    print("Done executing the commands. If it did not work, try entering the commands manually!")
                else:
                    print("Make sure to do all the steps")

                print("Editing ssh configuration file")
                cfgPath = getFolder() + "/config"
                changeHost(cfgPath, selection)
                print("Done!")
                break
            if case("Exit"):
                print("Goodbye!")
                exit()


if __name__ == "__main__":
    """ This is executed when run from the command line """
    main()