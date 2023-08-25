import tkinter as tk
from tkinter.ttk import Combobox
from tkinter import messagebox

import json
import os
import math
from calendar import monthrange

from kas.user_data import USER_DIR
from kas.windows.days_window import DaysWindow


class MainWindow:

    days_count = math.inf

    def __init__(self):
        self.win = tk.Tk()
        self.win.title('Routes Generator')
        self.win.geometry(f'{491}x{491}')
        self.win.resizable(False, False)
        self.win.configure(bg='#285888')

        self.frame = tk.Frame(self.win)

        self.user_info_frame = tk.LabelFrame(self.frame, text='User info')
        self.date_label = tk.Label(
            self.user_info_frame,
            text='Month / Year',
            background='#285888',
            font=('Candara', 12),
            fg='white'
        )
        self.date_entry = tk.Entry(self.user_info_frame)

        self.vehicles = ['Logan', 'Sportage']
        self.vehicles_var = tk.StringVar(value=self.vehicles[0])
        self.vehicles_label = tk.Label(
            self.user_info_frame,
            text='Vehicle',
            background='#285888',
            font=('Candara', 12),
            fg='white'
        )
        self.vehicles_combobox = Combobox(
            self.user_info_frame,
            values=self.vehicles,
            state='readonly',
            textvariable=self.vehicles_var
        )

        self.data_info_frame = tk.LabelFrame(self.frame,
                                             text='Data from last month')
        self.odo_label = tk.Label(
            self.data_info_frame,
            text='Current ODO',
            background='#285888',
            font=('Candara', 12),
            fg='white'
        )
        self.odo_entry = tk.Entry(self.data_info_frame)

        self.fuel_label = tk.Label(
            self.data_info_frame,
            text='Current fuel',
            background='#285888',
            font=('Candara', 12),
            fg='white'
        )
        self.fuel_entry = tk.Entry(self.data_info_frame)

        self.path_list_label = tk.Label(
            self.data_info_frame,
            text='Path list',
            background='#285888',
            font=('Candara', 12),
            fg='white'
        )
        self.path_list_spinbox = tk.Spinbox(
            self.data_info_frame,
            from_=1,
            to=365
        )

        self.save_button = tk.Button(
            self.data_info_frame,
            text='Save',
            width=16,
            command=self.save_data,
            relief=tk.RAISED,
            font=('Arial black', 10)
        )

        self.days_button = tk.Button(
            self.frame,
            text='Open day\'s window',
            width=16,
            command=self.create_days_window,
            relief=tk.SUNKEN,
            font=('Candara', 12),
            state=tk.ACTIVE
        )

    def run(self):
        self.setup_gui()
        self.win.mainloop()

    def setup_gui(self):

        self.frame.configure(background='#285888')
        self.frame.pack()
        self.frame.pack_configure(side='bottom', pady=20)

        self.user_info_frame.configure(
            background='#285888',
            font=('Consolas', 12),
            fg='white'
        )
        self.user_info_frame.grid(row=0, column=0, padx=15, pady=15)

        self.date_label.grid(row=0, column=0)
        self.date_entry.grid(row=1, column=0)

        self.vehicles_combobox.current(0)
        self.vehicles_combobox.bind('<<ComboboxSelected>>', self.apply_vehicle)
        self.vehicles_label.grid(row=0, column=1)
        self.vehicles_combobox.grid(row=1, column=1)

        for widget in self.user_info_frame.winfo_children():
            widget.grid_configure(padx=10, pady=10)

        self.data_info_frame.configure(
            background='#285888',
            font=('Consolas', 12),
            fg='white'
        )
        self.data_info_frame.grid(row=1, column=0, padx=15, pady=15)

        self.odo_label.grid(row=0, column=0)
        self.odo_entry.grid(row=1, column=0)

        self.fuel_label.grid(row=0, column=1)
        self.fuel_entry.grid(row=1, column=1)

        self.path_list_label.grid(row=0, column=2)
        self.path_list_spinbox.grid(row=1, column=2)

        for widget in self.data_info_frame.winfo_children():
            widget.grid_configure(padx=5, pady=10)

        self.save_button.grid(row=2, column=1, pady=10)

        self.days_button.grid(row=3, column=0, sticky='news', pady=10, padx=20)

    def save_data(self):
        try:
            user_odo = int(self.odo_entry.get())
            user_path_number = int(self.path_list_spinbox.get())
            user_fuel = float(self.fuel_entry.get())
            user_date = self.date_entry.get()
            user_vehicle = self.apply_vehicle(None)

            data = {
                "odo": user_odo,
                "path_number": user_path_number,
                "fuel": user_fuel,
                "date": user_date,
                "vehicle": user_vehicle
            }

            file_path = os.path.abspath(os.path.join(USER_DIR, 'input.json'))

            with open(file_path, 'w') as f:
                json.dump(data, f)

            self.days_count = self.get_days_count(user_date)

            self.days_button.configure(relief=tk.RAISED, state=tk.ACTIVE)

        except ValueError:
            messagebox.showwarning(
                title='Error!',
                message='One of the fields is incorrect!\n'
                        'Here\'s a filling examples:\n\n'
                        ' Date: mm/yyyy\n'
                        ' ODO: 0 - 999999\n'
                        ' Fuel: 00.00\n'
                        ' Path list: 0 - 365'

            )

    def apply_vehicle(self, event):
        data = self.vehicles_var.get()
        return data

    @staticmethod
    def get_days_count(date: str):
        month, year = date.split('/')[0], date.split('/')[1]
        return monthrange(int(year), int(month))[1]

    def create_days_window(self):
        DaysWindow(self.win, self.days_count)


if __name__ == '__main__':
    window = MainWindow()
    window.run()
