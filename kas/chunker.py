
class Chunked:

    def __init__(self, data: list):
        self.data = data

    def chunked(self) -> list:

        chunks: list = []
        current_chunk: dict = {}

        for day in self.data:
            for key, value in day.items():

                time: str | None = value.get('refueling_time')
                point: str | None = value.get('refueling_station')
                fuel: int | None = value.get('ltr')

                if time != '':
                    current_chunk[key] = {
                        'time': time,
                        'point': point,
                        'fuel': fuel
                    }
                    chunks.append(current_chunk)
                    current_chunk = {}
                else:
                    current_chunk[key] = None

        if current_chunk:
            chunks.append(current_chunk)

        return chunks
