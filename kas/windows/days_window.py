import tkinter as tk
from tkinter import messagebox

from kas.parser import parse
from kas.chunker import Chunked
from kas.distributor import DistributeFuel
from kas.generator.generator import GenerateRoutes
from kas.departures import get_departures
from kas.page_builder import write_to_pdf


class DaysWindow:

    routes = list

    def __init__(self, parent, days_count):
        self.root = tk.Toplevel(parent)
        self.root.title('Day\'s')
        self.root.geometry(f'{1100}x{600}')
        self.root.resizable(False, False)
        self.root.configure(bg='#285888')

        self.days_count = days_count

        self.main_frame = tk.Frame(self.root, background='#285888')
        self.main_frame.pack(pady=20)

        self.buttons_frame = tk.Frame(self.root, background='#285888')
        self.buttons_frame.pack(pady=10)

        self.entries = []

        self.buttons = [
            tk.Button(
                self.main_frame,
                text=f'Day {day}',
                bg='red',
                font=('Cascadia Code SemiBold', 10),
                height=4,
                width=10,
                command=lambda day=day: self.save_day(day)
            ) for day in range(1, self.days_count + 1)
        ]

        self.apply_month_button = tk.Button(
            self.buttons_frame,
            text='Confirm all day\'s data',
            command=self.generate,
            width=20,
            height=3,
            font=('Arial black', 8)
        )

        self.write_button = tk.Button(
            self.buttons_frame,
            text='Get PDF file',
            state=tk.DISABLED,
            relief=tk.SUNKEN,
            command=self.write_pdf,
            font=('Arial black', 8)
        )

        self.grab_focus()

    def grab_focus(self):
        self.setup_gui()
        self.root.wait_visibility()
        self.root.grab_set()
        self.root.focus_set()
        self.root.wait_window()

    def setup_gui(self):
        current_row = 0
        current_column = 0
        last_row = 0
        for day, button in enumerate(self.buttons, 1):
            button.grid(row=current_row, column=current_column,
                        padx=10, pady=10)
            current_column += 1
            if day % 10 == 0:
                current_row += 1
                current_column = 0
            last_row += 1

        self.apply_month_button.grid(row=last_row, column=0)
        self.write_button.grid(row=last_row + 1, column=0, pady=20)

    def save_day(self, day: int):

        def save_dial() -> dict:
            data = {
                'departure': departure_entry.get(),
                'refueling_time': time_entry.get(),
                'refueling_station': station_entry.get(),
                'ltr': fuel_entry.get(),
            }
            return data

        dial = tk.Toplevel(self.root)
        dial.title('Entry day data')
        dial.geometry(f'{250}x{320}')

        def on_dial_close():
            dial.grab_release()
            dial.destroy()

        dial.protocol("WM_DELETE_WINDOW", on_dial_close)

        departure_label = tk.Label(dial, text='Departure')
        departure_label.pack(pady=7)
        departure_entry = tk.Entry(dial)
        departure_entry.pack(pady=7)

        station_label = tk.Label(dial, text='Refill station')
        station_label.pack(pady=7)
        station_entry = tk.Entry(dial)
        station_entry.pack(pady=7)

        time_label = tk.Label(dial, text='Refill time')
        time_label.pack(pady=7)
        time_entry = tk.Entry(dial)
        time_entry.pack(pady=7)

        fuel_label = tk.Label(dial, text='Ltr')
        fuel_label.pack(pady=7)
        fuel_entry = tk.Entry(dial)
        fuel_entry.pack(pady=7)

        save_button = tk.Button(
            dial,
            text='Save',
            command=lambda: self.on_save(dial, day, save_dial())
        )
        save_button.pack(pady=10)
        dial.grab_set()

    def on_save(self, dial, day, data):

        def check_exist_day(key: str, arr: list):
            keys_list = [key for item in arr for key in item.keys()]
            return False if key not in keys_list else keys_list.index(key)

        empty_count = sum(value == '' for value in data.values())
        wrong_counts = [1, 2, 4]

        if empty_count in set(wrong_counts):
            messagebox.showwarning(
                title='Error!',
                message='You didn\'t enter anything.'
                        ' At least "Departure" field must be filled!'
            )
        else:
            index = check_exist_day(str(day), self.entries)
            if index is not False:
                self.entries.pop(index)
            self.entries.append({str(day): data})

            self.buttons[day - 1].configure(
                bg='green',
                fg='white'
            )

            dial.destroy()

    def generate(self):
        data = sorted(self.entries, key=lambda x: int(list(x.keys())[0]))
        initial_data = parse('input.json', fixtures=False)
        initial_fuel = initial_data.get('fuel')
        initial_odo = initial_data.get('odo')
        path_list = initial_data.get('path_number')

        departures = get_departures(data)

        chunks = Chunked(data)
        fuels = DistributeFuel(chunks.chunked(), initial_fuel)
        generated = GenerateRoutes(
            fuels.distribute(),
            initial_fuel,
            departures,
            initial_odo,
            path_list
        )

        output = generated.generate()[0]

        self.routes = output

        self.write_button.configure(state=tk.ACTIVE, relief=tk.RAISED)

    def write_pdf(self):
        write_to_pdf(self.routes)
