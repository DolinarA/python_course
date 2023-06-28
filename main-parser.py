"""
A tool for parsing and merging multiple files from user-specified directory.

usage: python main-parser.py --input-path=<input_path> --output-path=<output_path> --remove-empty-lines

Options: --input-path=<input_path>      Path to folder with files to merge. Glob pattern is supported for file names.
                                        Example: data/2023* (reads all files that start with 2023)
         --output-path=<output_path>    Path to output file (optional). Default: merged.txt
         --remove-empty-lines           Remove empty lines from merged file (optional). Default: False.
"""

# imports
import fnmatch  # string filtering using syntax
import os  # for interacting with the operating system and file paths, built-in module
import sys

from modules.file_helpers import validate_folder_path


# functions
def parse_arguments_input_path(arguments: list[str]) -> str:
    """
    Parses input path from command-line arguments.
    If not specified in arguments, asks user for input.
    """
    for argument in arguments:
        if argument.startswith("--input-path="):
            input_path = argument.split("--input-path=")[1]
            return input_path

    print("Argument --input-path= not provided. Please use it.")
    path = input("Enter input path: ")
    return path


def parse_arguments_output_path(arguments: list[str]) -> str:
    """
    Parses output path from command-line arguments.
    If not specified, uses the default value.
    """
    for argument in arguments:
        if argument.startswith("--output-path="):
            output_path = argument.split("--output-path=")[1]
            return output_path

    print(
        "Argument --output-path= not provided. Default value will be used (merged.txt)."
    )
    return "merged.txt"


def parse_arguments_remove_empty_lines(arguments: list[str]) -> bool:
    """
    Parses remove empty lines from arguments.
    If not specified, uses the default value
    """
    for argument in arguments:
        if argument == "--remove-empty-lines":
            return True
    return False  # if argument not specified, returns False


def get_absolute_file_paths(folder_name: str, filter: str = "*") -> list[str]:
    """Reads names of files in a folder and returns a list of files."""
    # filter default: * - all files (defined in function arguments)
    absolute_paths = []
    for dirpath, _, filenames in os.walk(folder_name):
        for filename in filenames:
            if fnmatch.fnmatch(filename, filter):
                absolute_path = os.path.abspath(os.path.join(dirpath, filename))
                absolute_paths.append(absolute_path)
    return absolute_paths


def read_text_file_to_list(file_path: str) -> list[str]:
    with open(file_path, "r") as file:
        file_data = file.readlines()
    return file_data


def strip_new_line_characters(file_data: list[str]) -> list[str]:
    return [line.strip() for line in file_data]


def remove_empty_lines_from_list(file_data: list[str]) -> list[str]:
    return [line for line in file_data if line != ""]


def write_list_to_text_file(file_data: list[str], file_path: str) -> None:
    with open(file_path, "w") as file:
        for line in file_data:
            file.write(line + "\n")


def split_input_path(input_path: str) -> tuple[str, str]:
    """Splits input path into folder path and filter."""
    # input: data/file*
    # output: (data, file*)
    dir_name, file_name = os.path.split(input_path)
    if not os.path.exists(dir_name):
        print(f"Directory {dir_name} does not exist. Exiting ...")
        sys.exit(1)
    return dir_name, file_name


def main():
    # parse arguments
    input_path = parse_arguments_input_path(sys.argv)
    output_path = parse_arguments_output_path(sys.argv)
    validate_folder_path(output_path)
    remove_empty_lines = parse_arguments_remove_empty_lines(sys.argv)
    data_folder_name, filter_file_name = split_input_path(input_path)

    # Read files
    all_file_paths = get_absolute_file_paths(
        folder_name=data_folder_name, filter=filter_file_name
    )

    merged_list = []
    for path in all_file_paths:
        file_data = read_text_file_to_list(path)
        merged_list += file_data

    # Remove new line characters
    merged_list = strip_new_line_characters(merged_list)

    # Remove empty lines
    if remove_empty_lines:
        merged_list = remove_empty_lines_from_list(merged_list)

    # Write to file
    write_list_to_text_file(file_path=output_path, file_data=merged_list)

    print("Done!")


if __name__ == "__main__":
    print("Start ...")
    main()
