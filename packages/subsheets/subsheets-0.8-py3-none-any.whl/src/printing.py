from colorama import Fore, Style
from .constants import ProjInfo


def print_version_info(cli=True):
    """
    Formats version differently for CLI and splash screen.
    """
    version = "v{} by {} (@{})".format(ProjInfo.VERSION,
                                       ProjInfo.AUTHOR_FULL_NAME,
                                       ProjInfo.AUTHOR_GITHUB)
    if not cli:
        print(Fore.RED + Style.BRIGHT + "\t{}\n".format(version) + Style.RESET_ALL)
    else:
        print(version)


def splash_screen():
    """
    Display splash graphic, and then stylized version and author info.
    """
    print(Fore.YELLOW + Style.BRIGHT + "\n" + ProjInfo.LOGO + Style.RESET_ALL)
    print_version_info(False)