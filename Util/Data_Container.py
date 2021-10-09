from math import log10
from math import sqrt

class Data_Container_2_Columns:

    def __init__(self, lines, name):
        self.list_of_lines = lines
        self.Column1 = []
        self.Column2 = []
        self.file_name = name

    def extract_columns(self, column_separator):
        self.Column1.clear()
        self.Column2.clear()
        for line in self.list_of_lines:
            split_line = line.split(column_separator)  # make list of line.
            self.Column1.append(float(split_line[0]))
            self.Column2.append(float(split_line[1]))

    def get_col1(self):
        return self.Column1

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

    def get_name(self):
        return self.file_name

    def set_name(self, name):
        self.file_name = name
