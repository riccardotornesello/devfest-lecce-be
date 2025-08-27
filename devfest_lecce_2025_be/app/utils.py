import logging

import cachecontrol
import google.auth.transport.requests
import requests
from google.oauth2 import id_token

session = requests.session()
cached_session = cachecontrol.CacheControl(session)
request = google.auth.transport.requests.Request(session=cached_session)


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


def print_error(message):
    """
    Print an error message in red.
    """
    logging.error(f"{bcolors.FAIL}❌ ERROR: {message}{bcolors.ENDC}")


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


def verify_firebase_token(id_token_str):
    # TODO: variable client ids

    FIREBASE_CLIENT_IDS = [
        "514905954124-olcp9abhdkpugliopm5iu4r5q1uiicsr.apps.googleusercontent.com",
        "514905954124-99f3ds205d38s8v603hv3bn9agjiheo7.apps.googleusercontent.com",
    ]

    try:
        decoded = id_token.verify_oauth2_token(
            id_token_str, request, audience=FIREBASE_CLIENT_IDS
        )
        return decoded["sub"]
    except Exception as e:
        print_error(f"Error during authentication: {e}")
        return None
