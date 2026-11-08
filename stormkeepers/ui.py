"""Terminal colors and validated input."""
from colorama import Fore, Style, just_fix_windows_console
just_fix_windows_console()
COLORS = {'info': Fore.CYAN, 'good': Fore.GREEN, 'bad': Fore.RED, 'gold': Fore.YELLOW}

def say(message, kind='info'):
    print(COLORS.get(kind, Fore.WHITE) + str(message) + Style.RESET_ALL)

def choose(prompt, choices):
    while True:
        answer = input(prompt).strip().lower()
        if answer in choices:
            return answer
        say('Choose: ' + ', '.join(choices), 'bad')
