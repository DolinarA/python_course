import os


def validate_folder_path(path: str) -> None:
    dir_name, file_name = os.path.split(path)
    if not os.path.exists(dir_name):
        print(f"Directory {dir_name} does not exist. Creating it.")
        os.makedirs(dir_name)
