# --------------------------------------------
# flight.py
# Purpose: Contains Airport and flight classes
# Author: Chris Apple
# Tests: test_flight.py
# TODO:
# ---------------------------------------------

import os
import pdb
import re
from dateutil import parser

FLIGHT_CODES_FPATH = 'valid_flight_codes.txt'
FLIGHT_DIR = os.path.dirname(os.path.realpath(__file__))

SCHEDULE_CLEAN_REGEX = re.compile(r"(\d{1,2}:\d{1,2}[AP])\s+(\d{1,2}:\d{1,2}[AP])(\+\d)?\s+(\d{1,4})\s+(\w{3})\s\d\s+((\d{1,2}h)?(\d{1,2}m))([-| SMTWTF]+)")


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
            raise ValueError('FLIGHT CODE NOT FOUND: %s' % code)

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
        

class FlightTupleParser(object):
    """ Takes an individual flight object tuple and creates a list of flights """

    def __init__(self, origin_tuple, flight_tuple):
        """ 
        Parameters
        ----------
        destination_tuple : origin tuple
            From the read_in script a tuple that passes is_origin_or_header

        flight_tuple : destination_tuple
            A tuple that passes is_destination, has a schedule as last member
        """

        self._origin_tuple = origin_tuple 
        self._flight_tuple = flight_tuple
        self._resulting_flights = self._create_flights()

    @property
    def resulting_flights(self):
        return self._resulting_flights

    def _create_flights(self):

        origin_location, origin_code, _, distance, schedule_lines = self._flight_tuple

        schedule_list = schedule_lines.splitlines()

        schedule_list = [schedule for schedule in schedule_list if schedule != '']


        destination_location, destination_code, _, _, _ = self._origin_tuple

        destination_airport = Airport(destination_code, destination_location)
        origin_airport = Airport(origin_code, origin_location)

        resulting_flights = []
        for schedule in schedule_list:
            info_tuple = re.findall(SCHEDULE_CLEAN_REGEX, schedule)
            # departure, arrival, +1 (if necessary, flight number, equiptment, duration, duration hour, duration min, schedule string)

            departure_str, arrival_str, p1, flight_number, equip, duration, _, _, _ = info_tuple[0]
            departure = self._fix_time(departure_str) 
            arrival = self._fix_time(arrival_str)


            new_flight = Flight(origin_airport, destination_airport, departure, arrival, 
                                flight_number, equip, duration)

            resulting_flights.append(new_flight)

        return resulting_flights

    def _fix_time(self, flight_time):
        flight_date_time = parser.parse(flight_time)
        return flight_date_time

