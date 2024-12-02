import tkinter as tk
from tkinter import PhotoImage
import ttkbootstrap as ttk
import unicodedata


class UnicodeMapperApp:
    def __init__(self, root):
        self.root = root
        self.root.title("UniMapper")
        self.root.geometry("600x400")
        self.root.iconphoto(False, PhotoImage(file='../Media/UnicodeLogo.png'))

        self.search_label = ttk.Label(root, text="Search Unicode:", font=("Segoe UI Symbol", 20))
        self.search_label.pack(pady=5)

        self.search_entry = ttk.Entry(root, width=50)
        self.search_entry.insert(0, "Enter a name")
        self.search_entry.config(foreground="grey")
        self.search_entry.pack(pady=5)
        self.search_entry.bind("<FocusIn>", self.clear_placeholder)
        self.search_entry.bind("<FocusOut>", self.add_placeholder)
        self.search_entry.bind("<Return>", self.search_unicode)

        self.search_button = ttk.Button(root, text="Search", command=self.search_unicode)
        self.search_button.pack(pady=5)

        self.results_list = tk.Listbox(root, width=50, height=15)
        self.results_list.pack(pady=5)
        self.results_list.bind("<<ListboxSelect>>", self.display_character)

        self.char_display = tk.Label(root, text="", font=("Segoe UI Symbol", 30))
        self.char_display.pack(pady=5)

    def clear_placeholder(self, event):
        """Clear placeholder text on focus."""
        if self.search_entry.get() == "Enter a name":
            self.search_entry.delete(0, tk.END)
            self.search_entry.config(foreground="black")

    def add_placeholder(self, event):
        """Add placeholder text if the entry is empty."""
        if not self.search_entry.get():
            self.search_entry.insert(0, "Enter a name")
            self.search_entry.config(foreground="grey")

    def search_unicode(self):

        query = self.search_entry.get().strip().upper()
        self.results_list.delete(0, tk.END)

        if query:
            for code_point in range(0x0000, 0x10FFFF):
                try:
                    char = chr(code_point)
                    name = unicodedata.name(char)
                    if query in name:
                        self.results_list.insert(tk.END, f"U+{code_point:04X}: {char} - {name}")
                except ValueError:
                    continue

    def display_character(self, event):
        selection = self.results_list.curselection()
        if selection:
            result = self.results_list.get(selection[0])
            char = result.split(":")[1].strip().split()[0]
            self.char_display.config(text=char)


if __name__ == "__main__":
    tk_root = tk.Tk()
    app = UnicodeMapperApp(root=tk_root)
    tk_root.mainloop()
