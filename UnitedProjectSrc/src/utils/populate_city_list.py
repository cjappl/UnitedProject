import os
import re

FIND_CODE_REGEX = re.compile(r"\(([A-Z]{3})")
CURRENT_FILE_PATH = os.path.dirname(os.path.realpath(__file__))
OUTPUT_FILE_PATH = os.path.join(CURRENT_FILE_PATH, os.path.pardir, 'obj', 'valid_flight_codes.txt')

def populate_city_list():
    with open("dest_by_city.txt", 'r') as f:
        full_city_list = f.read()

    airport_codes = re.findall(FIND_CODE_REGEX, full_city_list)

    with open(OUTPUT_FILE_PATH, 'w') as f:
        for code in airport_codes:
            f.write("%s\n" % code)
