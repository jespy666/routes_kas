from kas.generator.step_build import build_step
from kas.database import distances
from kas.generator.journey_helpers import \
    calculate_distance,\
    calculate_travel_time,\
    get_departure,\
    search_inside_points,\
    get_header_distance,\
    get_ordinary_point,\
    normalize_distances,\
    get_point_from_header,\
    find_nearest_diff


MAX_DISTANCE = 100


class OrdinaryDay:

    def __init__(self, consumption: float, departure: str, ride_type: str):
        self.consumption = consumption
        self.departure = departure
        self.type = ride_type

        self.common_way = calculate_distance(self.consumption, self.type)
        self.way_balance = self.common_way

        self.steps = []
        self.visited_points = []
        self.passed_way = 0

        self.current_time = departure
        self.steps_count = self.get_steps_count()
        self.step_distance = self.common_way // self.steps_count

    def get_steps_count(self):
        if self.type == 'city':
            match self.common_way:
                case w if w >= MAX_DISTANCE * 2:
                    return 5
                case w if MAX_DISTANCE <= w < MAX_DISTANCE * 2:
                    return 4
                case w if (MAX_DISTANCE // 2) <= w < MAX_DISTANCE:
                    return 3
                case _:
                    return 2
        return 2

    def one_step_ride(self):
        distance = self.common_way // 2
        remainder = self.common_way % 2
        point = get_point_from_header(distance, self.type)
        arrival = calculate_travel_time(distance, self.current_time, self.type)

        self.steps.append(
            build_step(
                'Office',
                self.current_time,
                distance,
                point,
                arrival
            )
        )

        self.current_time = get_departure(arrival)
        last_distance = distance + remainder
        last_arrival = calculate_travel_time(
            last_distance,
            self.current_time,
            self.type
        )

        self.steps.append(
            build_step(
                point,
                self.current_time,
                last_distance,
                'Office',
                last_arrival
            )
        )

        self.current_time = last_arrival
        self.passed_way += (distance + last_distance)

    def multi_step_ride(self):
        first_point = get_point_from_header(self.step_distance, self.type)
        first_distance = get_header_distance(first_point, self.type)
        first_arrival = calculate_travel_time(
            first_distance,
            self.current_time,
            self.type
        )

        self.steps.append(
            build_step(
                'Office',
                self.current_time,
                first_distance,
                first_point,
                first_arrival
            )
        )

        self.visited_points.append(first_point)
        current_point = first_point
        self.current_time = get_departure(first_arrival)
        self.passed_way += first_distance
        self.steps_count -= 1
        while self.steps_count > 0:
            if self.steps_count == 2:
                rest_of_the_way = self.common_way - self.passed_way
                directions = search_inside_points(current_point)
                penult_point = find_nearest_diff(
                    distances.DISTANCES_INSIDE_CITY,
                    directions,
                    rest_of_the_way,
                    self.visited_points
                )
                penult_distance = [value for key, value
                                   in directions.items()
                                   if key == penult_point][0]
                penult_arrival = calculate_travel_time(
                    penult_distance,
                    self.current_time,
                    self.type
                )

                self.steps.append(
                    build_step(
                        current_point,
                        self.current_time,
                        penult_distance,
                        penult_point,
                        penult_arrival
                    )
                )

                self.current_time = get_departure(penult_arrival)
                current_point = penult_point
                last_distance = get_header_distance(current_point)
                last_arrival = calculate_travel_time(
                    last_distance,
                    self.current_time,
                    self.type
                )

                self.steps.append(
                    build_step(
                        current_point,
                        self.current_time,
                        last_distance,
                        'Office',
                        last_arrival
                    )
                )

                self.current_time = last_arrival
                self.passed_way += (first_distance + last_distance)
                break
            else:
                directions = search_inside_points(current_point)
                next_point = get_ordinary_point(
                    current_point,
                    self.step_distance,
                    self.visited_points
                )
                next_distance = [value for key, value
                                 in directions.items()
                                 if key == next_point][0]
                next_arrival = calculate_travel_time(
                    next_distance,
                    self.current_time,
                    self.type
                )

                self.steps.append(
                    build_step(
                        current_point,
                        self.current_time,
                        next_distance,
                        next_point,
                        next_arrival
                    )
                )

                current_point = next_point
                self.current_time = get_departure(next_arrival)
                self.visited_points.append(next_point)
                self.passed_way += next_distance
                self.steps_count -= 1

    def generate(self) -> tuple:
        match self.steps_count:
            case x if x == 2:
                self.one_step_ride()
            case _:
                self.multi_step_ride()
        dist_remainder = self.common_way - self.passed_way
        return normalize_distances(dist_remainder, self.steps), \
            self.current_time, \
            self.common_way
