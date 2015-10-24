# --------------------------------------------
# flight.py
# Purpose: Contains Airport and flight classes
# Author: Chris Apple
# Tests: test_flight.py
# TODO:
# ---------------------------------------------

import os
import pdb

FLIGHT_CODES_FPATH = 'valid_flight_codes.txt'
FLIGHT_DIR = os.path.dirname(os.path.realpath(__file__))


class Airport(object):
    """ A three letter string that represents a airport code """

    def __init__(self, code):
        self._code = self._init_code(code)

    @property
    def code(self):
        return self._code

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
            raise ValueError('FLIGHT CODE NOT FOUND: %s' % code)

        return code


class Flight(object):

    def __init__(self, origin, destination, flight_num, equip, duration):
        self._origin = origin
        self._destination = destination
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
    def flight_num(self):
        return self._flight_num

    @property
    def equip(self):
        return self._equip

    @property
    def duration(self):
        return self._duration
