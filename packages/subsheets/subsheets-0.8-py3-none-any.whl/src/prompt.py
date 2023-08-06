import sys

import inquirer
from colorama import Fore, Style


def main_menu_prompt():
    """
    Prompt user for an action
    """
    questions = [
        inquirer.List('choice',
            message=Fore.GREEN + Style.BRIGHT + "What would you like to do?" + Fore.BLUE,
            choices=[
                '1. Excels to subsheets',
                '2. Subsheets in a excel to excels'
            ],
        ),
    ]
    answers = inquirer.prompt(questions)
    if answers:
        return answers.get('choice').strip().lower()
    else:
        sys.exit(1)