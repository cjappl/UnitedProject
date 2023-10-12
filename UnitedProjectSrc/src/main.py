import os
import csv
import logging
import logging.handlers
import json
from input import get_flights_csv, filter_flight_list, get_flights_pdf

logger = logging.getLogger(__name__)

CURRENT_FLIE_PATH = os.path.dirname(os.path.realpath(__name__))
CSV_PATH = os.path.join(CURRENT_FLIE_PATH, os.path.pardir, os.path.pardir,
                        'CSV_OUTPUT_FOLDER', 'EZStandby.csv')


def main():
    MIN_FLIGHT_NUM = 0
    MAX_FLIGHT_NUM = 7000
    REMOVE_DUPLICATES = False
    USE_NEW_PDF = True
    START_PAGE = 106
    pdf_in = False
    csv_in = True
    filter_continents = False

    csv_file = os.path.join(CURRENT_FLIE_PATH, os.path.pardir, os.path.pardir,
                            'PDF_INPUT_FOLDER', 'Widebody.csv')

    assert MIN_FLIGHT_NUM < MAX_FLIGHT_NUM, 'Min flight number must be less than max!'

    print 'Getting all available flights! This may take a little...'
    if pdf_in:
        all_flights = get_flights_pdf(START_PAGE, USE_NEW_PDF)
    elif csv_in:
        all_flights = get_flights_csv(csv_file)
    else:
        assert False

    print 'Filtering flights!'
    filtered_flights = filter_flight_list(all_flights, REMOVE_DUPLICATES,
                                          (MIN_FLIGHT_NUM, MAX_FLIGHT_NUM))

    print 'Initializing continent fields!'
    JSON_PATH = os.path.join(CURRENT_FLIE_PATH, 'obj', 'airports.json')
    with open(JSON_PATH, 'r') as f:
        airport_db = json.load(f)

    for flight in filtered_flights:
        flight.origin.init_continent(airport_db)
        flight.destination.init_continent(airport_db)
        flight.origin.init_country(airport_db)
        flight.destination.init_country(airport_db)
        if csv_in:
            flight.origin.init_location(airport_db)
            flight.destination.init_location(airport_db)

    if filter_continents:
        cont_filt_flights = []
        for flight in filtered_flights:
            if flight.origin.continent == 'NA' and flight.destination.continent == 'EU':
                cont_filt_flights.append(flight)

    print 'Outputting CSV file!'
    create_flight_csv(filtered_flights, CSV_PATH)


def create_flight_csv(flight_list, csv_path):

    with open(csv_path, 'w') as f:
        writer = csv.writer(f)
        header = ['Origin Airport Name', 'Origin Code', 'Origin Continent', 'Origin Country',
                  'Dest. Airport Name', 'Dest. Code', 'Dest. Continent', 'Dest. Country',
                  'Departure Time', 'Arrival Time',
                  'Duration',
                  'Flight #',
                  'Equipment',
                  'Days of Week']

        writer.writerow(header)

        for flight in flight_list:
            formatted_flight = flight.format_for_csv()

            try:
                writer.writerow(formatted_flight)
            except UnicodeEncodeError:
                normalized_flight = []
                for col in formatted_flight:
                    if type(col) == unicode:
                        normalized_col = col.encode('utf8')
                    else:
                        normalized_col = col
                    normalized_flight.append(normalized_col)
                writer.writerow(normalized_flight)


if __name__ == '__main__':
    main()
