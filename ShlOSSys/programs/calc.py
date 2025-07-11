import customtkinter as ctk
import tkinter as tk
from datetime import datetime
from tkinter import messagebox
import math

# App settings
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

# Custom colors
PRIMARY_COLOR = "#6A0DAD"
BUTTON_COLOR = "#9B30FF"
FONT = ("Segoe UI", 14)

class CalculatorApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.geometry("381x407")
        self.title("Purple Calculator")

        self.scientific_mode = False
        self.current_view = "calculator"

        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.create_calculator_view()

    def create_calculator_view(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        self.current_view = "calculator"

        self.entry = ctk.CTkEntry(self.main_frame, font=("Segoe UI", 22), justify="right", corner_radius=10, fg_color="white", text_color="black", height=40)
        self.entry.grid(row=0, column=0, columnspan=4, padx=5, pady=5, sticky="ew")

        buttons = [
            ("7", 1, 0), ("8", 1, 1), ("9", 1, 2), ("/", 1, 3),
            ("4", 2, 0), ("5", 2, 1), ("6", 2, 2), ("*", 2, 3),
            ("1", 3, 0), ("2", 3, 1), ("3", 3, 2), ("-", 3, 3),
            ("0", 4, 0), (".", 4, 1), ("=", 4, 2), ("+", 4, 3),
        ]

        for (text, row, col) in buttons:
            ctk.CTkButton(self.main_frame, text=text, command=lambda t=text: self.on_button_click(t), fg_color=PRIMARY_COLOR, text_color="white", font=FONT, height=40).grid(row=row, column=col, padx=3, pady=3, sticky="nsew")

        self.main_frame.grid_rowconfigure(list(range(5)), weight=1)
        self.main_frame.grid_columnconfigure(list(range(4)), weight=1)

        self.mode_button = ctk.CTkButton(self.main_frame, text="Toggle Scientific", command=self.toggle_scientific_mode, fg_color=BUTTON_COLOR, font=FONT, height=30)
        self.mode_button.grid(row=5, column=0, columnspan=2, padx=5, pady=5, sticky="ew")

        self.date_button = ctk.CTkButton(self.main_frame, text="Date Calculator", command=self.create_date_calculator_view, fg_color=BUTTON_COLOR, font=FONT, height=30)
        self.date_button.grid(row=5, column=2, columnspan=2, padx=5, pady=5, sticky="ew")

        if self.scientific_mode:
            sci_buttons = [
                ("sin", 6, 0), ("cos", 6, 1), ("tan", 6, 2), ("sqrt", 6, 3),
            ]
            for (text, row, col) in sci_buttons:
                ctk.CTkButton(self.main_frame, text=text, command=lambda t=text: self.on_scientific_click(t), fg_color=PRIMARY_COLOR, text_color="white", font=FONT, height=30).grid(row=row, column=col, padx=3, pady=3, sticky="nsew")

            self.main_frame.grid_rowconfigure(6, weight=1)

    def toggle_scientific_mode(self):
        self.scientific_mode = not self.scientific_mode
        self.create_calculator_view()

    def on_button_click(self, char):
        if char == "=":
            try:
                result = eval(self.entry.get())
                self.entry.delete(0, tk.END)
                self.entry.insert(0, str(result))
            except:
                messagebox.showerror("Error", "Invalid expression")
        else:
            self.entry.insert(tk.END, char)

    def on_scientific_click(self, func):
        try:
            val = float(self.entry.get())
            result = {
                "sin": math.sin,
                "cos": math.cos,
                "tan": math.tan,
                "sqrt": math.sqrt
            }[func](math.radians(val) if func in ["sin", "cos", "tan"] else val)

            self.entry.delete(0, tk.END)
            self.entry.insert(0, str(result))
        except:
            messagebox.showerror("Error", "Invalid input for scientific operation")

    def create_date_calculator_view(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        self.current_view = "date_calculator"

        ctk.CTkLabel(self.main_frame, text="Enter Date (YYYY-MM-DD):", font=FONT).pack(pady=10)
        date_entry = ctk.CTkEntry(self.main_frame, font=FONT)
        date_entry.pack(pady=5)

        def calculate_days():
            try:
                input_date = datetime.strptime(date_entry.get(), "%Y-%m-%d")
                today = datetime.today()
                delta = today - input_date
                messagebox.showinfo("Date Difference", f"{abs(delta.days)} days")
            except:
                messagebox.showerror("Error", "Invalid date format")

        ctk.CTkButton(self.main_frame, text="Calculate", command=calculate_days, fg_color=BUTTON_COLOR, font=FONT).pack(pady=10)
        ctk.CTkButton(self.main_frame, text="Back to Calculator", command=self.create_calculator_view, fg_color=PRIMARY_COLOR, font=FONT).pack(pady=5)


if __name__ == "__main__":
    app = CalculatorApp()
    app.mainloop()
