# --------------------------------------------
# flight.py
# Purpose: Contains Airport and flight classes
# Author: Chris Apple
# Tests: test_flight.py
# TODO:
# ---------------------------------------------

import os
import logging
import json
from utils.flight_helpers import datetime_within_tolerance

FLIGHT_CODES_FPATH = 'valid_flight_codes.txt'
CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))

JSON_PATH = os.path.join(CURRENT_DIR, 'airports.json')

logger = logging.getLogger(__name__)

CSV_TIME_FORMAT = '%H:%M'
PDF_TIME_FORMAT = '%I:%M %p'


class Airport(object):
    """ A three letter string that represents a airport code """

    def __init__(self, code, location):
        self._location = location
        self._code = self._init_code(code)
        self._continent = None
        self.db_entry = None

    @property
    def code(self):
        return self._code

    @property
    def location(self):
        return self._location

    @property
    def continent(self):
        return self._continent

    def _init_code(self, code):
        """ Cleans the code for input

        Parameters
        ----------
        code : anything
            A code to be inputted, we would like to error check it

        Returns
        ----------
        code : str
            A three letter all caps string representing an airport code

        Raises
        ------
        TypeError - if input string is of the wrong type

        ValueError - if the string is not found in the supporting document

        TODO: Make code checking more robust
        """

        try:
            code = code.upper()
        except AttributeError:
            raise TypeError('UNEXPECTED AIRPORT CODE: %s' % code)

        """
        flight_codes = [flight['iata'] for flight in self._flight_json]

        if code not in flight_codes:

            # pdb.set_trace()
            raise AirportNotExistError('FLIGHT CODE NOT FOUND: %s' % code)
        """

        return code

    def init_continent(self, airports):
        if self.db_entry:
            self._continent = self.db_entry['continent']
        else:
            # must search through database
            for airport in airports:
                if airport['iata'] == self._code:
                    self.db_entry = airport
                    self._continent = str(airport['continent'])
                    break
            else:
                self._continent = '?'

    def init_location(self, airports):
        if self.db_entry:
            self._location = self.db_entry['name']
        else:
            for airport in airports:
                if airport['iata'] == self._code:
                    self.location = str(airport['name'])
                    break
            else:
                self._location = '?'

    def _get_json(self):
        with open(JSON_PATH, 'r') as f:
            airport_json = json.load(f)

        return airport_json


class Flight(object):

    def __init__(self, origin, destination, departure, arrival,
                 flight_num, equip, duration, DOW=None):
        self._origin = origin
        self._destination = destination
        self._departure = departure
        self._arrival = arrival
        self._flight_num = flight_num
        self._equip = equip
        self._duration = duration
        self._DOW = self._fill_days_of_week(DOW)

    @property
    def origin(self):
        return self._origin

    @property
    def destination(self):
        return self._destination

    @property
    def departure(self):
        return self._departure

    @property
    def arrival(self):
        return self._arrival

    @property
    def flight_num(self):
        return self._flight_num

    @property
    def equip(self):
        return self._equip

    @property
    def duration(self):
        return self._duration

    def _fill_days_of_week(self, DOW):
        if DOW is None:
            return
        if '1' in DOW:
            self.mon = 'Mon'
        else:
            self.mon = ''
        if '2' in DOW:
            self.tue = 'Tue'
        else:
            self.tue = ''
        if '3' in DOW:
            self.wed = 'Wed'
        else:
            self.wed = ''
        if '4' in DOW:
            self.thu = 'Thu'
        else:
            self.thu = ''
        if '5' in DOW:
            self.fri = 'Fri'
        else:
            self.fri = ''
        if '6' in DOW:
            self.sat = 'Sat'
        else:
            self.sat = ''
        if '7' in DOW:
            self.sun = 'Sun'
        else:
            self.sun = ''

    def format_for_csv(self):

        csv_tuple = (self._origin.location,
                     self._origin.code,
                     self._origin.continent,
                     self._destination.location,
                     self._destination.code,
                     self._destination.continent,
                     self._departure.strftime(CSV_TIME_FORMAT),
                     self._arrival.strftime(CSV_TIME_FORMAT),
                     self._duration,
                     self._flight_num,
                     self._equip,
                     self.sun,
                     self.mon,
                     self.tue,
                     self.wed,
                     self.thu,
                     self.fri,
                     self.sat
                     )

        return csv_tuple

    def __repr__(self):
        repr_str = ''

        repr_str += '%s (%s) to %s (%s) | ' % (self._origin.location, self._origin.code,
                                               self.destination.location, self.destination.code)

        repr_str += 'Departing: %s | Arriving: %s | ' % \
                    (self._departure.strftime(CSV_TIME_FORMAT),
                     self._arrival.strftime(CSV_TIME_FORMAT))

        repr_str += 'Duration: %s | ' % self._duration

        repr_str += 'Flight Number: %s | ' % self._flight_num

        repr_str += 'Plane: %s |' % self._equip

        return repr_str

    def __eq__(self, other):
        EQUALITY_TOL = 60  # 30 minute equality tolerance
        if isinstance(other, self.__class__):
            if self._flight_num == other.flight_num:
                if datetime_within_tolerance(self._departure, other.departure, EQUALITY_TOL):
                    return True
        return False

    def __ne__(self, other):
        return not self.__eq__(other)


class AirportNotExistError(Exception):
    pass
