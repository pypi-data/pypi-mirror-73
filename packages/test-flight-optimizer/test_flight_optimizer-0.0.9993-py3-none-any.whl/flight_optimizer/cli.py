import click
from dataclasses import dataclass
from datetime import date, timedelta
from typing import Iterable

import requests
from haversine import haversine as get_distance


@click.command()
@click.option('--from', '-f', 'departure', required=True, type=str, help="Departure City")
@click.option('--to', '-t', 'destinations', required=True, type=str, help="Destination City (can be multiple)",
              multiple=True)
@click.option('--show-all-destinations', '-a', is_flag=True, default=False,
              help="Shows the best flights for every destination")
@click.option('--suggest-options', '-s', is_flag=True, default=False,
              help="If entered city was misspelled, than it suggests correct city name options")
def search(departure, destinations, show_all_destinations, suggest_options):
    try:
        flight_optimizer = FlightOptimizer(departure, destinations)
        response = flight_optimizer.process(show_all_destinations, suggest_options)
        click.echo(response.price_per_kilometer)

    except Exception as exception:
        click.echo(str(exception))


@click.command()
@click.option('--from', '-f', 'city', required=True, type=str, help="City")
def get_locations(city):
    try:
        flight_optimizer = FlightOptimizer(city, city)
        response = flight_optimizer.get_city(city)
        ret = {
            "city": response.input_name,
            "possible_cities": response.correct_name_options
        }
        print(ret)
        print(response)

    except Exception as exception:
        click.echo(str(exception))


DATE_FORMAT = "%d/%m/%Y"

AGGREGATION_FLIGHTS_URL = "https://api.skypicker.com/aggregation_flights"
LOCATIONS_URL = "https://api.skypicker.com/locations"


@dataclass
class City:
    id: str
    input_name: str
    valid_name: str
    assumed_name: str
    correct_name_options: Iterable[str]
    is_found: bool

    # def __repr__(self):
    #     return f'{self.valid_name}' if self.valid_name else f'{self.assumed_name}'

    def get_message_for_options(self):
        if not self.valid_name:
            options = '\", \"'.join(self.correct_name_options)
            output = f'Entered city name "{self.input_name}" was misspelled. ' \
                     f'It was assumed as "{self.assumed_name}". '
            output += f'Maybe you meant next options: "{options}"' if options != '' else ''
            return output


@dataclass
class Airport:
    city: City
    name: str
    code: str
    is_found: bool
    location: tuple

    def __repr__(self) -> str:
        return f'{self.city}, {self.name}'


@dataclass
class Flight:
    departure: Airport
    destination: Airport
    is_found: bool
    price: float

    @property
    def distance(self) -> float:
        return get_distance(self.departure.location, self.destination.location)

    @property
    def price_per_kilometer(self) -> float:
        return self.price / self.distance

    # def __repr__(self) -> str:
    #     if self.is_found:
    #         return f'{self.departure}  -  {self.destination}  -  {self.distance:.2f}km / ${self.price} = ' \
    #                f'${self.price_per_kilometer:.2f} per km'
    #     else:
    #         return f'{self.departure}  -  {self.destination}  -  No flights found :('


@dataclass
class Route:
    departure: Airport
    destination: Airport


class NoSuchCity(Exception):
    def __init__(self, city: str) -> None:
        super().__init__(f'{city} city not found')


class NoSuchAirport(Exception):
    def __init__(self, city: str) -> None:
        super().__init__(f'Airport not found in the city {city}')


class FlightsNotFound(Exception):
    def __init__(self) -> None:
        super().__init__(f'Unfortunately, there is no any flights to all destinations. Try other routes.')


class FlightOptimizer:

    def __init__(self, departure: str, destinations: Iterable[str]) -> None:
        self.departure = departure
        self.destinations = destinations

    def process(self, show_all_destinations, suggest_options):
        departure_city = self.get_city(self.departure)
        destination_cities = list(map(self.get_city, self.destinations))

        departure_airport = self._get_airport(departure_city)
        destination_airports = list(map(self._get_airport, destination_cities))

        routes = [Route(departure_airport, destination_airport) for destination_airport in destination_airports]

        best_flights = list(map(self._get_best_flight, routes))
        sorted_flights = sorted(best_flights, key=lambda flight: flight.price_per_kilometer)

        if not sorted_flights[0].is_found:
            raise FlightsNotFound()

        # suggestion_text = self.get_suggested_options(sorted_flights) if suggest_options else ''
        #
        # if not show_all_destinations:
        #     sorted_flights = sorted_flights[:1]
        #
        # response = '\n'.join([str(flight) for flight in sorted_flights])
        # response = f'{response}\n{suggestion_text}'

        return sorted_flights[0]

    def get_suggested_options(self, flights):
        options = [flights[0].departure.city.get_message_for_options()]
        for flight in flights:
            options.append(flight.destination.city.get_message_for_options())
        filtered_options = list(filter(lambda x: x is not None, options))
        return '\n'.join(filtered_options)

    @staticmethod
    def _get_best_flight(route: Route) -> Flight:
        departure = route.departure
        destination = route.destination

        if not departure.is_found or not destination.is_found:
            return Flight(is_found=False, departure=departure, destination=destination)

        query = {
            'fly_from': f'airport:{departure.code}',
            'fly_to': f'airport:{destination.code}',
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
            print("NO FLIGHTS", departure.city, destination.city)
            is_found = False
            best_price = float('inf')
        else:
            is_found = True
            best_price = data["data"][destination.city.id]

        return Flight(
            departure=departure,
            destination=destination,
            is_found=is_found,
            price=best_price
        )

    @staticmethod
    def _get_airport(city: City) -> Airport:

        query = {
            'term': city.id,
            'type': 'subentity',
            'location_types': 'airport',
            'active_only': 'true',
            'limit': 1,
            'sort': 'rank'
        }

        response = requests.get(LOCATIONS_URL, params=query)
        data = response.json()

        if 'locations' not in data or len(data['locations']) == 0:
            raise NoSuchAirport(city=city.input_name)

        airport = data['locations'][0]

        return Airport(
            city=city,
            is_found=True,
            name=airport["name"],
            code=airport["code"],
            location=(
                airport["location"]["lat"],
                airport["location"]["lon"]
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
            # raise NoSuchCity(city=city)
            return City(
                input_name=city,
                valid_name=None,
                assumed_name=None,
                id=None,
                correct_name_options=[],
                is_found=False
            )

        cities = data['locations']
        city_name = cities[0]['name']

        if city.lower() != city_name.lower():
            is_found = True
            valid_name = None
            assumed_name = city_name
            correct_name_options = list(map(lambda possible_city: possible_city['name'], cities))
        else:
            is_found = True
            valid_name = city_name
            assumed_name = None
            correct_name_options = list(map(lambda possible_city: possible_city['name'], cities))

        return City(
            input_name=city,
            valid_name=valid_name,
            assumed_name=assumed_name,
            id=cities[0]['id'],
            correct_name_options=correct_name_options,
            is_found=is_found
        )
