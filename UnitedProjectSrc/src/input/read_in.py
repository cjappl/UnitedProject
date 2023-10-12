# ---------------------------------------
# Contains input class
# Will read in files and parse them
#
#
#
#
# ---------------------------------------
import csv
import os
import re
from PyPDF2 import PdfFileReader
from dateutil import parser
from obj.flight import Flight, Airport, AirportNotExistError


CURRENT_FILE_DIR = os.path.dirname(os.path.realpath(__file__))
OUT_TXT = os.path.join(CURRENT_FILE_DIR, 'pdf', 'out', 'out.txt')

PDF_REGEX = re.compile(r"([\w\-\., /\(\)']+)\((\w{3})([- \.'\w]+)?\)\n(Cont'd.|[\d,]+ mi)?(((\s*\d{1,2}:\d{2}[AP])\s*(\d{1,2}:\d{2}[AP])(\+\d)?\s*(\w{1,4})\s*(\w{3})\s+\d\s+(\d{1,2}h)?(\d{1,2}m) ([-SMTWTF|]+)\n)+)?")

SCHEDULE_CLEAN_REGEX = re.compile(r'(\d{1,2}:\d{1,2}[AP])\s+(\d{1,2}:\d{1,2}[AP])(\+\d)?\s+(\d{1,4})\s+(\w{3})\s\d\s+((\d{1,2}h)?(\d{1,2}m))([-| SMTWTF]+)')


def get_flights_pdf(page_start, USE_NEW_PDF):
    """ Will create all possible flights from a united pdf

    Parameters
    ----------
    page_start : int
        The page number of the first schedule page of a united pdf

    Returns
    -------
    flights : List of Flight objects
        All possible flights available from the united PDF
    """

    united_pdf_parser = UnitedPdfParser()
    if USE_NEW_PDF:
        united_pdf_parser.input_pdf(page_start)
    else:
        united_pdf_parser.input_txt()

    flight_tuples = united_pdf_parser.flight_regex_tuples

    # we are assuming at this point headers are stripped, so we will create an alias
    is_origin = is_header_or_origin

    assert is_origin(flight_tuples[0])

    origin = None
    all_flights = []

    for flight_tuple in flight_tuples:

        if is_origin(flight_tuple):
            # if new origin comes up, replace the old origin
            origin = flight_tuple
        else:
            # otherwise create all flights from that next tuple and proceed
            try:
                curr_flight_tup_parser = FlightTupleParser(origin, flight_tuple)
                all_flights.append(curr_flight_tup_parser.resulting_flights)
            except AirportNotExistError as e:
                print e

    return all_flights


def get_flights_csv(csv_path):
    """ Reads in a csv with flight info, outputs flights """

    all_flights = []
    with open(csv_path, 'rU') as f:
        reader = csv.reader(f)
        for line in reader:
            if line[0] == 'Departs':
                continue
            else:
                origin = Airport(line[0], '')
                destination = Airport(line[1], '')
                try:
                    flight_number = int(line[2])
                except ValueError:
                    continue
                departure = _fix_time(line[3])
                arrival = _fix_time(line[4])
                equiptment = line[5]
                DOW = line[6]
                if not origin:
                    continue

                new_flight = Flight(origin, destination, departure, arrival,
                                    flight_number, equiptment, None, DOW)

                all_flights.append(new_flight)

    return all_flights


class UnitedPdfParser(object):

    def __init__(self):
        self._regex = PDF_REGEX
        self._out_txt = OUT_TXT

        self._pdf_path = _find_input_pdf_path()
        self._full_pdf_string = None
        self._flight_regex_tuples = None

    @property
    def flight_regex_tuples(self):
        """ Getter for flight regex tuples """
        return self._flight_regex_tuples

    def input_pdf(self, page_start):
        """ reads in a new pdf for analysis """
        self._create_txt_from_pdf(page_start)
        self._read_txt_into_str()
        self._create_regex_tuples()

    def input_txt(self):
        """ uses an existing txt for analysis """
        self._read_txt_into_str()
        self._create_regex_tuples()

    def _create_txt_from_pdf(self, page_start):
        """ creates .txt file from pdf using system call to pdf2txt.py """

        last_page_number = PdfFileReader(self._pdf_path).getNumPages()

        rng = range(page_start, last_page_number + 1)  # inclusive range to last page

        page_str = ','.join([str(page) for page in rng])
        # above lines will output in the form N,M,O,P where each letter is a page to extract from the .pdf

        cmd = 'pdf2txt.py -p %s -o %s %s' % (page_str, self._out_txt, self._pdf_path)
        os.system(cmd)

    def _read_txt_into_str(self):
        """ reads the txt file into a string variable """
        with open(self._out_txt, 'r') as f:
            self._full_pdf_string = f.read()

    def _create_regex_tuples(self):
        """ Creates the regex groups for cleaning. As it stands the groups will be:

        1) name, 2) code, 3) optional extention, 4) distance 5) schedule string
        """

        regex_groups_original = re.findall(self._regex, self._full_pdf_string)

        # The first 5 fields are all we care about
        regex_groups_trimmed = [group[:5] for group in regex_groups_original]
        # 1) name, 2) code, 3) optional extention, 4) distance 5) schedule string

        regex_groups_no_headers = _remove_headers(regex_groups_trimmed)

        self._flight_regex_tuples = regex_groups_no_headers


