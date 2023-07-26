def get_departures(data: list) -> dict:
    departures: dict = {}
    for i in data:
        for key, value in i.items():
            departures[key] = value.get('departure')
    return departures
