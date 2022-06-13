import inquirer
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
