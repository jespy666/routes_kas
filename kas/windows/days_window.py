import tkinter as tk
from tkinter import ttk
import json
import calendar
from kas.user_data import USER_DIR
import os
from kas.parser import parse

from kas.chunker import Chunked
from kas.distributor import DistributeFuel
from kas.generator import GenerateRoutes
from kas.departures import get_departures
from kas.page_builder import write_to_pdf


class DaysWindow:

    def __init__(self, parent, title='Fill Days',
                 resizable=(False, False)):
        self.win = tk.Toplevel(parent)
        self.win.title(title)
        self.win.geometry(
            "{0}x{1}+0+0".format(
                self.win.winfo_screenwidth(),
                self.win.winfo_screenheight()
            )
        )
        self.win.resizable(resizable[0], resizable[1])
        self.win['bg'] = '#285888'
        self.row_entries = []

        self.pdf_writer_button = tk.Button(self.win, text='Get PDF',
                                           command=self.handle_data,
                                           state=tk.DISABLED, width=10)
        self.create_labels()
        self.grab_focus()

    def grab_focus(self):
        self.win.wait_visibility()
        self.win.grab_set()
        self.win.focus_set()
        self.win.wait_window()

    @staticmethod
    def get_days_count():
        user_file = os.path.abspath(os.path.join(USER_DIR, 'input.json'))

        with open(user_file, 'r') as r:
            data = r.read()

        user_data = json.loads(data)
        user_date = user_data.get('date')
        month, year = user_date.split('/')[0], user_date.split('/')[1]
        return calendar.monthrange(int(year), int(month))[1]

    def save_data(self):
        days = []
        for row_data in self.row_entries:
            day = row_data['day']
            departure_entry = row_data['departure_entry']
            refueling_time_entry = row_data['refueling_time_entry']
            refueling_station_entry = row_data['refueling_station_entry']
            ltr_entry = row_data['ltr']
            check = row_data['is_exist'].get()
            is_exist = True if check == 1 else False

            departure_value = departure_entry.get()
            refueling_time_value = refueling_time_entry.get()
            refueling_station_value = refueling_station_entry.get()
            ltr_value = ltr_entry.get()

            rows = {
                day: {
                    'is_exist': is_exist,
                    'departure': departure_value,
                    'refueling_time': refueling_time_value,
                    'refueling_station': refueling_station_value,
                    'ltr': ltr_value
                }
            }
            days.append(rows)

        days_file = os.path.abspath(os.path.join(USER_DIR, 'by_days.json'))
        with open(days_file, 'w') as f:
            json.dump(days, f)

        self.pdf_writer_button.config(state=tk.NORMAL)

    @staticmethod
    def handle_data():
        input_data = parse('initial_data1.json', fixtures=True)
        data = parse('data1.json', fixtures=True)
        fuel = input_data.get('fuel')
        odo = input_data.get('odo')
        path_number = input_data.get('path_number')
        departures = get_departures(data)
        chunks = Chunked(data)
        chunks.filter()
        fuels = DistributeFuel(chunks.chunked(), fuel)
        routes = GenerateRoutes(fuels.distribute(), fuel,
                                departures, odo, path_number)
        result = routes.generate_routes()
        write_to_pdf(result[0])

    def create_labels(self):
        days_count = self.get_days_count()

        for day in range(1, days_count + 1):
            check_var = tk.IntVar()
            check_button = ttk.Checkbutton(self.win, variable=check_var,
                                           text=day)
            departure_label = tk.Label(self.win, text='Departure Time:',
                                       width=12, relief=tk.GROOVE)
            departure_entry = tk.Entry(self.win, font='Consolas 12', width=8)
            refueling_time_label = tk.Label(self.win, text='Refueling Time:',
                                            width=12, relief=tk.GROOVE)
            refueling_time_entry = tk.Entry(self.win, font='Consolas 12',
                                            width=8)
            refueling_station_label = tk.Label(self.win, text='Refueling AZK:',
                                               width=12, relief=tk.GROOVE)
            refueling_station_entry = tk.Entry(self.win, font='Consolas 12',
                                               width=8)
            ltr_label = tk.Label(self.win, text='ltr:', width=12,
                                 relief=tk.GROOVE)
            ltr_entry = tk.Entry(self.win, font='Consolas 12', width=8)

            check_button.grid(row=day, column=1, columnspan=2)
            departure_label.grid(row=day, column=5)
            departure_entry.grid(row=day, column=6)
            refueling_time_label.grid(row=day, column=7)
            refueling_time_entry.grid(row=day, column=8)
            refueling_station_label.grid(row=day, column=9)
            refueling_station_entry.grid(row=day, column=10)
            ltr_label.grid(row=day, column=11)
            ltr_entry.grid(row=day, column=12)

            row_data = {
                'day': day,
                'departure_entry': departure_entry,
                'refueling_time_entry': refueling_time_entry,
                'refueling_station_entry': refueling_station_entry,
                'ltr': ltr_entry,
                'is_exist': check_var
            }
            self.row_entries.append(row_data)

        apply_button = tk.Button(self.win, text='Apply',
                                 command=self.save_data, width=10)
        apply_button.grid(row=days_count+1, column=5, rowspan=20)

        self.pdf_writer_button.grid(row=days_count+1, column=6, rowspan=20)
