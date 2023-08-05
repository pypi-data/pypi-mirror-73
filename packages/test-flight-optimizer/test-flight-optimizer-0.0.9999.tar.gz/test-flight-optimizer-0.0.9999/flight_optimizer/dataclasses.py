from dataclasses import dataclass
from typing import Iterable

from haversine import haversine as get_distance


@dataclass
class City:
    is_found: bool
    input_name: str
    id: str = None
    name: str = None
    correct_name_options: Iterable[str] = Iterable

    def __repr__(self):
        return f'{self.name}'

    def get_explanation_message(self):
        if self.is_found:
            if self.name.lower() != self.input_name.lower():
                output = f'Entered city name "{self.input_name}" was misspelled. ' \
                         f'It was assumed as "{self.name}". '

                options = '\", \"'.join(self.correct_name_options[1:])
                output += f'Maybe you meant next options: "{options}"' if options != '' else ''
                return output
        else:
            return f'Entered city name "{self.input_name}" was misspelled. No assumption found.'


@dataclass
class Airport:
    is_found: bool
    name: str = None
    code: str = None
    location: tuple = None

    def __repr__(self) -> str:
        return f'{self.name}'


@dataclass
class Location:
    city: City
    airport: Airport

    def __repr__(self):
        return f'{self.city}, {self.airport}'


@dataclass
class Flight:
    departure: Location
    destination: Location
    is_found: bool
    price: float = float('inf')

    @property
    def distance(self) -> float:
        if self.is_found:
            return get_distance(self.departure.airport.location, self.destination.airport.location)
        else:
            return 1

    @property
    def price_per_kilometer(self) -> float:
        return self.price / self.distance

    def __repr__(self) -> str:
        if self.is_found:
            price_over_distance = f'${self.price} / {self.distance:.0f} km '
            return f'To {str(self.destination):50.50}   {price_over_distance:<20} = ' \
                   f'${self.price_per_kilometer:.2f} per km'
        else:
            if self.departure.airport.is_found and self.destination.airport.is_found:
                return f'To {str(self.destination):50.50}   currently there is no any flights.'
            else:
                return f'To {str(self.destination.city.input_name):50.50}   city was not found.'


@dataclass
class Route:
    departure: Location
    destination: Location

