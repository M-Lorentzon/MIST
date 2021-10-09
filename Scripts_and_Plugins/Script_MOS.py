from Util import List_Of_Strings_Container as Cont


def calculate_new_columns(Time_col, Val_col, Time1, Time2, TimeF, TimeS, Rate1, Rate2, Layers, Offset_Thickness, delim_char):
    # print("Time for first layer in bilayer", Time1)
    # print("Time for second layer in bilayer", Time2)
    # print("Time for absolutely first layer", TimeF)
    # print("Time addition for second layer", TimeS)
    # print("Rate for first layer in bilayer", Rate1)
    # print("Rate for second layer in bilayer", Rate2)
    print("Number of bilayers", Layers)
    # print("Offset_Thickness", Offset_Thickness)#

    break_indices = []  # contain the searched and found break point indices

    Result_List = Cont.List_Of_Strings_Container()
    Decimal_places = 6

    previous_target = 0
    current_target = TimeF
    T1 = 0
    T2 = 1
    added = False
    Layer_Counter = 0

    ### find breakpoints based on script inputs ###
    for i in range(len(Time_col) - 1):

        if Time_col[i + 1] > current_target:
            break_indices.append(i)
            added = True
            Layer_Counter += 1

        if added:
            previous_target = current_target
            current_target = current_target + (Time1 * (T1 % 2)) + (Time2 * (T2 % 2))
            if Layer_Counter == 1:
                current_target += TimeS
            T1 += 1
            T2 += 1
        added = False

    ### Write new list based on breakpoints ###

    current_thickness = Offset_Thickness
    Number_of_breakpoints = len(break_indices)
    print("Number_of_breakpoints :", Number_of_breakpoints)
    for i in range(Number_of_breakpoints):
        ## Relaxation!
        if i > (Layers + Layers - 1):
            print("sdfsdf")
            for k in range(break_indices[i - 1], break_indices[i]):
                thickness = current_thickness
                Result_List.add_row_6(Time_col[k], "", "", thickness, thickness, Val_col[k], Decimal_places, delim_char)


        else:
            if i == 0:
                for k in range(break_indices[0]):
                    thickness = current_thickness + Time_col[k] * Rate1
                    Result_List.add_row_6(Time_col[k], thickness, "", "", thickness, Val_col[k], Decimal_places, delim_char)
                current_thickness = thickness
            elif (i % 2) == 1:
                thickness = current_thickness
                for k in range(break_indices[i - 1], break_indices[i]):
                    thickness = current_thickness + (Time_col[k] - Time_col[break_indices[i - 1] - 1]) * Rate2
                    Result_List.add_row_6(Time_col[k], "", thickness, "", thickness, Val_col[k], Decimal_places, delim_char)
                current_thickness = thickness
            elif (i % 2) == 0:
                thickness = current_thickness
                for k in range(break_indices[i - 1], break_indices[i]):
                    thickness = current_thickness + (Time_col[k] - Time_col[break_indices[i - 1] - 1]) * Rate1
                    Result_List.add_row_6(Time_col[k], thickness, "", "", thickness, Val_col[k], Decimal_places, delim_char)
                current_thickness = thickness

            ## incomplete data for one layer (aborted MOS)
            if i == Number_of_breakpoints - 1:
                if (i % 2) == 0:
                    thickness = current_thickness
                    for k in range(break_indices[i], len(Time_col)):
                        thickness = current_thickness + (Time_col[k] - Time_col[break_indices[i] - 1]) * Rate2
                        Result_List.add_row_6(Time_col[k], "", thickness, "", thickness, Val_col[k], Decimal_places, delim_char)
                    current_thickness = thickness
                elif (i % 2) == 1:
                    thickness = current_thickness
                    for k in range(break_indices[i], len(Time_col)):
                        thickness = current_thickness + (Time_col[k] - Time_col[break_indices[i] - 1]) * Rate1
                        Result_List.add_row_6(Time_col[k], thickness, "", "", thickness, Val_col[k], Decimal_places, delim_char)
                    current_thickness = thickness

    return Result_List.get_list()


def Script_MOS(Time_col, Val_col, Time1, Time2, TimeF, TimeS, Rate1, Rate2, Layers, Offset_Thickness, delim_char):
    print("running script MOS")
    T_F = 0

    if Time1 == 0 or Time2 == 0:
        print("Must specify both T_1 and T_2!")
    if TimeF == 0:
        T_F = Time1
    else:
        T_F = TimeF

    if Layers == 0:
        return calculate_new_columns(Time_col, Val_col, float(Time1), float(Time2), float(T_F), float(TimeS), float(Rate1), float(Rate2),
                                     1000, float(Offset_Thickness), delim_char)
    else:
        return calculate_new_columns(Time_col, Val_col, float(Time1), float(Time2), float(T_F), float(TimeS), float(Rate1), float(Rate2),
                                     int(Layers), float(Offset_Thickness), delim_char)
