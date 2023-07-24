from kas.parser import parse

from kas.chunker import Chunked
from kas.distributor import DistributeFuel
from kas.generator import GenerateRoutes
from kas.departures import get_departures

import pytest


data = parse('data1.json', fixtures=True)
departures = get_departures(data)

initial_data = parse('initial_data1.json', fixtures=True)
fuel_balance = initial_data.get('fuel')
odo_balance = initial_data.get('odo')
path_number = initial_data.get('path_number')

exp_chunks = parse('expected_chunks1.json', fixtures=True)

exp_fuels = parse('expected_fuels1.json', fixtures=True)

exp_routes = parse('expected_routes1.json', fixtures=True)


class TestInnerView:

    @pytest.fixture
    def chunker(self):
        chunks = Chunked(data)
        chunks.filter()
        return chunks.chunked()

    @pytest.fixture
    def distributer(self, chunker):
        chunks = chunker
        fuels = DistributeFuel(chunks, fuel_balance)
        return fuels.distribute()

    @pytest.fixture
    def generator(self, distributer):
        distributed = distributer
        routes = GenerateRoutes(
            distributed,
            fuel_balance,
            departures,
            odo_balance,
            path_number
        )

        return routes.generate_routes()

    def test_inner_view(self, chunker, distributer, generator):
        assert chunker == exp_chunks
        assert distributer == exp_fuels
        assert generator[0] == exp_routes
