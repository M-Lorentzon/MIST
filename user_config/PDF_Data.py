

class PDF_Data:

    def __init__(self, name, list_of_data, list_of_active_index):
        self.name = name
        self.list_of_data = list_of_data
        self.list_of_active_index = list_of_active_index

        self.list_size = len(self.list_of_data)

    def get_list_of_data(self):
        return self.list_of_data

    def get_list_of_active_indices(self):
        return self.list_of_active_index

    def get_list_of_active_data(self):
        temp = []
        for index in self.list_of_active_index:
            temp.append(self.list_of_data[index])
        return temp

