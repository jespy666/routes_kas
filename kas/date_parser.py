
import json


def get_date():
    date = kas.date.get()
    date.split('/')
    with open('kas/user_data/date.json', 'w') as file:
        json.dump({date[0]: date[-1]}, file)
