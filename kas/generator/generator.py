from kas.generator.refill_day import RefillDay
from kas.generator.ordinary_day import OrdinaryDay
from kas.generator.step_build import build_day
from kas.generator.journey_helpers import get_refill_type, \
    get_ordinary_type, \
    normalize_consumption


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

        self.routes = []

    def generate(self):
        current_fuel = self.remainder
        current_odo = self.odo
        current_number = self.path_number

        for day in self.fuels:
            for key, value in day.items():
                departure = self.departures.get(key)
                if isinstance(value, dict):
                    point = value.get('refill_point')
                    time = value.get('refill_time')
                    refill = value.get('refill')
                    ride = value.get('ride')
                    ride_type = get_refill_type(point)
                    normalized_consumption = normalize_consumption(
                        ride,
                        ride_type
                    )
                    day = RefillDay(
                        normalized_consumption,
                        departure,
                        time,
                        point,
                        ride_type
                    )
                    steps, arriving, odo = day.generate()
                    fuel_at_end = round((current_fuel + refill) -
                                        normalized_consumption, 2)
                    self.routes.append(
                        build_day(
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
                    ride_type = get_ordinary_type(value)
                    normalized_consumption = normalize_consumption(
                        value,
                        ride_type
                    )
                    day = OrdinaryDay(
                        normalized_consumption,
                        departure,
                        ride_type
                    )
                    steps, arriving, odo = day.generate()
                    fuel_at_end = round(current_fuel - normalized_consumption,
                                        2)
                    self.routes.append(
                        build_day(
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

        return self.routes, current_odo, current_fuel
