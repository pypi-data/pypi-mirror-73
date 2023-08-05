from datetime import date, timedelta
from typing import Iterable

import requests
from .dataclasses import Airport, City, Flight, Location

DATE_FORMAT = "%d/%m/%Y"

AGGREGATION_FLIGHTS_URL = "https://api.skypicker.com/aggregation_flights"
LOCATIONS_URL = "https://api.skypicker.com/locations"


class FlightOptimizer:

    def __init__(self, departure: str, destinations: Iterable[str]) -> Iterable[Flight]:
        self.departure = departure
        self.destinations = destinations

    def process(self):
        departure_city = self.get_city(self.departure)
        destination_cities = list(map(self.get_city, self.destinations))

        departure_airport = self._get_airport(departure_city)
        destination_airports = list(map(self._get_airport, destination_cities))

        best_flights = [
            self._get_best_flight(departure_airport, destination_airport)
            for destination_airport in destination_airports
        ]

        sorted_flights = sorted(best_flights, key=lambda flight: flight.price_per_kilometer)

        return sorted_flights

    @staticmethod
    def get_result_explanation(flights: Iterable[Flight]) -> str:
        departure_explanation = flights[0].departure.city.get_explanation_message()
        destination_explanations = [flight.destination.city.get_explanation_message() for flight in flights]

        explanations = [departure_explanation] + destination_explanations
        filtered_explanations = list(filter(lambda x: x is not None, explanations))

        message = '\n'.join(filtered_explanations) if filtered_explanations else 'Every city was correctly spelled.'
        return f'\nExplanation and suggestions:\n{message}'

    @staticmethod
    def _get_best_flight(departure: Location, destination: Location) -> Flight:

        if not departure.airport.is_found or not destination.airport.is_found:
            return Flight(is_found=False, departure=departure, destination=destination)

        query = {
            'fly_from': f'airport:{departure.airport.code}',
            'fly_to': f'airport:{destination.airport.code}',
            'date_from': date.today().strftime(DATE_FORMAT),
            'date_to': (date.today() + timedelta(days=1)).strftime(DATE_FORMAT),
            'one_for_city': 1,
            'children': 0,
            'adults': 1,
            'infants': 0,
            'partner': 'picky',
            'curr': 'USD',
            'limit': 1,
            'sort': 'price',
            'asc': 1,
            'xml': 0
        }
        response = requests.get(AGGREGATION_FLIGHTS_URL, params=query)
        data = response.json()

        if 'data' not in data or destination.city.id not in data['data']:
            return Flight(is_found=False, departure=departure, destination=destination)

        return Flight(
            departure=departure,
            destination=destination,
            is_found=True,
            price=data["data"][destination.city.id]
        )

    @staticmethod
    def _get_airport(city: City) -> Location:

        query = {
            'term': city.id,
            'type': 'subentity',
            'location_types': 'airport',
            'active_only': 'true',
            'limit': 1,
            'sort': 'rank'
        }

        if not city.is_found:
            return Location(city=city, airport=Airport(is_found=False))

        response = requests.get(LOCATIONS_URL, params=query)
        data = response.json()

        if 'locations' not in data or len(data['locations']) == 0:
            return Location(city=city, airport=Airport(is_found=False))

        airport = data['locations'][0]

        return Location(
            city=city,
            airport=Airport(
                is_found=True,
                name=airport["name"],
                code=airport["code"],
                location=(
                    airport["location"]["lat"],
                    airport["location"]["lon"]
                )
            )
        )

    @staticmethod
    def get_city(city: str) -> City:
        query = {
            'term': city,
            'location_types': 'city',
            'active_only': 'true',
            'limit': 5,
        }

        response = requests.get(LOCATIONS_URL, params=query)
        data = response.json()

        if 'locations' not in data or len(data['locations']) == 0:
            return City(is_found=False, input_name=city)

        cities = data['locations']
        correct_name_options = list(
            map(
                lambda possible_city: (possible_city['name'], possible_city['country']['name']),
                cities
            )
        )

        return City(
            is_found=True,
            input_name=city,
            name=cities[0]['name'],
            id=cities[0]['id'],
            correct_name_options=correct_name_options,
        )
