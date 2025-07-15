import logging


class bcolors:
    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKCYAN = "\033[96m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"


def print_warning(message):
    """
    Print a warning message in yellow.
    """
    logging.warning(f"{bcolors.WARNING}⚠️ WARNING: {message}{bcolors.ENDC}")


def print_section_start(section_name):
    """
    Print a section start message in bold.
    """
    logging.info(f"{bcolors.BOLD}--- {section_name} ---{bcolors.ENDC}")


def print_section_end(section_name):
    """
    Print a section end message in bold.
    """
    logging.info(f"{bcolors.BOLD}--- End of {section_name} ---{bcolors.ENDC}")
