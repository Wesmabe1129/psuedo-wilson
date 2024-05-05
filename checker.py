import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
import os
import time

class WidgetGenerator:
    @staticmethod
    def create_label(master, text=None, bg=None, width=None, height=None, fg=None, font=None, grid=None, pack=None, place=None):
        label = tk.Label(master, text=text, bg=bg, fg=fg, width=width, height=height, font=font)
        WidgetGenerator.set_geometry_manager(label, pack=pack, grid=grid, place=place)
        return label
    
    @staticmethod
    def create_button(master, text=None, font=None, width=None, bg=None, command=None, grid=None, pack=None, place=None, state=None):
        button = tk.Button(master, text=text, font=font, width=width, bg=bg, state=state, command=command)
        WidgetGenerator.set_geometry_manager(button, pack=pack, grid=grid, place=place)
        return button
    
    @staticmethod
    def create_entry(master, font=None, show=None, state=None, width=None, grid=None, pack=None, place=None):
        entry = tk.Entry(master, font=font, state=state, show=show, width=width)
        WidgetGenerator.set_geometry_manager(entry, pack=pack, grid=grid, place=place)
        return entry
    
    @staticmethod
    def create_listbox(master, width=None, height=None, font=None, grid=None, pack=None, place=None):
        listbox = tk.Listbox(master, width=width, height=height, font=font)
        WidgetGenerator.set_geometry_manager(listbox, pack=pack, grid=grid, place=place)
        return listbox

    @staticmethod
    def create_frame(master, width=None, height=None, bg=None, grid=None, pack=None, place=None):
        frame = tk.Frame(master, width=width, height=height, bg=bg)
        WidgetGenerator.set_geometry_manager(frame, pack=pack, grid=grid, place=place)
        return frame
    
    @staticmethod
    def configure_widget(widget, bg=None, fg=None):
        if bg:
            widget.config(bg=bg)
        if fg:
            widget.config(fg=fg)
    
    @staticmethod    
    def set_widget_measurement(widget, width=None, height=None):
        widget.config(width=width, height=height)

    @staticmethod
    def set_geometry_manager(widget, pack=None, grid=None, place=None):
        if pack:
            widget.pack(**pack)
        elif grid:
            widget.grid(**grid)
        elif place:
            widget.place(**place)
        else:
            widget.pack()

