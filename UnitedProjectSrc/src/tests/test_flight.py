import pytest
import datetime
from obj.flight import * 


@pytest.fixture
def full_flight():
    origin = Airport('SFO', 'San Francisco')
    destination = Airport('LAX', 'Los Angeles')
    departure = datetime.datetime.today() 
    arrival = datetime.datetime.today()
    flight_num = 853
    equip = 747
    duration = datetime.time(hour=1, minute=30)

    return Flight(origin, destination, departure, arrival, flight_num, equip, duration)


def test_code_normal():
    SFO = Airport('SFO', 'SAN FRANCISCO')
    assert SFO.code == 'SFO'


def test_code_number():
    with pytest.raises(TypeError):
        code = Airport(134)


def test_code_lower_case():
    SFO = Airport('sfO', 'SAN FRANCISCO')
    assert SFO.code == 'SFO'


def test_flight_init_origin(full_flight):
    flight = full_flight
    assert flight.origin.code == 'SFO'


def test_flight_init_destination(full_flight):
    flight = full_flight
    assert flight.destination.code == 'LAX'


def test_flight_init_num(full_flight):
    flight = full_flight
    assert flight.flight_num == 853


def test_flight_init_equip(full_flight):
    flight = full_flight
    assert flight.equip == 747


def test_flight_init_duration(full_flight):
    flight = full_flight
    assert flight.duration.hour == 1
    assert flight.duration.minute == 30


   
