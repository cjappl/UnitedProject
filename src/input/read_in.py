# ---------------------------------------
# Contains input class
# Will read in files and parse them
#
#
#
#
# ---------------------------------------
# TODO: remove
import pdb
from pprint import pformat

import os
import re
from utils.united_logging import get_united_logger

PDF_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'pdf', 'timetable.pdf')
OUT_TXT = os.path.join(os.path.dirname(os.path.realpath(__file__)),  'pdf', 'out', 'out.txt')
MAX_PAGES = 300

REGEX = re.compile(r"([\w\-\., /']+)\((\w{3})([- \.'\w]+)?\)\n(Cont'd.|[\d,]+ mi)?(((\s*\d{1,2}:\d{2}[AP])\s*(\d{1,2}:\d{2}[AP])(\+\d)?\s*(\w{1,4})\s*(\w{3})\s+\d\s+(\d{1,2}h)?(\d{1,2}m) ([-SMTWTF|]+)\n)+)?")

logger = get_united_logger()


class UnitedPdfParser(object):

    def __init__(self, page_start):
        self._regex_groups = None
        self._pdf_path = PDF_PATH
        self._out_txt = OUT_TXT
        self._full_pdf_string = None
        self._regex = REGEX
        self._page_start = page_start

    def input_pdf(self):
        self._create_txt_from_pdf()
        self._read_txt_into_str()

    def create_regex_groups(self):
        regex_groups_original = re.findall(REGEX, self._full_pdf_string)

        # The first 5 fields are most important
        self._regex_groups = [group[:5] for group in regex_groups_original]
        # 1) name, 2) code, 3) optional extention, 4) distance 5) schedule string

        # TODO: REMOVE
        pretty_str = pformat(self._regex_groups, width=70)
        with open('pretty_str.txt', 'w') as f:
            f.write(pretty_str)

        pdb.set_trace()
        #

    def _create_txt_from_pdf(self):
        """ creates .txt file from pdf using system call to pdf2txt.py """
        logger.info('Creating text file from pdf: %s' % self._pdf_path)
        logger.info('Starting at page %i' % self._page_start)

        page_str = ''
        for number in range(self._page_start, MAX_PAGES):
            page_str += str(number) + ','

        page_str = page_str[:-1]  # remove the last comma

        cmd = 'pdf2txt.py -p %s -o %s %s' % (page_str, self._out_txt, self._pdf_path)
        os.system(cmd)
        logger.info('SUCCESS!')

    def _read_txt_into_str(self):
        """ reads the txt file into a string variable """
        logger.info('Reading in text file')
        with open(self._out_txt, 'r') as f:
            self._full_pdf_string = f.read()
        logger.info('SUCCESS!')
