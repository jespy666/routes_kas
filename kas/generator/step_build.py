def build_step(
        start: str,
        departure: str,
        distance: int,
        end: str,
        arriving: str
) -> dict:
    return {
        'from_AZK': start,
        'departure': departure,
        'distance': distance,
        'to_AZK': end,
        'arriving': arriving
    }


def build_day(day: str,
              departure: str,
              arriving: str,
              fuel_at_start: float,
              fuel_at_end: float,
              refill: None | float,
              odo_at_start: int,
              odo_at_end: int,
              consumption_per_day: float,
              cover: int,
              path_number: int,
              steps: list) -> dict:
    """forming the day dict"""
    return {day: {
        'departure': departure,
        'arriving': arriving,
        'fuel_at_start': fuel_at_start,
        'fuel_at_end': fuel_at_end,
        'refill': refill,
        'odo_at_start': odo_at_start,
        'odo_at_end': odo_at_end,
        'consumption_per_day': consumption_per_day,
        'cover': cover,
        'path_number': path_number,
        'steps': steps
    }}
