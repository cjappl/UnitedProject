import pytest
from flight.Flight import Airport


def test_code_normal():
    SFO = Airport('SFO')
    assert SFO.code == 'SFO'


def test_code_number():
    with pytest.raises(TypeError):
        code = Airport(134)

def test_code_lower_case():
    SFO = Airport('sfO')
    assert SFO.code == 'SFO'

