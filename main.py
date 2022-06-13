import json
import os.path
import toml
from tkinter import Tk  # from tkinter import Tk for Python 3.x
from tkinter.filedialog import askopenfilenames

from toml.decoder import TomlDecodeError


def traverse(dictionary: dict, out_file, indent_spaces=4, parent_keys="", depth=0):
    """
    Traverses dictionary and outputs a TOML file of its contents.
    :param dictionary: Dictionary to be converted to TOML format.
    :param out_file: TOML output file (Actual file, not just filename. Must open beforehand).
    :param indent_spaces: number of spaces for TOML indentation
    """
    dicts = []
    keys = []
    for key, value in dictionary.items():
        if type(value) is dict:
            dicts.append(key)
        else:
            keys.append(key)

    ordered_keys = keys + dicts

    for index, key in enumerate(ordered_keys):
        if type(dictionary[key]) is dict:
            sub_dict = dictionary[key]

            if 'Note' in sub_dict:
                out_file.write(depth * " " * indent_spaces)
                out_file.write(f"# {sub_dict['Note']}\n")
                del sub_dict['Note']

            # Prepends all parent key values to a sub-key string.
            key = f"{parent_keys}{key}"
            out_file.write(depth * " " * indent_spaces)
            out_file.write(f"[{key}]\n")
            traverse(sub_dict, out_file, indent_spaces=indent_spaces, parent_keys=f"{key}.", depth=depth + 1)

        else:
            value = dictionary[key]
            if type(value) is str:
                value = f'"{value}"'
            if type(value) is bool:
                value = str(value).lower()
            if value is None:
                # Skips writing "None" to TOML, as TOML does not support null types.
                # The best alternative I could find was simply to not include them in the output.
                continue

            out_file.write((depth - 1) * " " * indent_spaces)
            out_file.write(f"{key} = {value}\n")

            if index == len(dictionary) - 1:
                out_file.write("\n")

            elif type(dictionary[ordered_keys[index + 1]]) is dict:
                # if the next value is a dictionary, print a newline.
                out_file.write("\n")


Tk().withdraw()  # Suppresses unnecessary window
filenames_in = askopenfilenames()

for filename_in in filenames_in:
    filename_out = os.path.splitext(filename_in)[0] + ".toml"

    with open(filename_in, encoding='utf-8') as file:
        jDict = json.load(file)

    with open(filename_out, "w", encoding='utf-8') as file:
        # file.write(toml.dumps(jDict))
        traverse(jDict, file, indent_spaces=4)

    with open(filename_out, encoding='utf-8') as f:
        # Just checking to make sure it can be read
        try:
            tDict = toml.load(f)
            print(f"Success reading {filename_out}")
        except TomlDecodeError as e:
            print(f"Error reading {filename_out}")
            print(e)

# TODO: Compare dictionaries after processing.
#  Need to implement comparison while taking into account that JSON supports "null", while TOML does not.
# if jDict == tDict:
#     print("\u001b[32m", "Success!", "\u001b[0m")
# else:
#     print("\u001b[31m", "Failed to convert JSON to TOML", "\u001b[0m")

# print(json.dumps(jDict, indent=4))
# print(json.dumps(tDict, indent=4))
