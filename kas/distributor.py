from kas.database import distances
from kas.parser import parse


class DistributeFuel:

    def __init__(self, inner: list, fuel: float):
        self.inner = inner
        self.fuel = fuel

    @staticmethod
    def calculate_min_required_fuel(point: str) -> float:

        distance: list = [value for key, value
                          in distances.DISTANCES_INSIDE_CITY.items()
                          if key == point]

        if not distance:
            distance: list = [value for key, value
                              in distances.DISTANCES_OUTSIDE_CITY.items()
                              if key == point]
            fuel: float = (9.84 / 100) * distance[0]
        else:
            fuel: float = (12.14 / 100) * distance[0]

        return round(fuel, 2)

    @staticmethod
    def calculate_fuel_per_step(current_fuel: float,
                                min_fuel: float,
                                step_length: int) -> float:

        common_fuel: float = current_fuel - (min_fuel * 2)

        return round(common_fuel / step_length, 2)

    @staticmethod
    def get_current_fuel(step: dict,
                         refill: float,
                         current_fuel: float) -> float:

        refill_key = list(step.keys())[-1]
        refill_consumption = step[refill_key]['ride']
        consumption = 0
        for key, value in step.items():
            if isinstance(value, float):
                consumption += value
        consumption += refill_consumption
        return round((current_fuel + refill) - consumption, 2)

    def calculate_fuels(self, index: int, current_fuel: float,
                        time: str, point: str) -> tuple | float:

        min_fuel: float = self.calculate_min_required_fuel(point)
        step_length: int = len(self.inner[index])

        if step_length > 1:
            match time:
                case x if int(x.split(':')[0]) >= 11:
                    refill_day = min_fuel * 2
                    unrefillable_days = current_fuel / (step_length - 1)
                    before_refill_day = unrefillable_days - min_fuel
                case _:
                    refill_day = (current_fuel / step_length) + min_fuel
                    unrefillable_days = current_fuel / (step_length - 1)
                    before_refill_day = unrefillable_days - min_fuel
            return refill_day, before_refill_day, unrefillable_days

        elif step_length == 1:
            match time:
                case x if int(x.split(':')[0]) >= 11:
                    return min_fuel * 2
                case _:
                    return current_fuel - (min_fuel * 2)

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
        result: dict = {}

        step: dict = self.inner[index]
        keys: list = list(step.keys())
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

    def distribute_last_days(self, index: int,
                             counter: int,
                             current_fuel: float,
                             remainder=20) -> list | None:

        if current_fuel < remainder:
            return None

        fuel_per_day = round((current_fuel - remainder) / counter, 2)
        last_days = {key: fuel_per_day
                     for key, value
                     in self.inner[index].items()}
        fuel_remainder = round(current_fuel - (fuel_per_day * counter), 2)

        return [last_days, fuel_remainder]

    def distribute(self) -> list:

        current_fuel: float = self.fuel

        steps: list = []
        for chunk in self.inner:

            index: int = self.inner.index(chunk)
            counter: int = 0
            for key, value in chunk.items():

                if isinstance(value, dict):

                    time: str = value['time']
                    point: str = value['point']
                    refill: str = value['fuel']

                    calculated: tuple | float = self.calculate_fuels(
                        index, current_fuel, time, point)
                    match calculated:
                        case c if isinstance(c, tuple):
                            refill_day, \
                                before_refill_day, \
                                unrefillable_days = calculated
                            built = self.distribute_step(
                                index,
                                time,
                                point,
                                float(refill),
                                refill_day,
                                before_refill_day,
                                unrefillable_days)
                        case _:
                            built = {
                                key: {
                                    'ride': calculated,
                                    'refill_time': time,
                                    'refill_point': point,
                                    'refill': float(refill)
                                }
                            }
                    steps.append(built)

                    current_fuel = self.get_current_fuel(steps[-1],
                                                         float(refill),
                                                         float(current_fuel))
                    counter = 0

                else:
                    counter += 1

            if counter > 0:

                last_days: list | None = self.distribute_last_days(
                    index, counter, current_fuel)
                if last_days:
                    steps.append(last_days[0])
                    current_fuel: float = last_days[1]

        return steps


chunks = parse('chunks1.json', fixtures=True)
fuel = DistributeFuel(chunks, 42.08)
fuels = fuel.distribute()
