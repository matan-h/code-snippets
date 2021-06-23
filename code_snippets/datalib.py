import json
from os import path

data_file = 'answers.json'


def get_data():
    if path.exists(data_file):
        return json.load(open(data_file, 'r'))
    else:
        return {}


def write_data(data):
    with open(data_file, 'w') as data_io:
        json.dump(data, data_io)


if __name__ == '__main__':
    write_data(get_data()) # create the file
