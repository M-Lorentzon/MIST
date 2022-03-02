from math import log10
from math import sqrt
import re

class Data_Container:

    def __init__(self, lines, name):
        self.list_of_lines = lines
        self.Column1 = []
        self.Column2 = []
        self.Column3 = []
        self.Column4 = []
        self.Column5 = []
        self.Column6 = []
        self.list_of_columns = [self.Column1, self.Column2, self.Column3, self.Column4, self.Column5, self.Column6]

        self.file_name = name
        self.number_of_columns = 0

    def extract_columns(self, ignore_rows=0):
        self.clear_columns()
        delimiters = " ", ",", ";", "\t", ":"
        # Init extraction
        one_row = self.list_of_lines[ignore_rows+1]
        one_row_split = re.split('[ ;:|\t]', one_row)
        self.number_of_columns = len(one_row_split)

        for index, line in enumerate(self.list_of_lines):
            if index > ignore_rows:
                split_line = re.split('[ ;:|\t]', line)
                if len(split_line) == self.number_of_columns :
                    for col_index, value in enumerate(split_line) :
                        self.list_of_columns[col_index].append(float(value))


    def get_col1(self):
        return self.Column1

    def get_col2(self):
        return self.Column2

    def get_col3(self):
        return self.Column3

    def get_col4(self):
        return self.Column4

    def get_col5(self):
        return self.Column5

    def get_col6(self):
        return self.Column6

    def get_col2_in_linear_with_offset(self, offset):
        retval = []
        for elem in self.Column2:
            retval.append(elem + offset)
        return retval

    def get_col2_in_log_with_offset(self, offset):
        retval = []
        for elem in self.Column2:
            try:
                retval.append(log10(elem) + offset)
            except:
                retval.append(offset)
        return retval

    def get_col2_in_sqrt_with_offset(self, offset):
        retval = []
        for elem in self.Column2:
            try:
                retval.append(sqrt(elem) + offset)
            except:
                retval.append(offset)
        return retval


    def clear_columns(self):
        self.Column1.clear()
        self.Column2.clear()
        self.Column3.clear()
        self.Column4.clear()
        self.Column5.clear()
        self.Column6.clear()

    def get_name(self):
        return self.file_name

    def set_name(self, name):
        self.file_name = name

