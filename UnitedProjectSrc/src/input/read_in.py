# ---------------------------------------
# Contains input class
# Will read in files and parse them
#
#
#
#
# ---------------------------------------

import os
import re

PDF_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'pdf', 'timetable.pdf')
OUT_TXT = os.path.join(os.path.dirname(os.path.realpath(__file__)),  'pdf', 'out', 'out.txt')
MAX_PAGES = 300

REGEX = re.compile(r"([\w\-\., /']+)\((\w{3})([- \.'\w]+)?\)\n(Cont'd.|[\d,]+ mi)?(((\s*\d{1,2}:\d{2}[AP])\s*(\d{1,2}:\d{2}[AP])(\+\d)?\s*(\w{1,4})\s*(\w{3})\s+\d\s+(\d{1,2}h)?(\d{1,2}m) ([-SMTWTF|]+)\n)+)?")



class UnitedPdfParser(object):

    def __init__(self, page_start):
        self._page_start = page_start

        self._regex_groups = None
        self._pdf_path = PDF_PATH
        self._out_txt = OUT_TXT
        self._full_pdf_string = None
        self._regex = REGEX

    def input_pdf(self):
        self._create_txt_from_pdf()
        self._read_txt_into_str()
        self._create_regex_groups()

    def _create_regex_groups(self):
        """ Creates the regex groups for cleaning. As it stands the groups will be:

        1) name, 2) code, 3) optional extention, 4) distance 5) schedule string
        """

        regex_groups_original = re.findall(REGEX, self._full_pdf_string)

        # The first 5 fields are most important
        regex_groups_trimmed = [group[:5] for group in regex_groups_original]
        # 1) name, 2) code, 3) optional extention, 4) distance 5) schedule string

        regex_groups_no_headers = _remove_headers(regex_groups_trimmed)
        

    def _create_txt_from_pdf(self):
        """ creates .txt file from pdf using system call to pdf2txt.py """

        page_str = ''
        for number in range(self._page_start, MAX_PAGES):
            page_str += str(number) + ','

        page_str = page_str[:-1]  # remove the last comma

        cmd = 'pdf2txt.py -p %s -o %s %s' % (page_str, self._out_txt, self._pdf_path)
        os.system(cmd)

    def _read_txt_into_str(self):
        """ reads the txt file into a string variable """
        with open(self._out_txt, 'r') as f:
            self._full_pdf_string = f.read()


def is_header_or_origin(regex_parsed_tuple):
    """ Returns True if the tuple is of the form:
    (origin_name, origin_code, ?, '', '')
    (origin_name, origin_code, ?, 'Cont'd.', '')

    This corresponds to an origin or header 
    
    Parameters
    ----------
    regex_parsed_tuple : tup
        A len 5 tuple from a parsed United Pdf

    Returns
    -------
    Bool : if last member is empty
    """
    # TODO: make private

    if regex_parsed_tuple[-1] is '':
        return True
    else:
        return False

def is_destination(regex_parsed_tuple):
    """ Returns True if the tuple is of the form:
    (origin_name, origin_code, ?, '', 'schedule_info')

    This corresponds to a destination member 

    schedule_info strings must have | in them
    
    Parameters
    ----------
    regex_parsed_tuple : tup
        A len 5 tuple from a parsed United Pdf

    Returns
    -------
    Bool : if last member contains |  
    """
    # TODO: make private

    if '|' in regex_parsed_tuple[-1]:
        return True
    else:
        return False

def _remove_headers(full_regex_list):
    """ Removes headers from the full regex list

    Used to prepare for final parsing

    Parameters
    ----------
    full_regex_list : list of tup
        A list from UnitedPdfParser containing the full regex group
    
    Returns
    -------
    regex_without_headers : list of tup
        A list without headers. Headers will be found by:
        1) iterating through list
        2) if 3 headers or origins are found in a row, toss the first 2

        Headers have been found to occur like this in the outputted regex groups 
    """
    i_to_remove = []
    count = 0
    for index, regex_group in enumerate(full_regex_list): 
        if count == 3:
            i_to_remove.append(index - 2)
            i_to_remove.append(index - 1)

        if is_header_or_origin(regex_group):
            count += 1
        else:
            count = 0

    regex_without_headers = [full_regex_list[i] for i in range(len(full_regex_list)) if i not in i_to_remove]

    return full_regex_list