class FlightTupleParser(object):
    """ Takes an individual flight object tuple and an origin and creates a list of flights """

    def __init__(self, origin_tuple, flight_tuple):
        """
        Parameters
        ----------
        destination_tuple : origin tuple
            From the read_in script a tuple that passes is_origin_or_header

        flight_tuple : destination_tuple
            A tuple that passes is_destination, has a schedule as last member
        """

        self._origin_tuple = self._strip_tuple(origin_tuple)
        self._flight_tuple = self._strip_tuple(flight_tuple)
        self._resulting_flights = self._create_flights()

    @property
    def resulting_flights(self):
        # TODO: rename maybe
        return self._resulting_flights

    def _create_flights(self):
        """ Creates a flight for each line in the schedule of flight_tuple

        Returns
        -------
        resulting_flights : list of Flight
            A list of all flights in the schedule string of flight_tuple
        """

        destination_location, destination_code, _, distance, schedule_lines = self._flight_tuple

        schedule_list = schedule_lines.splitlines()
        schedule_list = [schedule for schedule in schedule_list if schedule != '']

        origin_location, origin_code, _, _, _ = self._origin_tuple

        destination_airport = Airport(destination_code, destination_location)
        origin_airport = Airport(origin_code, origin_location)

        resulting_flights = []

        for schedule in schedule_list:
            info_tuple = re.findall(SCHEDULE_CLEAN_REGEX, schedule)
            # info_tuple of the form:
            # departure, arrival, +1 (if necessary), flight number, equiptment, duration,
            # duration hour, duration min, schedule string

            departure_str, arrival_str, p1, flight_num, equip, duration, _, _, _ = info_tuple[0]
            flight_num = int(flight_num)
            departure = _fix_time(departure_str)
            arrival = _fix_time(arrival_str)

            # If the flight looks like it can be simplified, we'll skip it and leave the earlier

            new_flight = Flight(origin_airport, destination_airport,
                                departure, arrival,
                                flight_num, equip, duration)

            resulting_flights.append(new_flight)

        return resulting_flights

    def _strip_tuple(self, input_tuple):
        """ Removes leading and following spaces from each field in the tuple

        Parameters
        ----------
        input_tuple : tuple of str
            A tuple of strings with spaces to get rid of at the end/beg
            (' hi guys ', 'hi guys ', ' hi guys')

        Returns
        -------
        output_tuple : tuple of str
            Tuple of strings with spaces removed on either end
            ('hi guys', 'hi guys', 'hi guys')
        """
        # TODO: Doesn't need to be a method of this class

        output_list = [field.strip() for field in input_tuple]
        output_tuple = tuple(output_list)

        return output_tuple


def _find_input_pdf_path():
    """ Returns the path of the first file in PDF_INPUT_FOLDER ending with .pdf

    Does some checking to make sure it can't be confused
    """

    input_pdf_folder = os.path.join(CURRENT_FILE_DIR, os.path.pardir, os.path.pardir, os.path.pardir, 'PDF_INPUT_FOLDER')
    input_pdf_path = None
    pdf_count = 0

    for file in os.listdir(input_pdf_folder):
        if file.endswith('.pdf'):
            input_pdf_path = os.path.join(input_pdf_folder, file)

            pdf_count += 1

    if input_pdf_path is None:
        raise PDFImportError('No PDF found in PDF_INPUT_FOLDER')

    if pdf_count > 1:
        raise PDFImportError('More than one PDF found in PDF_INPUT_FOLDER')

    return input_pdf_path


class PDFImportError(Exception):
    """ Exception for incorrect pdf import """
    pass


def is_header_or_origin(regex_parsed_tuple):
    """ Returns True if the tuple is of the form:
    (origin_name, origin_code, ?, '', '')
    (origin_name, origin_code, ?, 'Cont'd.', '')

    This corresponds to an origin or header

    Parameters
    ----------
    regex_parsed_tuple : tup
        A len 5 tuple from a parsed United Pdf

    Returns
    -------
    Bool : if last member is empty
    """
    # TODO: make private

    if regex_parsed_tuple[-1] is '':
        return True
    else:
        return False


def is_destination(regex_parsed_tuple):
    """ Returns True if the tuple is of the form:
    (origin_name, origin_code, ?, '', 'schedule_info')

    This corresponds to a destination member

    schedule_info strings must have | in them

    Parameters
    ----------
    regex_parsed_tuple : tup
        A len 5 tuple from a parsed United Pdf

    Returns
    -------
    Bool : if last member contains |
    """
    # TODO: make private

    if '|' in regex_parsed_tuple[-1]:
        return True
    else:
        return False


def _remove_headers(full_regex_list):
    """ Removes headers from the full regex list

    Used to prepare for final parsing

    Parameters
    ----------
    full_regex_list : list of tup
        A list from UnitedPdfParser containing the full regex group

    Returns
    -------
    regex_without_headers : list of tup
        A list without headers. Headers will be found by:
        1) iterating through list
        2) if 3 headers or origins are found in a row, toss the first 2

        Headers have been found to occur like this in the outputted regex groups
    """
    i_to_remove = []
    count = 0
    for index, regex_group in enumerate(full_regex_list):
        if count == 3:
            # we will keep the last, but remove the two before it
            # it is expected that we are on a destination flight now
            i_to_remove.append(index - 3)
            i_to_remove.append(index - 2)

            if is_header_or_origin(regex_group):
                # case of 4 in a row
                i_to_remove.append(index - 1)

        if is_header_or_origin(regex_group):
            count += 1
        else:
            count = 0

    regex_without_headers = [full_regex_list[i] for i in range(len(full_regex_list)) if i not in i_to_remove]

    return regex_without_headers


def _fix_time(flight_time_str):
    """ Parses flight time string and returns a datetime object

    Parameters
    ----------
    flight_time_str : str
        Ususally in the form 12:00PM, parser should handle others

    Returns
    -------
    flight_date_time : datetime.datetime
        Datetime object of the same time
    """

    flight_date_time = parser.parse(flight_time_str)
    return flight_date_time
