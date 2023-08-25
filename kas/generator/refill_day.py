from kas.generator.step_build import build_step
from kas.database import distances
from kas.generator.journey_helpers import \
    calculate_distance, \
    calculate_travel_time, \
    get_departure, \
    find_closest_point_from_base, \
    search_inside_points, \
    get_header_distance, \
    get_ordinary_point, \
    normalize_distances

MAX_DISTANCE = 100
MAX_REFILL_TIME = 11
MIN_PERMIT_TIME = 15


class RefillDay:

    def __init__(
            self,
            consumption: float,
            departure: str,
            time: str,
            point: str,
            type_: str
    ):

        self.consumption = consumption
        self.departure = departure
        self.time = time
        self.point = point
        self.type = type_

        self.steps = []
        self.visited_points = []
        self.passed_way = 0

        self.common_way = calculate_distance(self.consumption, self.type)
        self.way_balance = self.common_way
        self.current_time = departure

        self.steps_count = self.get_steps_count()
        self.step_distance = self.common_way // self.steps_count

    def get_steps_count(self) -> int:
        hour = int(self.time.split(':')[0])
        if MAX_REFILL_TIME < hour < MIN_PERMIT_TIME or self.type == 'country':
            return 2

        match self.common_way:
            case d if d >= MAX_DISTANCE * 2:
                return 6
            case d if MAX_DISTANCE <= d < MAX_DISTANCE * 2:
                return 5
            case d if (MAX_DISTANCE // 2) <= d < MAX_DISTANCE:
                return 4
            case _:
                return 3

    def get_first_step_on_multi(self):
        hour = int(self.time.split(':')[0])
        match hour:
            case t if t >= MIN_PERMIT_TIME:
                return find_closest_point_from_base(
                    distances.DISTANCES_INSIDE_CITY,
                    self.step_distance
                )
            case _:
                return self.point

    def one_step_ride(self):
        first_distance = self.common_way // 2
        remainder = self.common_way % 2
        first_arrival = calculate_travel_time(
            first_distance,
            self.current_time,
            self.type
        )

        self.steps.append(
            build_step(
                'Office',
                self.departure,
                first_distance,
                self.point,
                first_arrival
            )
        )

        self.current_time = get_departure(first_arrival, refill=self.time)
        last_distance = first_distance + remainder
        last_arrival = calculate_travel_time(
            last_distance,
            self.current_time,
            self.type
        )

        self.steps.append(
            build_step(
                self.point,
                self.current_time,
                last_distance,
                'Office',
                last_arrival
            )
        )

        self.current_time = last_arrival
        self.passed_way += (first_distance + last_distance)

    def multi_step_ride(self):
        first_step = self.get_first_step_on_multi()
        first_distance = distances.DISTANCES_INSIDE_CITY.get(first_step)
        first_arrival = calculate_travel_time(
            first_distance,
            self.current_time,
            self.type
        )

        self.steps.append(
            build_step(
                'Office',
                self.departure,
                first_distance,
                first_step,
                first_arrival
            )
        )

        self.visited_points.append(first_step)
        refill = self.time if first_step == self.point else None
        self.current_time = get_departure(first_arrival, refill=refill)
        self.steps_count -= 1

        current_point = first_step
        self.passed_way += first_distance
        while self.steps_count > 0:
            if self.steps_count == 2:
                penult_point = self.point if \
                    self.point not in self.visited_points \
                    else get_ordinary_point(
                     current_point,
                     self.step_distance,
                     self.visited_points
                    )
                directions = search_inside_points(penult_point)
                penult_distance = [value for key, value
                                   in directions.items()
                                   if key == current_point][0]
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

                self.current_time = get_departure(
                    penult_arrival,
                    refill=self.time
                )
                current_point = penult_point
                last_distance = get_header_distance(current_point, self.type)
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
                self.passed_way += (penult_distance + last_distance)
                break
            else:
                self.step_distance = self.common_way // self.steps_count
                next_point = get_ordinary_point(
                    current_point,
                    self.step_distance,
                    self.visited_points
                )
                directions = search_inside_points(current_point)
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
                self.visited_points.append(next_point)
                current_point = next_point
                self.current_time = get_departure(next_arrival)
                self.steps_count -= 1
                self.passed_way += next_distance

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
