from tkinter import *
from tkinter.ttk import Combobox
import json
import os
from kas.user_data import USER_DIR
from kas.database.vehicles import VEHICLES
from kas.windows.days_window import DaysWindow


class MainWindow:

    def __init__(self, width, height, title='Routes Calculator',
                 resizable=(False, False)):
        self.win = Tk()
        self.win['bg'] = '#3761E8'
        self.win.title(title)
        self.win.geometry(f'{width}x{height}+200+200')
        self.win.resizable(resizable[0], resizable[1])

        self.odo = Entry(self.win, font='Consolas 12', width=10)
        self.path_number = Entry(self.win, font='Consolas 12', width=10)
        self.fuel = Entry(self.win, font='Consolas 12', width=10)
        self.date = Entry(self.win, font='Consolas 12', width=10)

        self.odo_label = Label(self.win, text='km',
                               width=10, font=('Arial', 10))
        self.number_label = Label(self.win, text='№ list: xxx',
                                  width=10, font=('Arial', 10))
        self.fuel_label = Label(self.win, text='ltr', width=10,
                                font=('Arial', 10))
        self.date_label = Label(self.win, text='mm/yyyy',
                                width=10, font=('Arial', 10))

        vehicles = [car for car, rate in VEHICLES.items()]
        vehicles_var = StringVar(value=vehicles[0])

        self.vehicles_label = Label(self.win, text='Choose vehicle',
                                    width=10, font=('Arial', 10))
        self.vehicles = Combobox(self.win, values=vehicles, width=12,
                                 state='readonly', textvariable=vehicles_var)

    def run(self):
        self.setup_gui()
        self.win.mainloop()

    def setup_gui(self):
        self.odo.grid(row=0, column=1)
        self.path_number.grid(row=0, column=2)
        self.fuel.grid(row=0, column=3)
        self.date.grid(row=0, column=4)

        self.odo_label.grid(row=1, column=1)
        self.number_label.grid(row=1, column=2)
        self.fuel_label.grid(row=1, column=3)
        self.date_label.grid(row=1, column=4)

        self.vehicles_label.grid(row=0, column=5)

        self.vehicles.current(0)
        self.vehicles.grid(row=1, column=5, padx=4)
        self.vehicles.bind('<<ComboboxSelected>>', self.apply_vehicle)

        Button(self.win, text='Save', height=1, width=35,
               command=self.save_data).\
            grid(row=3, column=2, columnspan=2)

        Button(self.win, text='Go to days--->',
               height=1, width=35, command=self.create_days_window).\
            grid(row=4, column=3, columnspan=2)

    def save_data(self):
        user_odo = int(self.odo.get())
        user_path_number = int(self.path_number.get())
        user_fuel = float(self.fuel.get())
        user_date = self.date.get()
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

    def apply_vehicle(self, event):
        data = self.vehicles.get()
        return data

    def create_days_window(self, width=1000, height=800,
                           title='Days', resizable=(True, True)):
        DaysWindow(self.win, width, height, title, resizable)


if __name__ == '__main__':
    window = MainWindow(650, 400)
    window.run()
