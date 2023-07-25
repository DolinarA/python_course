import os
import random
import sys
import time
from typing import Union

import pdfkit
from bs4 import BeautifulSoup

BASE_TAXON_URL = "https://gd.eppo.int/taxon/"
BASE_SEARCH_URL = "https://gd.eppo.int/search?k="
# system path for wkhtmltopdf: c:/program files/wkhtmltopdf/bin
# copy to paths (Control panel – environmental variables -> path -> edit->new)
# if system path doesn't work, specify it using WKHTMLTOPDF_EXECUTABLE
# here and in functions that use convert_webpage_to_pdf function
# WKHTMLTOPDF_EXECUTABLE = r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe"


def validate_folder_path(path: str) -> None:
    if os.path.isfile(path):
        print(f"Error: {path} is a file, not a folder.")
        sys.exit(1)

    os.makedirs(path, exist_ok=True)


def convert_webpage_to_pdf(
    url: str, output_file_path: str, wkhtmltopdf_path: Union[str, None] = None
) -> None:
    try:
        pdfkit.from_url(
            url,
            output_file_path,
            verbose=True,
            # configuration=pdfkit.configuration(wkhtmltopdf=wkhtmltopdf_path),
        )
    except OSError:
        print(
            "Error: wkhtmltopdf not found. Specify the location using wkhtmltopdf_path argument."
        )


def get_taxon_code_from_url(url: str) -> list[str]:
    
    # search rezultate preprasate v html
    # request.get(url)
    # https://realpython.com/beautiful-soup-web-scraper-python/
    # beautiful soup - html parser
    # soup = BeautifulSoup(html, "html.parser")


def run_code_mode():
    code = input("Enter the code of the taxon: ")
    url = f"{BASE_TAXON_URL}{code.upper()}"
    output_file_path = f"./eppo_test/{code}.pdf"
    convert_webpage_to_pdf(
        url,
        output_file_path,
    )


def run_file_mode():
    input_file_path = input("Enter the path to the input file: ")
    output_folder_path = input("Enter the path to the output folder: ")
    validate_folder_path(output_folder_path)
    if os.path.exists(input_file_path):
        with open(input_file_path, "r") as input_file:
            for line in input_file:
                code = line.strip()
                url = f"{BASE_TAXON_URL}{code.upper()}"
                output_file_path = os.path.join(output_folder_path, f"{code}.pdf")
                convert_webpage_to_pdf(url, output_file_path)
                time.sleep(random.randint(2, 7))  # random sleep 2-7 seconds
    else:
        print("Error: input file does not exist.")


def run_search_mode():
    input_search_term = input("Enter the search term: ")
    output_folder_path = input("Enter the path to the output folder: ")
    validate_folder_path(output_folder_path)
    url = f"{BASE_SEARCH_URL}{input_search_term}"
    codes = get_taxon_code_from_url(url)
    for code in codes:
        code = code.strip()
        url = f"{BASE_TAXON_URL}{code.upper()}"
        output_file_path = os.path.join(output_folder_path, f"{code}.pdf")
        convert_webpage_to_pdf(url, output_file_path)
        time.sleep(random.randint(2, 7))


def main():
    try:
        mode = sys.argv[1]
        if mode == "code":
            run_code_mode()
        elif mode == "file":
            run_file_mode()
        elif mode == "search":
            run_search_mode()
        else:
            print(
                "Error: invalid mode specified. Please specify a valid mode (code, file, or search)."
            )

    except IndexError:
        print("Error: no mode specified. Please specify mode (code, file, or search).")


if __name__ == "__main__":
    main()
