import tkinter as tk
from tkinter.scrolledtext import ScrolledText

class Error_Handler :
    def __init__(self, frame):
        self.frame = frame

        self.error_text = ScrolledText(self.frame, width=26, height=16)
        self.error_text.grid(row=0, column=0)
        self.error_text.config(state="normal")


    def Write_Error_Text(self, text):
        self.error_text.insert("end", "\n\n")
        self.error_text.insert("end", text, 'error')
        self.error_text.tag_config('error', foreground='red')
        self.error_text.yview('end')

    def Write_notification(self, text):
        self.error_text.insert("end", "\n\n")
        self.error_text.insert("end", text, 'notice')
        self.error_text.tag_config('notice', foreground='black')
        self.error_text.yview('end')
