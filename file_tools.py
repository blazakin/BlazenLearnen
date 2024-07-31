# Functions for reading and writing from a text file.

import os
import json


def check_filepath(filepath):
    return os.path.isfile(filepath)


def read(file_name):
    # Reads a file to a string
    file_path = os.path.join(os.path.dirname(__file__), file_name)
    with open(file_path, "r") as file:
        text = file.read()
    return text


def read_filepath(file_path):
    # Reads a file to a string from a full file path
    with open(file_path, "r") as file:
        text = file.read()
    return text


def write(file_name, text):
    # Appends text to the end of a file
    file_path = os.path.join(os.path.dirname(__file__), file_name)
    with open(file_path, "a") as file:
        file.write(text)


def write_filepath(file_path, text):
    # Appends text to the end of a file from a full file path
    with open(file_path, "a") as file:
        file.write(text)


def overwrite(file_name, text):
    # Overwrites a file and returns what was overwritten
    file_path = os.path.join(os.path.dirname(__file__), file_name)
    with open(file_path, "r") as file:
        file_text = file.read()
    with open(file_path, "w") as file:
        file.write(text)
    return file_text


def jread(file_name):
    # Reads a json file to a dictionary
    file_path = os.path.join(os.path.dirname(__file__), file_name)
    with open(file_path, "r") as file:
        data = json.loads(file.read())
    return data


def jwrite(file_name, data):
    # Appends text to the end of a file
    file_path = os.path.join(os.path.dirname(__file__), file_name)
    with open(file_path, "a") as file:
        file.write(json.dumps(data))


def joverwrite(file_name, data):
    # Overwrites a file and returns what was overwritten
    file_path = os.path.join(os.path.dirname(__file__), file_name)
    with open(file_path, "r") as file:
        file_data = json.loads(file.read())
    with open(file_path, "w") as file:
        file.write(json.dumps(data))
    return file_data


def delete(file_name):
    # Deletes a file and returns True if succesfully deleted
    file_path = os.path.join(os.path.dirname(__file__), file_name)
    if os.path.exists(file_path):
        os.remove(file_path)
        return True
    else:
        return False
