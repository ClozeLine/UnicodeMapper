import tkinter as tk
from tkinter import PhotoImage
import tkinter.font as TKFfont
import ttkbootstrap as ttk
import unicodedata


class UnicodeMapperApp:
    def __init__(self, root):
        self.root = root
        self.root.title("UniMapper")
        self.root.geometry("900x600")
        self.root.iconphoto(False, PhotoImage(file='../Media/UnicodeLogo.png'))

        # Search Frame
        self.search_frame = tk.Frame(
            self.root, bg="black", bd=2, relief="solid", pady=5, padx=10, width=100, height=100)
        self.search_frame.grid(row=0, column=0, columnspan=3, padx=5, pady=10, sticky="w")

        # Search Label
        self.search_label = tk.Label(self.search_frame, text="Search Unicode:", font=("Segoe UI Symbol", 20))
        self.search_label.grid(row=0, column=0, sticky="w", padx=5, pady=5)

        # Search Entry and Button
        self.search_button = ttk.Button(self.search_frame, text="Search", command=self.search_unicode)
        self.search_button.grid(row=1, column=0, padx=5, pady=5, sticky="w")

        self.root.update()
        button_width = self.search_button.winfo_width()
        button_x = self.search_button.winfo_x()

        self.search_entry = ttk.Entry(self.search_frame, width=50)
        self.search_entry.insert(0, "Enter a name")
        self.search_entry.config(foreground="grey")
        self.search_entry.grid(
            row=1, column=0, padx=(button_x + button_width), pady=5, sticky="w")
        self.search_entry.bind("<FocusIn>", self.clear_placeholder)
        self.search_entry.bind("<FocusOut>", self.add_placeholder)
        self.search_entry.bind("<Return>", self.search_unicode)

        # Results Listbox
        self.root.update()
        search_button_width = self.search_button.winfo_width()
        search_entry_width = self.search_entry.winfo_width()
        listbox_font = TKFfont.nametofont("TkFixedFont")
        char_width = listbox_font.measure("0")
        total_width = (search_button_width + search_entry_width) // char_width + 17
        self.results_list = tk.Listbox(self.search_frame, width=total_width, height=15)
        self.results_list.grid(row=2, column=0, columnspan=1, padx=5, pady=5, sticky="w")
        self.results_list.bind("<<ListboxSelect>>", self.display_character_info)

        # Character Card Box
        self.character_card_box = tk.Frame(root, bg="black", bd=2, relief="solid", pady=5, padx=10)
        self.character_card_box.grid(row=3, column=0, columnspan=3, padx=5, pady=10, sticky="ew")  # Full width
        root.grid_columnconfigure(0, weight=1)  # Expand first column
        root.grid_columnconfigure(1, weight=0)  # No stretch for button column
        root.grid_columnconfigure(2, weight=1)  # Expand last column

        # Icon Display in Card
        self.character_icon_display = tk.Frame(
            self.character_card_box, bg="black", bd=2, relief="solid", pady=5, padx=10, width=100, height=100
        )
        self.character_icon_display.grid(row=0, column=0, padx=5, pady=10, sticky="nsew")
        self.character_icon_display.pack_propagate(False)

        self.char_display = tk.Label(
            self.character_icon_display, text="", font=("Segoe UI Symbol", 70), anchor="center", bg="black", fg="white"
        )
        self.char_display.pack(expand=True, fill="both")

        # Info Display in Card
        self.character_info_display = tk.Frame(
            self.character_card_box, bg="black", bd=2, relief="solid", pady=5, padx=10
        )
        self.character_info_display.grid(row=0, column=1, padx=5, pady=10, sticky="nsew")

        # Name and Unicode Info
        self.char_name_display = tk.Label(
            self.character_info_display, text="Name: ", font=("Segoe UI Symbol", 10), anchor="w", bg="black", fg="white"
        )
        self.char_name_display.grid(row=0, column=0, padx=5, pady=5, sticky="ew")  # Stretch to fill

        self.char_unicode_display = tk.Label(
            self.character_info_display, text="Unicode: ", font=("Segoe UI Symbol", 10), anchor="w", bg="black",
            fg="white"
        )
        self.char_unicode_display.grid(row=1, column=0, padx=5, pady=5, sticky="ew")  # Stretch to fill

        self.char_unicode_dec_display = tk.Label(
            self.character_info_display, text="Unicode (dec): ", font=("Segoe UI Symbol", 10), anchor="w", bg="black",
            fg="white"
        )
        self.char_unicode_dec_display.grid(row=2, column=0, padx=5, pady=5, sticky="ew")  # Stretch to fill

        # Configure Weights
        root.grid_rowconfigure(3, weight=1)  # Make bottom card stay at the bottom

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

    def display_character_info(self, event):
        selection = self.results_list.curselection()
        if selection:
            result = self.results_list.get(selection[0])
            char = result.split(":")[1].strip().split()[0]
            self.char_display.config(text=char)
            self.char_name_display.config(text=f"Name: {unicodedata.name(char).title()}")
            self.char_unicode_display.config(text=f"Unicode: U+{ord(char):04X}")
            self.char_unicode_dec_display.config(text=f"Unicode (dec): {ord(char)}")


if __name__ == "__main__":
    tk_root = tk.Tk()
    app = UnicodeMapperApp(root=tk_root)
    tk_root.mainloop()
