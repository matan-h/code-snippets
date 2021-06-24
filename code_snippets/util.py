import json
import os
import importlib

import subprocess
import sys

import howdoi.howdoi as howdoi_base
from outdated import check_outdated
import PySimpleGUI as sg


def howdoi(query: str, num_answers: int = 1, search_engine='duckduckgo', all_answer: bool = True) -> dict:
    """
    send howdoi query

    Args:
        query: string for search
        num_answers: numbers of answers
        search_engine: search_engine name - (google,bing,...)
        all_answer: if False - only the code will be returned

    Returns:json output from howdoi

    """
    importlib.reload(howdoi_base)
    if search_engine != 'google':
        os.environ['HOWDOI_SEARCH_ENGINE'] = search_engine
    query = {
        'query': [query],
        'num_answers': num_answers,
        'all': all_answer,
        'json_output': True,
        'search_engine': search_engine,
        # default arguments:
        'explain': True,
        'pos': 1,
        'link': False,
        'color': False,
        'save': False,
        'remove': False,
    }
    try:
        result = howdoi_base.howdoi(query)
    except (howdoi_base.BlockError, howdoi_base.GoogleValidationError, howdoi_base.BingValidationError,
            howdoi_base.DDGValidationError) as e:
        result = {'error': str(e)}
    else:
        try:
            result = json.loads(result)
        except json.JSONDecodeError:
            return {'error': result}  # (Sorry, couldn't find any help with that topic)
    return result


def check_for_howdoi_update():
    """check if this is the last version of howdoi"""
    is_outdated, latest_version = check_outdated("howdoi", howdoi_base.__version__)
    if is_outdated:
        if sg.popup_ok_cancel(
                f"do you want to install a new version of howdoi library ({howdoi_base.__version__} -> {latest_version}). the search may don't work on outdated version",
                title="new version of howdoi") == "OK":
            subprocess.check_call([sys.executable, "-m", "pip", "install", "-U", "howdoi"])
