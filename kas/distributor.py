from kas.database.distances import DISTANCES_INSIDE_CITY,\
    DISTANCES_OUTSIDE_CITY


MAX_REFILL_TIME = 11
MIN_PERMIT_TIME = 15
MAX_FUEL_REMAINDER = 20


class DistributeFuel:

    def __init__(self, inner: list, fuel: float):
        self.inner = inner
        self.fuel = fuel

        self.current_fuel = fuel
        self.fuels = []

    @staticmethod
    def calculate_min_required_fuel(point: str) -> float:
        fuel_coefficient = 12.14 / 100
        distances = DISTANCES_INSIDE_CITY
        if point not in distances:
            distances = DISTANCES_OUTSIDE_CITY
            fuel_coefficient = 9.84 / 100

        distance = distances.get(point, 0)
        fuel = fuel_coefficient * distance
        return round(fuel, 2)

    def calculate_last_days(self, time: str, point: str, refill: float):
        min_fuel = self.calculate_min_required_fuel(point)
        step_length = len(self.inner[-1])
        hour = int(time.split(':')[0])
        fuel_value = (self.current_fuel + refill) - min_fuel
        if step_length == 1:
            match hour:
                case h if MAX_REFILL_TIME < h < MIN_PERMIT_TIME:
                    return min_fuel * 2
                case _:
                    return fuel_value - MAX_FUEL_REMAINDER
        else:
            match hour:
                case h if MAX_REFILL_TIME < h < MIN_PERMIT_TIME:
                    refill_day = min_fuel * 2
                    ordinary_day = pre_refill_day =\
                        (fuel_value - MAX_FUEL_REMAINDER) / (step_length - 1)
                case _:
                    refill_day = ordinary_day = pre_refill_day =\
                        (fuel_value + min_fuel - MAX_FUEL_REMAINDER) /\
                        step_length
            return refill_day, ordinary_day, pre_refill_day

    def calculate_fuels(self, index: int, time: str, point: str):
        min_fuel = self.calculate_min_required_fuel(point)
        step_length = len(self.inner[index])
        hour = int(time.split(':')[0])
        if step_length == 1:
            match hour:
                case h if MAX_REFILL_TIME < h < MIN_PERMIT_TIME:
                    return min_fuel * 2
                case _:
                    return self.current_fuel - (min_fuel * 2)
        else:
            match hour:
                case h if MAX_REFILL_TIME < h < MIN_PERMIT_TIME:
                    refill_day = min_fuel * 2
                    unrefillable_days = self.current_fuel / (step_length - 1)
                    before_refill_day = unrefillable_days - min_fuel
                case _:
                    refill_day = (self.current_fuel / step_length) + min_fuel
                    unrefillable_days = self.current_fuel / (step_length - 1)
                    before_refill_day = unrefillable_days - min_fuel
            return refill_day, before_refill_day, unrefillable_days

    def distribute_step(self, index: int, time: str, point: str, refill: float,
                        refill_day: float,
                        before_refill_day: float,
                        unrefillable_days: float) -> dict:

        refill_day, before_refill_day, unrefillable_days = \
            list(map(lambda x: round(x, 2),
                     [refill_day, before_refill_day, unrefillable_days]))

        refill_day_data = {
            'ride': refill_day,
            'refill_time': time,
            'refill_point': point,
            'refill': refill
        }
        result = {}

        step = self.inner[index]
        keys = list(step.keys())
        for _ in keys:

            if len(keys) == 1:
                result[keys[0]] = refill_day_data
            elif len(keys) == 2:
                result[keys[0]] = before_refill_day
                result[keys[1]] = refill_day_data
            else:
                for i in keys[:-2]:
                    result[i] = unrefillable_days

                result[keys[-2]] = before_refill_day
                result[keys[-1]] = refill_day_data

        return dict(sorted(result.items(), key=lambda x: int(x[0])))

    def set_current_fuel(self, step: dict, refill: float):
        refill_key = list(step.keys())[-1]
        refill_consumption = step[refill_key]['ride']
        consumption = 0
        for key, value in step.items():
            if isinstance(value, float):
                consumption += value
        consumption += refill_consumption
        fuel = round((self.current_fuel + refill) - consumption, 2)
        self.current_fuel = fuel

    def built_in(self, index: int, time: str, point: str, refill: float,
                 calculated: tuple | float, day: str):
        if isinstance(calculated, tuple):
            refill_, before_refill_, unrefill_ = calculated
            built = self.distribute_step(
                index,
                time,
                point,
                refill,
                refill_,
                before_refill_,
                unrefill_
            )
        else:
            built = {
                day:
                    {
                        'ride': calculated,
                        'refill_time': time,
                        'refill_point': point,
                        'refill': refill
                    }
            }
        self.fuels.append(built)
        self.set_current_fuel(built, refill)

    def distribute_last_days(self, chunk: dict):
        if all(not isinstance(value, dict) for value in chunk.values()):
            if self.current_fuel > MAX_FUEL_REMAINDER:
                last_fuel = (self.current_fuel - MAX_FUEL_REMAINDER) \
                            / len(chunk)
                last_days = {key: last_fuel for key in chunk.keys()}
                self.fuels.append(last_days)
        else:
            for day, value in chunk.items():
                if isinstance(value, dict):
                    time = value.get('time')
                    point = value.get('point')
                    refill = float(value.get('fuel'))
                    calculated = self.calculate_last_days(time, point, refill)
                    self.built_in(-1, time, point, refill, calculated, day)

    def distribute(self):
        for chunk in self.inner:
            index = self.inner.index(chunk)
            if index == len(self.inner) - 1:
                self.distribute_last_days(chunk)
                return self.fuels
            for day, value in chunk.items():
                if isinstance(value, dict):
                    time = value.get('time')
                    point = value.get('point')
                    refill = float(value.get('fuel'))
                    calculated = self.calculate_fuels(index, time, point)
                    self.built_in(index, time, point, refill, calculated, day)
        return self.fuels
