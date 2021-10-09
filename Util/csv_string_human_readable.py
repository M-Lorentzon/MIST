
def csv_to_human_readable(string, column_width):
    result = ""
    split_list = string.split(",")

    for element in split_list :

        # append the element and
        # if too short a word then append white space
        temp = element
        while len(temp) < column_width:
            temp += " "
        result += temp

    return result


