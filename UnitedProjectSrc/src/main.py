import pdb

import os
import csv
import logging
import logging.handlers
from input import get_all_available_flights, filter_flight_list

logger = logging.getLogger(__name__) 

CURRENT_FLIE_PATH = os.path.dirname(os.path.realpath(__name__))
CSV_PATH = os.path.join(CURRENT_FLIE_PATH, os.path.pardir, os.path.pardir,
                        'CSV_OUTPUT_FOLDER', 'out.csv')

def main():
    MIN_FLIGHT_NUM = 0 
    MAX_FLIGHT_NUM = 2000
    REMOVE_DUPLICATES = True
    USE_NEW_PDF = False
    PAGE_START = 109

    assert MIN_FLIGHT_NUM < MAX_FLIGHT_NUM, 'Min flight number must be less than max!'

    conf_log()
    all_flights = get_all_available_flights(PAGE_START, USE_NEW_PDF)

    filtered_flights = filter_flight_list(all_flights, REMOVE_DUPLICATES, 
                                          (MIN_FLIGHT_NUM, MAX_FLIGHT_NUM))

    pdb.set_trace()
    create_flight_csv(filtered_flights, CSV_PATH)


def create_flight_csv(flight_list, csv_path):

    with open(csv_path, 'w') as f:
        writer = csv.writer(f)
        for flight in flight_list:
            formatted_flight = flight.format_for_csv()
            writer.writerow(formatted_flight)


def conf_log():
    LOG_PATH = os.path.join(CURRENT_FLIE_PATH, 'log', 'UNITED_MASTER.log')
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    #Handler
    my_handler = logging.handlers.RotatingFileHandler(LOG_PATH, maxBytes=1000, backupCount=5)

    # Formatter
    formatter = logging.Formatter('%(asctime)s %(levelname)-8s [%(name)s] %(message)s')

    my_handler.setFormatter(formatter)

    logger.addHandler(my_handler)

if __name__ == "__main__":
    main()


