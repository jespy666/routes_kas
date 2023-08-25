from datetime import datetime, timedelta
from kas.database import distances


MAX_CITY_CONSUMPTION = 25.00


def calculate_distance(consumption: float, ride_type: str = 'city'):
    """convert consumption into distance"""
    if ride_type == 'city':
        return int(round(consumption / (12.14 / 100)))
    return int(round(consumption / (9.84 / 100)))


def calculate_travel_time(distance: int, departure: str, ride_type: str):
    if ride_type == 'city':
        match distance:
            case d if d < 10:
                speed = 30
            case d if 10 <= d < 30:
                speed = 40
            case _:
                speed = 50
    else:
        speed = 70
    travel_time = (distance / speed) * 60
    departure_time = datetime.strptime(departure, '%H:%M')
    updated_time = departure_time + timedelta(minutes=travel_time)
    return updated_time.strftime('%H:%M')


def get_departure(time: str, refill: str = None) -> str:
    """calculated time from arriving the point to departure.
        The named param: refill are setting refill time"""
    departure_time = datetime.strptime(time, '%H:%M')
    if not refill:
        parking_time = 40
        updated = departure_time + timedelta(minutes=parking_time)
    else:
        refill_time = datetime.strptime(refill, '%H:%M')
        updated = refill_time + timedelta(minutes=10)
    return updated.strftime('%H:%M')


def get_header_distance(point: str, type_='city') -> int:
    """returned distance from header to first point.
        The named param: type_
        are indicate the type of ride: city or country."""
    if type_ == 'city':
        distance = [value for key, value
                    in distances.DISTANCES_INSIDE_CITY.items()
                    if key == point][0]
    else:
        distance = [value for key, value
                    in distances.DISTANCES_OUTSIDE_CITY.items()
                    if key == point][0]

    return distance


def get_point_from_header(distance: int, type_='city') -> str:
    """the same method as 'get_header_distance'
    but returned name of point instead distance."""
    if type_ == 'city':
        points = {key: value for key, value
                  in distances.DISTANCES_INSIDE_CITY.items()
                  if distance <= value < distance + 10}

    else:
        points = {key: value for key, value
                  in distances.DISTANCES_OUTSIDE_CITY.items()
                  if distance <= value < distance + 40}

    return min(points, key=lambda k: abs(points[k] - distance))


def find_closest_point_from_base(database: dict, distance: int) -> str:
    closest_point = None
    min_difference = float('inf')

    for key, value in database.items():
        difference = abs(value - distance)
        if difference < min_difference:
            min_difference = difference
            closest_point = key

    return closest_point


def find_nearest_diff(dist_to_header: dict, dist_to_point: dict,
                      rest_of_the_way: int, visited_points: list) -> str:
    """the method uses when steps count are equal of 2
        and find the pre-last point"""
    diffs = {}
    for key in dist_to_point:
        if key in dist_to_header and key not in visited_points:
            sum_values = dist_to_header[key] + dist_to_point[key]
            diff = abs(sum_values - rest_of_the_way)
            diffs[key] = diff

    return min(diffs, key=diffs.get)


def search_inside_points(point: str) -> dict:
    """Find required dict with distances from nested list"""
    for i in distances.DIST_STATIONS_INSIDE:
        return [value for key, value in i.items() if key == point][0]


def get_ordinary_point(point: str, distance: int, visited_points: list) -> str:
    """search optimal next point"""
    points = {key: value
              for key, value
              in search_inside_points(point).items()
              if (distance - 10) <= value < (distance + 10)
              and key not in visited_points}

    return max(points, key=lambda k: abs(points[k] - distance))


def normalize_distances(distance_remainder: int, steps: list) -> list:
    """distribute the remainder of distance"""
    filtered_dicts = [d for d in steps if d['distance'] >= 10]
    if not filtered_dicts or distance_remainder == 0:
        return steps

    day_counts = len(filtered_dicts)
    remainder_per_dict = distance_remainder // day_counts
    remainder_mod = distance_remainder % day_counts

    for num, day in enumerate(filtered_dicts):
        if num < remainder_mod:
            day['distance'] += remainder_per_dict + 1
        else:
            day['distance'] += remainder_per_dict

    return steps


def normalize_consumption(consumption: float, ride_type: str) -> float:
    """the same method as 'normalize_distances' for fuel"""
    if ride_type == 'city':
        target_consumption = consumption // round(12.14 / 100, 2)
        closest_distance = round(target_consumption)
        return round(closest_distance * (12.14 / 100), 2)

    target_consumption = consumption // round(9.84 / 100, 2)
    closest_distance = round(target_consumption)
    return round(closest_distance * (9.84 / 100), 2)


def get_refill_type(point: str) -> str:
    """define type of ride for refill days"""
    type_ = 'city'
    if point in distances.DISTANCES_OUTSIDE_CITY.keys():
        type_ = 'country'
    return type_


def get_ordinary_type(consumption: float) -> str:
    """define type of ride for usual days"""
    type_ = 'city'
    if consumption > MAX_CITY_CONSUMPTION:
        type_ = 'country'
    return type_
