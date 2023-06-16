from math import log10
from math import sqrt
import re

class Data_Container:

    def __init__(self, lines, name, path):
        self.list_of_lines = lines
        self.Column1 = []
        self.Column2 = []
        self.Column3 = []
        self.Column4 = []
        self.Column5 = []
        self.Column6 = []
        self.Column7 = []
        self.list_of_columns = [self.Column1, self.Column2, self.Column3, self.Column4, self.Column5, self.Column6, self.Column7]

        self.file_name = name
        self.file_path = path
        self.number_of_columns = 0

    def extract_columns(self, ignore_rows = -1):
        self.clear_columns()
        delimiters = " ", ",", ";", "\t", ":"
        # Init extraction
        one_row = self.list_of_lines[ignore_rows+1]
        one_row_split = re.split('[ ;:|\t]', one_row)
        self.number_of_columns = len(one_row_split)
        ## print("Number of columns = ", self.number_of_columns)

        for index, line in enumerate(self.list_of_lines):
            if index > ignore_rows:
                split_line = re.split('[ ;:|\t]', line)
                if len(split_line) == self.number_of_columns :
                    for col_index, value in enumerate(split_line) :
                        ## print("Value = ", value)
                        try:
                            self.list_of_columns[col_index].append(float(value))
                        except (ValueError):
                            print("ValueError in extracting data")

        ## print("Column1 = ", self.Column1)
        ## print("Column2 = ", self.Column2)

    def extract_columns_plasma_probe(self, ignore_rows=-1):
        self.clear_columns()
        # Init extraction
        one_row = self.list_of_lines[ignore_rows + 1]
        one_row_split = re.split('[ ;:|\t]', one_row)
        self.number_of_columns = len(one_row_split)

        for index, line in enumerate(self.list_of_lines):
            if index > ignore_rows:
                split_line = re.split('[ ;:|\t]', line)
                if len(split_line) == self.number_of_columns:
                    for col_index, value in enumerate(split_line):

                        ## print("Value = ", value)
                        try:
                            self.list_of_columns[col_index].append(float(value.replace(",", ".")))
                        except (ValueError):
                            print("ValueError in extracting data")

    def extract_columns_2D_WAX(self, ignore_rows = -1):
        self.clear_columns()
        delimiters = " ", ",", ";", "\t", ":"
        # Init extraction
        one_row = self.list_of_lines[ignore_rows+1]
        one_row_split = re.split('[ ;:|\t]', one_row)
        self.number_of_columns = len(one_row_split)

        for index, line in enumerate(self.list_of_lines):
            if index > ignore_rows:
                split_line = re.split('[ ;:|\t]', ' '.join(line.split()))
                if len(split_line) == 2 :
                    for col_index, value in enumerate(split_line) :
                        try:
                            self.list_of_columns[col_index].append(float(value))
                        except (ValueError):
                            print("ValueError when importing data")

    def extract_columns_SRIM(self):
        self.clear_columns()
        ignore_rows_top = 23
        ignore_rows_bottom = 13

        # create sublist to work with (remove top and bottom)
        Number_of_rows = len(self.list_of_lines)
        indices = range(ignore_rows_top, Number_of_rows-ignore_rows_bottom)

        unit = self.list_of_lines[17]
        print(unit)

        for index in indices:
            row = self.list_of_lines[index]
            split_row = re.split(";", re.sub("\s+", ";", row))
            fixed_row = list(filter(None, split_row))

            self.Column1.append(self.convert_to_eV(float(fixed_row[0]), fixed_row[1])) # ion energy
            self.Column2.append(float(fixed_row[2])) # Electronic stopping
            self.Column3.append(float(fixed_row[3])) # Nuclear stopping
            self.Column4.append(float(fixed_row[2]) + float(fixed_row[3])) # Sum stopping
            self.Column5.append(self.convert_to_A(float(fixed_row[4]), fixed_row[5])) # Projected range
            self.Column6.append(self.convert_to_A(float(fixed_row[6]), fixed_row[7])) # Longitudinal straggling
            self.Column7.append(self.convert_to_A(float(fixed_row[8]), fixed_row[9])) # Lateral straggling


    def convert_to_eV(self, value, unit):
        if unit == "eV":
            return value
        elif unit == "keV":
            return value*1000
        elif unit == "MeV":
            return value*1000000
        elif unit == "GeV":
            return value*1000000000

    def convert_to_A(self, value, unit):
        if unit == "A":
            return value
        elif unit == "um":
            return value*10000
        elif unit == "mm":
            return value*10000000
        elif unit == "m":
            return value*10000000000


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

    def get_col7(self):
        return self.Column7

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
        self.Column7.clear()

    def get_name(self):
        return self.file_name

    def get_path(self):
        return self.file_path

    def set_name(self, name):
        self.file_name = name

