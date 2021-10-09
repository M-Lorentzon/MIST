import tkinter as tk
import tkinter.filedialog as filedialog
import os
import Util.Definitions as Defs
import Util.Data_Container as Data_Cont

class file_handler:

    def __init__(self, frame_info):
        self.frame_info = frame_info

        self.b_next = tk.Button(self.frame_info, text="-->", command=self.callback_next_file)
        self.b_next.config(bg=Defs.c_black, fg=Defs.c_white)
        self.b_next.grid(row=0, column=2, sticky="E")
        self.b_prev = tk.Button(self.frame_info, text="<--", command=self.callback_prev_file)
        self.b_prev.config(bg=Defs.c_black, fg=Defs.c_white)
        self.b_prev.grid(row=0, column=0, sticky="W")

        # index of the current active file!
        self.index_current_file = 0
        # file container, data and labels
        self.List_of_file_contents = []
        self.List_of_file_name_labels = []

    def remove_all_files(self):
        self.index_current_file = 0
        # remove visibility!
        for label in self.List_of_file_name_labels:
            label.grid_forget()
        self.List_of_file_contents.clear()
        self.List_of_file_name_labels.clear()


    def highlight_active_file(self):
        # Highlight active file!
        for element in self.List_of_file_name_labels:
            element.config(bg=Defs.c_file_inactive)

        if len(self.List_of_file_name_labels) != 0:
            self.List_of_file_name_labels[self.index_current_file].config(bg=Defs.c_file_active)


    def callback_prev_file(self):
        if self.index_current_file != 0 :
            self.index_current_file -= 1
        self.highlight_active_file()

    def callback_next_file(self):
        no_files = len(self.List_of_file_contents)
        if self.index_current_file >= no_files - 1:
            return
        else:
            self.index_current_file += 1

        self.highlight_active_file()

    def get_current_data(self):
        return self.List_of_file_contents[self.index_current_file]


    def new_file(self) :
        f_list = filedialog.askopenfiles(mode="r")

        for f in f_list:
            if f is not None:
                lines = f.read().splitlines() #list of lines without \n.
                label = tk.Label(self.frame_info, text=os.path.basename(f.name))

                self.List_of_file_contents.append(Data_Cont.Data_Container_2_Columns(lines, os.path.basename(f.name)))
                self.List_of_file_name_labels.append(label)
            else:
                print("Nothing opened")

            for l in self.List_of_file_name_labels:
                l.grid()

            # Update to newest list!
            self.index_current_file = len(self.List_of_file_name_labels) - 1
            self.highlight_active_file()

    def save_file(self, list_of_strings):
        f = filedialog.asksaveasfile(mode="w", defaultextension=".csv", filetypes=(("Text file", "*.txt"), ("Comma separated file", "*.csv"), ("All files", "*.*")))
        if f is None:
            return
        for s in list_of_strings :
            f.write(s + "\n")

