import json
from os import path

data_file = 'answers.json'


def get_data() -> dict:
    """
    get json from the data file

    Returns: the json data or the {} if no data
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
