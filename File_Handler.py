import tkinter as tk
import tkscrolledframe as SF
import tkinter.filedialog as filedialog
import os
import Util.Definitions as Defs
import Util.Data_Container as Data_Cont
from pathlib import Path

class file_handler:

    def __init__(self, frame_info_file_handler):
        self.frame_info_file_handler = frame_info_file_handler

        self.b_next = tk.Button(self.frame_info_file_handler, text="-->", command=self.callback_next_file)
        self.b_next.config(bg=Defs.c_black, fg=Defs.c_white)
        self.b_next.grid(row=0, column=2, sticky="E")
        self.b_prev = tk.Button(self.frame_info_file_handler, text="<--", command=self.callback_prev_file)
        self.b_prev.config(bg=Defs.c_black, fg=Defs.c_white)
        self.b_prev.grid(row=0, column=0, sticky="W")
        self.l_info = tk.Label(self.frame_info_file_handler, text="Available files", bg=Defs.c_frame_color, fg="white")
        self.l_info.config()
        self.l_info.grid(row=0, column=1, sticky="W")

        self.sframe = SF.ScrolledFrame(self.frame_info_file_handler, width=210, height=400)
        self.sframe.grid(row=1, column=0, columnspan=3)
        self.sframe.config(bg=Defs.c_frame_color)
        self.sframe.bind_arrow_keys(self.frame_info_file_handler)
        self.sframe.bind_scroll_wheel(self.frame_info_file_handler)
        self.inner_frame = self.sframe.display_widget(tk.Frame)

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

    def check_if_image_file(self, string):
        list_of_file_endings = [".tif", ".jpg"]
        if string in list_of_file_endings:
            return True
        else:
            return False

    def new_file(self) :
        f_list = filedialog.askopenfiles(mode="r")

        for f in f_list:
            if f is not None:
                label = tk.Label(self.inner_frame, text=os.path.basename(f.name))

                if self.check_if_image_file(Path(f.name).suffix):
                    empty_list = []
                    self.List_of_file_contents.append(Data_Cont.Data_Container(empty_list, os.path.basename(f.name), f.name))
                    self.List_of_file_name_labels.append(label)
                else:
                    lines = f.read().splitlines() #list of lines without \n.

                    self.List_of_file_contents.append(Data_Cont.Data_Container(lines, os.path.basename(f.name), f.name))
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

