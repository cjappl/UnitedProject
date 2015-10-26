from input.read_in import * 
import pytest
import os

ORIGIN = ('CHICAGO, IL ', 'ORD', " - O'HARE", "Cont'd.", '')
HEADER = ('COLLEGE STATION, TX ', 'CLL', '', '', '')
DESTINATION =  ('BERLIN, GERMANY ',
  'TXL',
  ' - TEGEL',
  '288 mi',
  '\n 6:25A   7:35A    2768    320 0   1h10m --MT-T-|-------|-------|-------\n 6:30A   7:40A    2768    320 0   1h10m -------|--MT---|--MT---|--MT---\n 6:30A   7:40A    2768    319 0   1h10m -------|-----T-|-----T-|-----T-\n 6:45A   7:55A    2757    319 0   1h10m S------|S------|-------|-------\n')


@pytest.fixture
def parser():
    parser = UnitedPdfParser(109)
    return parser


def test_pdf_exists(parser):
    assert os.path.isfile(parser._pdf_path)


def test_is_header_or_origin():
    assert is_header_or_origin(ORIGIN)
    assert is_header_or_origin(HEADER)
    assert not is_header_or_origin(DESTINATION)


def test_is_destination():
    assert is_destination(DESTINATION)
    assert not is_destination(ORIGIN)
    assert not is_destination(HEADER)


@pytest.mark.long
def test_create_txt_from_pdf(parser):
    parser._create_txt_from_pdf()
    assert os.path.isfile(parser._out_txt)

@pytest.mark.input_pdf
@pytest.mark.long
def test_input_pdf(parser):
    parser.input_pdf()

    assert parser._full_pdf_string

@pytest.mark.long
@pytest.mark.input_regex
def test_input_regex(parser):
    parser.input_pdf()
    parser._create_regex_groups()
    list_of_reg = parser._regex_groups
    assert len(list_of_reg)
