import pytest
import datetime
from flight.flight import * 
from utils.united_logging import get_united_logger

FLIGHT_TUP = ('DENVER, CO ',
  'DEN',
  '',
  '73 mi',
  '\n 6:00A   6:50A    6230    CR7 0     50m -------|-SMTWTF|SSMTWTF|SSMTWTF\n 6:00A   6:48A    6230    E7W 0     48m --MTWTF|-------|-------|-------\n 6:00A   6:48A    6230    CR7 0     48m -S-----|-------|-------|-------\n 6:20A   7:08A    5268    CR7 0     48m S------|S------|-------|-------\n 6:22A   7:08A    5268    E7W 0     46m -S-----|-------|-------|-------\n 6:38A   7:25A    5633    E7W 0     47m -------|--MTWTF|S-MTWTF|S-MTWTF\n 6:38A   7:25A    5633    CR7 0     47m -------|-S-----|-------|-------\n 6:40A   7:25A    5268    CR7 0     45m ---TW--|-------|-------|-------\n 6:45A   7:30A    5268    CR7 0     45m --M--TF|-------|-------|-------\n 8:00A   8:48A    5633    CRJ 0     48m SSMTWTF|S------|-------|-------\n 8:00A   8:51A    5509    CRJ 0     51m -------|--MTWTF|S-MTWTF|S-MTWTF\n 8:29A   9:20A    5509    E7W 0     51m -------|-S-----|-S-----|-S-----\n 8:29A   9:20A    5485    E7W 0     51m -------|--MTWTF|--MTWTF|--MTWTF\n 8:30A   9:15A    6234    E7W 0     45m S------|S------|-------|-------\n 8:33A   9:18A    6234    CR7 0     45m -S-----|-------|-------|-------\n 8:35A   9:20A    6234    CR7 0     45m --MTWTF|-------|-------|-------\n 9:01A   9:55A    5485    CR7 0     54m -------|-------|-------|S------\n 9:21A  10:15A    5485    CR7 0     54m -------|-------|S------|-------\n 9:38A  10:29A    5485    E7W 0     51m SSMTWTF|S------|-------|-------\n10:56A  11:50A    5485    CR7 0     54m -------|-------|-S-----|-------\n10:56A  11:50A    5485    CRJ 0     54m -------|-S-----|-------|-S-----\n11:00A  11:51A    5229    CR7 0     51m -SMTWTF|-------|-------|-------\n11:00A  11:52A    3428    ERJ 0     52m S------|S------|-------|-------\n11:06A  12:00P    3432    ERJ 0     54m -------|-------|------F|--MTWTF\n11:07A  12:01P    3432    ERJ 0     54m -------|--MTWTF|--MTWT-|-------\n11:37A  12:23P    4887    DH4 0     46m SS--W--|S------|-------|-------\n11:39A  12:25P    4887    DH4 0     46m --M--TF|-------|-------|-------\n12:09P  12:54P    5229    CRJ 0     45m -------|-S-----|-S-----|-S-----\n12:14P  12:59P    5229    CRJ 0     45m -------|--M----|-------|-------\n12:19P   1:07P    4875    DH4 0     48m -------|-------|-------|S------\n12:19P   1:07P    4894    DH4 0     48m -------|-------|S------|-------\n12:19P   1:04P    5229    CRJ 0     45m -------|----WTF|--M-WTF|--M-WTF\n 1:50P   2:38P    5268    CRJ 0     48m -------|-S-----|-S-----|-S-----\n 1:50P   2:40P    4875    DH4 0     50m -------|--M-WTF|--M-WTF|--M-WTF\n')

ORIGIN_TUP = ('COLORADO SPRINGS, CO ', 'COS', '', '', '')

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


def test_flight_tuple_parser():
    FTP = FlightTupleParser(ORIGIN_TUP, FLIGHT_TUP)
    pytest.set_trace()
    
