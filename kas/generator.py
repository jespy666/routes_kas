from datetime import datetime, timedelta

from kas.database import distances


MAX_DISTANCE = 105
MAX_CITY_CONSUMPTION = 21.00
MAX_REFILL_TIME = 11


class GenerateRoutes:

    def __init__(
            self,
            fuels: list,
            remainder: float,
            departures: dict,
            odo: int,
            path_number: int
    ):
        self.fuels = fuels
        self.remainder = remainder
        self.departures = departures
        self.odo = odo
        self.path_number = path_number

    @staticmethod
    def get_distance(consumption: float, ride_type: str = 'city'):
        if ride_type == 'city':
            return int(round(consumption / (12.14 / 100)))
        if ride_type == 'country':
            return int(round(consumption / (9.84 / 100)))
        else:
            raise ValueError(f'Incorrect param: {ride_type}')

    @staticmethod
    def get_header_distance(point: str, type_='city') -> int:
        """returned distance from header to first point.
         The named param: type_
         are indicate the type of ride: city or country."""
        if type_ == 'city':
            distance = [value for key, value
                        in distances.DISTANCES_INSIDE_CITY.items()
                        if key == point][0]

        elif type_ == 'country':
            distance = [value for key, value
                        in distances.DISTANCES_OUTSIDE_CITY.items()
                        if key == point][0]

        else:
            raise ValueError(f"Incorrect param: {type_}")

        return distance

    @staticmethod
    def get_point_from_header(distance: int, type_='city') -> str:
        """the same method as 'get_header_distance'
         but returned name of point instead distance."""
        if type_ == 'city':
            points = {key: value for key, value
                      in distances.DISTANCES_INSIDE_CITY.items()
                      if distance <= value < distance + 10}

        elif type_ == 'country':
            points = {key: value for key, value
                      in distances.DISTANCES_OUTSIDE_CITY.items()
                      if distance <= value < distance + 20}

        else:
            raise ValueError(f"Incorrect param: {type_}")

        return min(points, key=lambda k: abs(points[k] - distance))

    @staticmethod
    def build_step(start: str,
                   departure: str,
                   distance: int,
                   end: str,
                   arriving: str) -> dict:
        """forming the step dict"""
        return {
            'from_AZK': start,
            'departure': departure,
            'distance': distance,
            'to_AZK': end,
            'arriving': arriving
        }

    @staticmethod
    def get_refill_steps_count(time: str, distance: int) -> int:
        """define counts of ride when was refill, depends on common distance
         and time of refill"""
        if int(time.split(':')[0]) < MAX_REFILL_TIME:

            match distance:
                case d if d >= MAX_DISTANCE * 3:
                    return 7
                case d if (MAX_DISTANCE * 2) <= d < (MAX_DISTANCE * 3):
                    return 6
                case d if MAX_DISTANCE <= d < (MAX_DISTANCE * 2):
                    return 5
                case d if (MAX_DISTANCE // 2) <= d < MAX_DISTANCE:
                    return 4
                case _:
                    return 2
        return 2

    @staticmethod
    def get_ordinary_steps_count(distance: int, ride_type: str) -> int:
        """the same method as 'get_refill_steps_count' for usual days"""
        if ride_type == 'city':

            match distance:
                case d if d > MAX_DISTANCE:
                    return 4
                case d if (MAX_DISTANCE // 2) <= d < MAX_DISTANCE:
                    return 3
                case _:
                    return 2
        return 2

    @staticmethod
    def get_type(point: str) -> str:
        """define type of ride for refill days"""
        type_ = 'city'
        if point in distances.DISTANCES_OUTSIDE_CITY.keys():
            type_ = 'country'
        return type_

    @staticmethod
    def get_ordinary_type(consumption: float) -> str:
        """define type of ride for usual days"""
        type_ = 'city'
        if consumption > MAX_CITY_CONSUMPTION:
            type_ = 'country'
        return type_

    @staticmethod
    def calculate_travel_time(distance: int, departure: str, ride_type: str)\
            -> str:
        """get updated time after passing the distance"""
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

    @staticmethod
    def get_departure(time: str, refill: bool = False) -> str:
        """calculated time from arriving the point to departure.
         The named param: refill are indicate on refill day"""
        departure_time = datetime.strptime(time, '%H:%M')
        if not refill:
            parking_time = 40
            updated = departure_time + timedelta(minutes=parking_time)
        else:
            updated = departure_time + timedelta(minutes=10)
        return updated.strftime('%H:%M')

    @staticmethod
    def search_inside_points(station: str) -> dict:
        """Find required dict with distances from nested list"""
        for i in distances.DIST_STATIONS_INSIDE:
            return [value for key, value in i.items() if key == station][0]

    @staticmethod
    def find_nearest_diff(dist_to_header: dict, dist_to_point: dict,
                          rest_of_the_way: int) -> str:
        """the method uses when steps count are equal of 2
         and find the pre-last point"""
        diffs = {}

        for key in dist_to_point:
            if key in dist_to_header:
                sum_values = dist_to_header[key] + dist_to_point[key]
                diff = abs(sum_values - rest_of_the_way)
                diffs[key] = diff

        return min(diffs, key=diffs.get)

    def get_ordinary_point(self, point: str, step_distance: int,
                           visited_points: list) -> str:
        """search optimal next point"""
        points = {key: value
                  for key, value
                  in self.search_inside_points(point).items()
                  if (step_distance - 10) <= value < (step_distance + 10)
                  and key not in visited_points}

        return max(points, key=lambda k: abs(points[k] - step_distance))

    def generate_refill_day(self, consumption: float, departure: str,
                            time: str, point: str, ride_type: str) -> tuple:
        """forming the day there are was refill"""

        common_distance = self.get_distance(consumption, ride_type)
        distance_balance = common_distance
        current_time = departure

        steps = []
        steps_count = self.get_refill_steps_count(time, common_distance)

        if steps_count == 2:

            first_distance = common_distance // 2
            remainder = common_distance % 2

            first_arrival = self.calculate_travel_time(
                first_distance,
                current_time,
                ride_type
            )
            steps.append(
                self.build_step(
                    'Office',
                    departure,
                    first_distance,
                    point,
                    first_arrival
                )
            )

            current_time = first_arrival

            last_departure = self.get_departure(current_time, refill=True)
            last_distance = first_distance + remainder
            last_arrival = self.calculate_travel_time(
                last_distance,
                last_departure,
                ride_type
            )

            steps.append(
                self.build_step(
                    point,
                    last_departure,
                    last_distance,
                    'Office',
                    last_arrival
                )
            )

            current_time = last_arrival
            distance_balance -= (first_distance + last_distance)

        else:

            first_point = point
            first_distance = self.get_header_distance(first_point, ride_type)
            first_arrival = self.calculate_travel_time(
                first_distance,
                departure,
                ride_type
            )

            steps.append(
                self.build_step(
                    'Office',
                    departure,
                    first_distance,
                    first_point,
                    first_arrival
                )
            )

            steps_count -= 1
            step_distance = (common_distance - first_distance) // steps_count
            current_time = self.get_departure(time, refill=True)
            current_point = first_point

            visited_points = [first_point]
            distance_balance -= first_distance

            while steps_count > 0:
                if steps_count == 2:
                    rest_of_the_way = step_distance * 2

                    penult_point = self.find_nearest_diff(
                        distances.DISTANCES_INSIDE_CITY,
                        self.search_inside_points(current_point),
                        rest_of_the_way
                    )
                    penult_distance = [value for key, value in
                                       self.search_inside_points(
                                           current_point
                                       ).items() if key == penult_point][0]
                    penult_arrival = self.calculate_travel_time(
                        penult_distance, current_time, ride_type
                    )
                    steps.append(
                        self.build_step(
                            current_point,
                            current_time,
                            penult_distance,
                            penult_point,
                            penult_arrival
                        )
                    )
                    current_time = self.get_departure(
                        penult_arrival,
                        refill=False
                    )
                    current_point = penult_point

                    last_distance = self.get_header_distance(current_point)
                    last_arrival = self.calculate_travel_time(
                        last_distance,
                        current_time,
                        ride_type
                    )

                    steps.append(
                        self.build_step(
                            current_point,
                            current_time,
                            last_distance,
                            'Office',
                            last_arrival
                        )
                    )

                    current_time = last_arrival
                    distance_balance -= (penult_distance + last_distance)
                    break

                else:
                    next_point = self.get_ordinary_point(
                        current_point,
                        step_distance,
                        visited_points
                    )

                    next_distance = [value for key, value in
                                     self.search_inside_points(
                                         current_point
                                     ).items() if key == next_point][0]

                    next_arrival = self.calculate_travel_time(
                        next_distance,
                        current_time,
                        ride_type
                    )

                    steps.append(
                        self.build_step(
                            current_point,
                            current_time,
                            next_distance,
                            next_point,
                            next_arrival
                        )
                    )

                    current_point = next_point
                    current_time = self.get_departure(
                        next_arrival,
                        refill=False
                    )

                    steps_count -= 1
                    visited_points.append(next_point)
                    distance_balance -= next_distance

        self.normalize_distances(distance_balance, steps)

        return steps, current_time, common_distance

    def generate_ordinary_day(self, consumption: float, departure: str,
                              ride_type: str) -> tuple:
        """forming usual day"""

        common_distance = self.get_distance(consumption, ride_type)
        distance_balance = common_distance

        steps_count = self.get_ordinary_steps_count(common_distance, ride_type)

        current_time = departure
        steps = []

        if steps_count == 2:
            distance_per_step = common_distance // 2
            remainder = common_distance % 2

            first_point = self.get_point_from_header(
                distance_per_step,
                ride_type
            )
            first_distance = self.get_header_distance(first_point, ride_type)
            first_arrival = self.calculate_travel_time(
                first_distance,
                current_time,
                ride_type
            )

            steps.append(
                self.build_step(
                    'Office',
                    current_time,
                    first_distance,
                    first_point,
                    first_arrival
                )
            )

            current_time = self.get_departure(first_arrival, refill=False)

            last_distance = first_distance + remainder
            last_arrival = self.calculate_travel_time(
                last_distance,
                current_time,
                ride_type
            )

            steps.append(
                self.build_step(
                    first_point,
                    current_time,
                    last_distance,
                    'Office',
                    last_arrival
                )
            )
            current_time = last_arrival
            distance_balance -= (first_distance + last_distance)

        else:

            step_distance = common_distance // steps_count
            first_point = self.get_point_from_header(
                step_distance,
                ride_type
            )
            first_distance = self.get_header_distance(first_point, ride_type)
            first_arrival = self.calculate_travel_time(
                first_distance,
                current_time,
                ride_type
            )

            steps.append(
                self.build_step(
                    'Office',
                    current_time,
                    first_distance,
                    first_point,
                    first_arrival
                )
            )

            current_point = first_point
            current_time = self.get_departure(first_arrival, refill=False)

            steps_count -= 1
            visited_points = [first_point]
            distance_balance -= first_distance

            while steps_count > 0:
                if steps_count == 2:
                    rest_of_the_way = step_distance * 2

                    penult_point = self.find_nearest_diff(
                        distances.DISTANCES_INSIDE_CITY,
                        self.search_inside_points(current_point),
                        rest_of_the_way
                    )
                    penult_distance = [value for key, value in
                                       self.search_inside_points(
                                           current_point
                                       ).items() if key == penult_point][0]
                    penult_arrival = self.calculate_travel_time(
                        penult_distance, current_time, ride_type
                    )
                    steps.append(
                        self.build_step(
                            current_point,
                            current_time,
                            penult_distance,
                            penult_point,
                            penult_arrival
                        )
                    )
                    current_time = self.get_departure(
                        penult_arrival,
                        refill=False
                    )
                    current_point = penult_point

                    last_distance = self.get_header_distance(current_point)
                    last_arrival = self.calculate_travel_time(
                        last_distance,
                        current_time,
                        ride_type
                    )

                    steps.append(
                        self.build_step(
                            current_point,
                            current_time,
                            last_distance,
                            'Office',
                            last_arrival
                        )
                    )

                    current_time = last_arrival
                    distance_balance -= (penult_distance + last_distance)
                    break

                else:
                    next_point = self.get_ordinary_point(
                        current_point,
                        step_distance,
                        visited_points
                    )

                    next_distance = [value for key, value in
                                     self.search_inside_points(
                                         current_point
                                     ).items() if key == next_point][0]

                    next_arrival = self.calculate_travel_time(
                        next_distance,
                        current_time,
                        ride_type
                    )

                    steps.append(
                        self.build_step(
                            current_point,
                            current_time,
                            next_distance,
                            next_point,
                            next_arrival
                        )
                    )

                    current_point = next_point
                    current_time = self.get_departure(
                        next_arrival,
                        refill=False
                    )

                    steps_count -= 1
                    visited_points.append(next_point)
                    distance_balance -= next_distance

        self.normalize_distances(distance_balance, steps)

        return steps, current_time, common_distance

    @staticmethod
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

    @staticmethod
    def normalize_consumption(consumption: float, ride_type: str) -> float:
        """the same method as 'normalize_distances' for fuel"""
        if ride_type == 'city':
            target_consumption = consumption // round(12.14 / 100, 2)
            closest_distance = round(target_consumption)
            return round(closest_distance * (12.14 / 100), 2)

        target_consumption = consumption // round(9.84 / 100, 2)
        closest_distance = round(target_consumption)
        return round(closest_distance * (9.84 / 100), 2)

    @staticmethod
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

    def generate_routes(self) -> tuple:
        """the main method, generate all days"""
        current_fuel = self.remainder
        current_odo = self.odo
        current_number = self.path_number

        routes = []
        for day in self.fuels:
            for key, value in day.items():
                departure = self.departures.get(key)

                if isinstance(value, dict):
                    point = value.get('refill_point')
                    time = value.get('refill_time')
                    refill = value.get('refill')
                    ride = value.get('ride')
                    ride_type = self.get_type(point)
                    normalized_consumption = self.normalize_consumption(
                        ride,
                        ride_type
                    )

                    steps, arriving, odo =\
                        self.generate_refill_day(
                            normalized_consumption,
                            departure,
                            time,
                            point,
                            ride_type
                        )

                    fuel_at_end = round((current_fuel + refill) -
                                        normalized_consumption, 2)
                    routes.append(
                        self.build_day(
                            key,
                            departure,
                            arriving,
                            current_fuel,
                            fuel_at_end,
                            refill,
                            current_odo,
                            current_odo + odo,
                            normalized_consumption,
                            odo,
                            current_number,
                            steps
                        )
                    )

                else:
                    ride_type = self.get_ordinary_type(value)
                    normalized_consumption = self.normalize_consumption(
                        value,
                        ride_type
                    )
                    steps, arriving, odo =\
                        self.generate_ordinary_day(
                            normalized_consumption,
                            departure,
                            ride_type
                        )

                    fuel_at_end = round(current_fuel - normalized_consumption,
                                        2)

                    routes.append(
                        self.build_day(
                            key,
                            departure,
                            arriving,
                            current_fuel,
                            fuel_at_end,
                            None,
                            current_odo,
                            current_odo + odo,
                            normalized_consumption,
                            odo,
                            current_number,
                            steps
                        )
                    )

                current_fuel = fuel_at_end
                current_odo += odo
                current_number += 1

        return routes, current_odo, current_fuel
