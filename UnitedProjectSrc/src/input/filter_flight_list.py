# --------------------------------------------------
# filter_flight_list
# contains master filter to be applied to flight list
#
# TODO: Break into individual functions
# TODO: Unit test
# --------------------------------------------------


def filter_flight_list(flight_list, remove_duplicates=None, flight_number_range=None):
    """
    Parameters
    ----------
    flight_list : List of list of flight by origin
        List of flights to filter
    remove_duplicates : Bool
        True if removing flights that are "equal"
    flight number range : tup of int
        Min and max allowable flight numbers
    """

    flights_to_filter = []
    if remove_duplicates:
        for sublist in flight_list:
            sublist.sort(key=lambda fl: fl.flight_num)

            seen_flights = []
            for flight in sublist:
                if seen_flights:
                    last_flight_added = seen_flights[-1]
                    if flight != last_flight_added:
                        seen_flights.append(flight)
                else:
                    seen_flights.append(flight)

            seen_flights.sort(key=lambda fl: fl.departure)
            flights_to_filter += seen_flights
    else:
        try:
            # list of lists option, used in the pdf
            flights_to_filter = [flight for sublist in flight_list for flight in sublist]
        except TypeError:
            # Flat list, found in the csv
            flights_to_filter = flight_list

    if flight_number_range:
        min_flight_num, max_flight_num = flight_number_range
        flights_to_filter = [flight for flight in flights_to_filter if
                             flight.flight_num < max_flight_num]

        flights_to_filter = [flight for flight in flights_to_filter if
                             flight.flight_num > min_flight_num]

    filtered_flights = flights_to_filter
    return filtered_flights
