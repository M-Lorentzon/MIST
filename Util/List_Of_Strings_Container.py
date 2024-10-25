
class List_Of_Strings_Container:

    def __init__(self):
        self.String_List = []


    def get_list(self):
        return self.String_List

    def add_row_1(self, elem1, dec_places, delim):
        The_String = self.round_if_float(elem1, dec_places)
        self.String_List.append(The_String)

    def add_row_2(self, elem1, elem2, dec_places, delim):
        The_String = self.round_if_float(elem1, dec_places)
        The_String += delim
        The_String += self.round_if_float(elem2, dec_places)
        self.String_List.append(The_String)

    def add_row_3(self, elem1, elem2, elem3, dec_places, delim):
        The_String = self.round_if_float(elem1, dec_places)
        The_String += delim
        The_String += self.round_if_float(elem2, dec_places)
        The_String += delim
        The_String += self.round_if_float(elem3, dec_places)
        self.String_List.append(The_String)

    def add_row_4(self, elem1, elem2, elem3, elem4, dec_places, delim):
        The_String = self.round_if_float(elem1, dec_places)
        The_String += delim
        The_String += self.round_if_float(elem2, dec_places)
        The_String += delim
        The_String += self.round_if_float(elem3, dec_places)
        The_String += delim
        The_String += self.round_if_float(elem4, dec_places)
        self.String_List.append(The_String)

    def add_row_5(self, elem1, elem2, elem3, elem4, elem5, dec_places, delim):
        The_String = self.round_if_float(elem1, dec_places)
        The_String += delim
        The_String += self.round_if_float(elem2, dec_places)
        The_String += delim
        The_String += self.round_if_float(elem3, dec_places)
        The_String += delim
        The_String += self.round_if_float(elem4, dec_places)
        The_String += delim
        The_String += self.round_if_float(elem5, dec_places)
        self.String_List.append(The_String)

    def add_row_6(self, elem1, elem2, elem3, elem4, elem5, elem6, dec_places, delim):
        The_String = self.round_if_float(elem1, dec_places)
        The_String += delim
        The_String += self.round_if_float(elem2, dec_places)
        The_String += delim
        The_String += self.round_if_float(elem3, dec_places)
        The_String += delim
        The_String += self.round_if_float(elem4, dec_places)
        The_String += delim
        The_String += self.round_if_float(elem5, dec_places)
        The_String += delim
        The_String += self.round_if_float(elem6, dec_places)
        self.String_List.append(The_String)

    def round_if_float(self, val, dec_pl):
        if isinstance(val, str):
            return val
        elif isinstance(val, float):
            return str(round(val, dec_pl))
        else:
            return "error"

    def clear_results(self):
        self.String_List = []







