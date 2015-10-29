# --------------------------------------------
# flight.py
# Purpose: Contains Airport and flight classes
# Author: Chris Apple
# Tests: test_flight.py
# TODO:
# ---------------------------------------------
import os
import logging
from utils.flight_helpers import datetime_within_tolerance

FLIGHT_CODES_FPATH = 'valid_flight_codes.txt'
FLIGHT_DIR = os.path.dirname(os.path.realpath(__file__))

logger = logging.getLogger(__name__)

class Airport(object):
    """ A three letter string that represents a airport code """

    def __init__(self, code, location):
        self._code = self._init_code(code)
        self._location = location

    @property
    def code(self):
        return self._code

    @property
    def location(self):
        return self._location

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

        fpath = os.path.join(FLIGHT_DIR, FLIGHT_CODES_FPATH)
        with open(fpath) as f:
            flight_codes = f.readlines()

        if code + '\n' not in flight_codes:
            raise AirportNotExistError('FLIGHT CODE NOT FOUND: %s' % code)

        return code


class Flight(object):

    def __init__(self, origin, destination, departure, arrival, flight_num, equip, duration):
        self._origin = origin
        self._destination = destination
        self._departure = departure
        self._arrival = arrival
        self._flight_num = flight_num
        self._equip = equip
        self._duration = duration

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

    def format_for_csv(self):

        csv_tuple = (self._origin.location,
                     self._origin.code,
                     self.destination.location,
                     self.destination.code, 
                     self._departure.strftime('%I:%M %p'), 
                     self._arrival.strftime('%I:%M %p'),
                     self._duration,
                     self._flight_num,
                     self._equip)

        return csv_tuple

    def __repr__(self):
        repr_str = ''

        repr_str += '%s (%s) to %s (%s) | ' % (self._origin.location, self._origin.code,
                                        self.destination.location, self.destination.code) 

        repr_str += 'Departing: %s | Arriving: %s | ' % (self._departure.strftime('%I:%M %p'), 
                            self._arrival.strftime('%I:%M %p'))

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
