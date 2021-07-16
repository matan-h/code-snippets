import json
from os import path
import os
import appdirs

data_file = 'answers.json'
data_folder = path.abspath(".")
try:
    open(data_file, "w").close()
except PermissionError:
    data_folder = appdirs.user_data_dir("codeSnippet")
    if not path.exists(data_folder):
        os.makedirs(data_folder)

data_file = path.join(data_folder, data_file)


def get_data() -> dict:
    """
    get json from the data file

    Returns : the json data or the {} if no data
    """
    if path.exists(data_file):
        return json.load(open(data_file, 'r'))

    return {}


def write_data(data) -> None:
    """
    write json data to the data file

    Args:
        data: json data
    """
    with open(data_file, 'w') as data_io:
        json.dump(data, data_io)


if __name__ == '__main__':
    write_data(get_data())  # create the file
