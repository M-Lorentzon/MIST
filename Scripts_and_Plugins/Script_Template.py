from Util import List_Of_Strings_Container as Cont


def calculate_new_columns(Angle_col, Intensity_col, delim_char):

    # Create a new list of strings containing the result.
    Result_List = Cont.List_Of_Strings_Container()

    # Perform necessary calculations and write rows to the list
    # e.g. "Result_List.add_row_6(Val1, Val2, Val3, Val4, Val5, Val6, delim_char)"

    # Return the created list!
    return Result_List.get_list()


def Script_Template(Angle_col, Intensity_col, delim_char):
    # Do potential initial checks for the script to work properly.

    # return a complete list of strings containing the result.
    return calculate_new_columns(Angle_col, Intensity_col, delim_char)


