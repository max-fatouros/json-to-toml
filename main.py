import json
import os.path
import tomli

# For file explorer
from tkinter import Tk
from tkinter.filedialog import askopenfilenames


def traverse(dictionary: dict, out_file, indent_spaces=4, depth=0,
             comment_notes=True, comment_nulls=True, parent_keys=""):
    """
    Recursively traverses dictionary and outputs a TOML file of its contents.
    
    :param dictionary: Dictionary to be converted to TOML format.
    :param out_file: TOML output file (Actual file, not just filename. Must open beforehand).
    :param indent_spaces: number of spaces for TOML indentation
    :param comment_nulls: Replace null-types with TOML comments
    :param comment_notes: Replace keys named "note" with comments placed before table taken from that keys value.
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

            if comment_notes and 'note' in (key.lower() for key in sub_dict):
                out_file.write(depth * " " * indent_spaces)
                out_file.write(f"# {sub_dict['Note']}\n")
                del sub_dict['Note']

            # Prepends all parent key values to a sub-key string.
            key = f"{parent_keys}{key}"
            out_file.write(depth * " " * indent_spaces)
            out_file.write(f"[{key}]\n")

            traverse(sub_dict, out_file, indent_spaces=indent_spaces, depth=depth + 1,
                     comment_notes=comment_notes, comment_nulls=comment_nulls, parent_keys=f"{key}.")

        else:
            value = dictionary[key]
            if type(value) is str:
                value = f'"{value}"'

            elif type(value) is bool:
                # toml only supports lower case booleans
                value = str(value).lower()

            elif value is None:
                if comment_nulls:
                    out_file.write((depth - 1) * " " * indent_spaces)
                    out_file.write(f"# {key}\n")

                continue

            out_file.write((depth - 1) * " " * indent_spaces)
            out_file.write(f"{key} = {value}\n")

            if index == len(dictionary) - 1:
                out_file.write("\n")

            elif type(dictionary[ordered_keys[index + 1]]) is dict:
                # if the next value is a dictionary, print a newline.
                out_file.write("\n")


Tk().withdraw()  # Suppresses unnecessary window
filenames_in = askopenfilenames()  # Opens window to choose JSON files, can choose multiple files.

for filename_in in filenames_in:
    filename_out = os.path.splitext(filename_in)[0] + ".toml"

    with open(filename_in, encoding='utf-8') as file:
        jDict = json.load(file)

    with open(filename_out, "w", encoding='utf-8') as file:
        # file.write(tomli.dumps(jDict))
        traverse(jDict, file, indent_spaces=4)

    with open(filename_out, 'rb') as f:
        # Just checking to make sure it can be read after conversion
        try:
            tDict = tomli.load(f)
            print(f"Success reading {filename_out} as dictionary")
        except tomli.TOMLDecodeError as e:
            print(f"Error reading {filename_out} as dictionary")
            print(e)

# TODO: Compare dictionaries after processing.
#  Need to implement comparison while taking into account that JSON supports null-types, while TOML does not.
# if jDict == tDict:
#     print("\u001b[32m", "Success!", "\u001b[0m")
# else:
#     print("\u001b[31m", "Failed to convert JSON to TOML", "\u001b[0m")

# print(json.dumps(jDict, indent=4))
# print(json.dumps(tDict, indent=4))
