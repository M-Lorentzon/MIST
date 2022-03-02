import user_config.popup_settings as popup
import user_config.PDF_Data as container
import json

class PDF_Settings_Handler:

    def __init__(self, parent):
        self.Parent = parent

        self.PDF_Data_Containers = []  # List of containers
        self.active_pdf = [] # Must be same size as number of PDF-buttons!

        self.Parse_json_settings()


    def Open_Settings(self):
        popup.popup_settings(self)


    def Parse_json_settings(self):
        with open("user_config/json_xrd_pdf.txt", 'r') as infile:
            data = json.load(infile)
            for card in data['PDF_Card']:
                # print("Material: ", card['Material'])
                # print("Peak_tuples: ", card['Peak_tuples'])
                # print("Active_peak_index: ", card['Active_peak_index'])
                self.PDF_Data_Containers.append(container.PDF_Data(
                                                card['Material'], card['Peak_tuples'], card['Active_peak_index']))
            for globalsetting in data['Global']:
                # print("Active_PDF_Index: ", globalsetting['Active_PDFs_Index'])
                self.active_pdf = globalsetting['Active_PDFs_Index']

    def get_active_pdf_container(self, index):
        if index < 4:
            return self.PDF_Data_Containers[self.active_pdf[index]]

    def add_new_pdf_data(self, data):
        # print(data.name)
        # print(data.get_list_of_data())
        # print(data.get_list_of_active_indices())
        self.PDF_Data_Containers.append(data)

        self.Save_data_to_json_file()

    def Assert_active_indices_within_bounds(self):
        max_index = len(self.PDF_Data_Containers) - 1

        for i in range(len(self.active_pdf)):
            if self.active_pdf[i] > max_index:
                self.active_pdf[i] = 0

    def Save_data_to_json_file(self):

        Aggregated_Data = {}
        Aggregated_Data['Global'] = []
        Aggregated_Data['PDF_Card'] = []

        # "global" settings
        Aggregated_Data['Global'].append(
            {
                "Active_PDFs_Index": self.active_pdf
            }
        )

        # PDF-card data
        for data in self.PDF_Data_Containers:
            Aggregated_Data['PDF_Card'].append(
                {
                    "Material": data.name,
                    "Peak_tuples": data.get_list_of_data(),
                    "Active_peak_index": data.get_list_of_active_indices()
                }
            )

        with open("user_config/json_xrd_pdf.txt", "w") as outfile:
            json.dump(Aggregated_Data, outfile, indent=4)

    def Update_PDF_Buttons(self):
        self.Parent.Update_PDF_Buttons()

