from Util import List_Of_Strings_Container as Cont
import math


def calculate_new_columns(Angle_col, Intensity_col, offset, delim_char):

    # Create a new list of strings containing the result.
    Result_List = Cont.List_Of_Strings_Container()
    Decimal_places = 5

    # Perform calculation for each element in the intensity column!
    # Write a new row containing the calculation results.
    for i in range(len(Intensity_col)):
        sqrt = math.sqrt(Intensity_col[i])
        log = math.log10(Intensity_col[i])
        log_offs = offset + math.log10(Intensity_col[i])
        Result_List.add_row_5(Angle_col[i], Intensity_col[i], sqrt, log, log_offs, Decimal_places, delim_char)

    # Return the created list!
    return Result_List.get_list()


def Script_XRD1(Angle_col, Intensity_col, offset, delim_char):
    # Do potential initial checks for the script to work properly.
    print("running script XRD1")

    # return a complete list of strings containing the result.
    return calculate_new_columns(Angle_col, Intensity_col, offset, delim_char)