class PlagiarismChecker(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.homepage_frame = None
        self.header_frame = None
        self.footer_frame = None
        self.progress_bar = None

        self.__configure_window()
        self.show_homepage()

    def show_homepage(self):
        if self.homepage_frame:
            self.homepage_frame.destroy()

        self.show_header()

        self.homepage_frame = WidgetGenerator.create_frame(self, pack={"pady":75})

        self.doc1_label = WidgetGenerator.create_label(self.homepage_frame, text="CHECK", font=("Helvetica", 12, "bold"), grid={'row':0, 'column':0})
        self.doc1_entry = WidgetGenerator.create_entry(self.homepage_frame,  font=("Helvetica", 12), width=30, grid={'row':0, 'column':1})
        self.doc1_button = WidgetGenerator.create_button(self.homepage_frame, text="Browse...", font=("Helvetica", 10), command=self.browse_file1, grid={'row':0, 'column':2})

        self.doc2_label = WidgetGenerator.create_label(self.homepage_frame, text="ORIGINAL", font=("Helvetica", 12, "bold"), grid={'row':1, 'column':0})
        self.doc2_entry = WidgetGenerator.create_entry(self.homepage_frame, font=("Helvetica", 12), width=30, grid={'row':1, 'column':1})
        self.doc2_button = WidgetGenerator.create_button(self.homepage_frame, text="Browse...", font=("Helvetica", 10), command=self.browse_file2, grid={'row':1, 'column':2})

        self.check_btn = WidgetGenerator.create_button(self.homepage_frame, text="Check for Uniqueness", width=20, bg="powderblue", font=("Helvetica", 12), command=self.check_for_uniqueness, grid={'row':2, 'column':1, 'pady':20})

        self.progress_bar = ttk.Progressbar(self.homepage_frame, orient='horizontal', length=200, mode='determinate')
        self.progress_bar.grid(row=3, column=1, pady=10)

    def browse_file1(self):
        file_path = filedialog.askopenfilename()
        self.doc1_entry.delete(0, tk.END)
        self.doc1_entry.insert(0, file_path)

    def browse_file2(self):
        file_path = filedialog.askopenfilename()
        self.doc2_entry.delete(0, tk.END)
        self.doc2_entry.insert(0, file_path)

    def reader1(self, file_path):
        try:
            with open(file_path, 'r') as file:
                content = file.read()
            return content
        except FileNotFoundError:
            print("File not Found!")
            return None

    def reader2(self, file_path):
        try:
            with open(file_path, 'r') as file:
                content = file.read()
            return content
        except FileNotFoundError:
            print("File not Found!")
            return None

    def levenshtein_distance(self, str1, str2):
        f = len(str1)
        s = len(str2)

        if f < s:
            return self.levenshtein_distance(str2, str1)
        if s == 0:
            return f
        
        prev_row = range(s + 1)

        for i, c1 in enumerate(str1):
            current_row = [i + 1]
            for j, c2 in enumerate(str2):
                insertion = prev_row[j + 1] + 1
                deletion = current_row[j] + 1
                subtitution = prev_row[j] + (c1 != c2)

                current_row.append(min(insertion, deletion, subtitution))

            prev_row = current_row

        return prev_row[-1]

    def check_for_uniqueness(self):
        doc1 = self.doc1_entry.get()
        doc2 = self.doc2_entry.get()

        if not doc1 or not doc2:
            print("Please provide both documents")
            return

        reader1 = self.reader1(doc1)
        reader2 = self.reader2(doc2)

        # print(reader1)
        # print(reader2)

        if not reader1 or not reader2:
            print("One or both documents not found")
            return

        self.progress_bar.start(10)

        distance = self.levenshtein_distance(reader1.lower(), reader2.lower())
        length = max(len(doc1), len(doc2))
        similarity = 1 - (distance / length)

        similarity_percentage = max(0, min(100, similarity * 100))

        # Adding a delay to make the transition smoother
        self.after(1500, lambda: self.stop_progress_bar(similarity_percentage))

    def stop_progress_bar(self, similarity_percentage):
        self.progress_bar.stop()

        if similarity_percentage >= 80:
            result_text = f"PLAGIARISM DETECTED!\nSimilarity: {similarity_percentage:.2f}%"
        else:
            result_text = f"NO PLAGIARISM DETECTED\nSimilarity: 0.00%"

        result_window = tk.Toplevel(self)
        result_window.title("Plagiarism Check Result")

        result_label = tk.Label(result_window, text=result_text, font=("Helvetica", 12))
        result_label.pack(padx=20, pady=20)

    def __configure_window(self):
        self.title("PLAGIARISM CHECKER.IO")
        self.geometry("1000x75000")

    def show_header(self):
        if self.header_frame:
            self.header_frame.destroy()

        self.header_frame = WidgetGenerator.create_frame(self, pack={"pady":20, 'padx':10}, bg="powderblue")
        
        self.icon = WidgetGenerator.create_label(self.header_frame,bg="powderblue", text="PC", font=("times", 36, "bold"), pack={'fill':'both', 'expand':True})
        
        self.header = WidgetGenerator.create_label(self.header_frame, bg="powderblue",text="PLAGIARISM CHECKER", font=("times", 16, "bold"))
        
    def show_footer(self):
        self.footer_frame = WidgetGenerator.create_frame(self, pack={'side':'bottom'})

if __name__=="__main__":
    pc = PlagiarismChecker()
    pc.mainloop()
