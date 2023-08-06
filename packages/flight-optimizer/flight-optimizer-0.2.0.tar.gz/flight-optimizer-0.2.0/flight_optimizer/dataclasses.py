from dataclasses import dataclass, field
from typing import Iterable

from haversine import haversine as get_distance


@dataclass
class City:
    is_found: bool
    input_name: str
    id: str = None
    name: str = None
    correct_name_options: Iterable[tuple] = field(default_factory=lambda: [])

    def __repr__(self):
        return f'{self.name}'

    def get_explanation_message(self):
        """Returns information about search and suggests city options in case misspelled input"""

        if self.is_found:
            if self.name.lower() != self.input_name.lower():
                output = f'City "{self.input_name}" was misspelled. ' \
                         f'It was assumed as "{self.name}" in {self.correct_name_options[0][1]}.'

                options = [f'"{option[0]}" in {option[1]}' for option in self.correct_name_options[1:]]
                options = ', '.join(options)

                output += f'\nMaybe you meant next options: {options}' if options != '' else ''
                return output
        else:
            return f'City "{self.input_name}" was misspelled. No assumption found.'


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
    price: float = float('inf')  # set to 'inf' in case flight was not found

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
                # if airport were found, it means there is no any flights
                return f'To {str(self.destination):50.50}   currently there is no any flights.'
            else:
                # cities or airports were not found
                return f'To {str(self.destination.city.input_name):50.50}   city was not found.'


@dataclass
class Route:
    departure: Location
    destination: Location

