from input.read_in import UnitedPdfParser 
import pytest
import os


@pytest.fixture
def parser():
    parser = UnitedPdfParser(109)
    return parser

def test_pdf_exists(parser):
    assert os.path.isfile(parser._pdf_path)

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
    parser.create_regex_groups()
