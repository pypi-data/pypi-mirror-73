from datetime import date, timedelta
from typing import Iterable

import requests
from .dataclasses import Airport, City, Flight, Location

DATE_FORMAT = "%d/%m/%Y"

AGGREGATION_FLIGHTS_URL = "https://api.skypicker.com/aggregation_flights"
LOCATIONS_URL = "https://api.skypicker.com/locations"


class FlightOptimizer:

    def __init__(self, departure: str, destinations: Iterable[str]) -> Iterable[Flight]:
        '''
        :param departure: from city (user's input)
        :param destinations: to cities, might be multiple (user's input)
        '''
        self.departure = departure
        self.destinations = destinations

    def process(self):
        '''Processes all steps of searching the best flights to all destinations

        :return: list of flights data sorted by price per kilometer
        '''

        # get cities' data
        departure_city = self.get_city(self.departure)
        destination_cities = list(map(self.get_city, self.destinations))

        # get airports' data based on cities' data
        departure_airport = self._get_airport(departure_city)
        destination_airports = list(map(self._get_airport, destination_cities))

        # search for the best flights
        best_flights = [
            self._get_best_flight(departure_airport, destination_airport)
            for destination_airport in destination_airports
        ]

        # sort flights based on price per kilometer parameter
        sorted_flights = sorted(best_flights, key=lambda flight: flight.price_per_kilometer)

        return sorted_flights

    @staticmethod
    def get_result_explanation(flights: Iterable[Flight]) -> str:
        '''Generates search explanation message

        :param flights: for which explanations were requested
        :return: explanation and suggestions message (string)
        '''

        departure_explanation = flights[0].departure.city.get_explanation_message()
        destination_explanations = [flight.destination.city.get_explanation_message() for flight in flights]

        explanations = [departure_explanation] + destination_explanations
        filtered_explanations = list(filter(lambda x: x is not None, explanations))

        message = '\n'.join(filtered_explanations) if filtered_explanations else 'Every city was correctly spelled.'
        return f'\nExplanation and suggestions:\n{message}'

    @staticmethod
    def _get_best_flight(departure: Location, destination: Location) -> Flight:
        '''Searches the best flight between two cities

        :param departure: main airport of city
        :param destination: main airport of city
        :return: data about best flight
        '''

        # if departure or destination airport was not found return not found flight
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

        # if there is no destination in response, set flight's is_found field to False
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
        '''Searches for airport of the city

        :param city: name and id
        :return: data about the airport: name, international code and location
        '''

        query = {
            'term': city.id,
            'type': 'subentity',
            'location_types': 'airport',
            'active_only': 'true',
            'limit': 1,
            'sort': 'rank'
        }

        # if city was not found, then return not found airport
        if not city.is_found:
            return Location(city=city, airport=Airport(is_found=False))

        response = requests.get(LOCATIONS_URL, params=query)
        data = response.json()

        # if there is no any airports in response, set airport's is_found field to False
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
        """Searches for the given city

        :param city: name from user input
        :return: data about the city: name and id
        """
        query = {
            'term': city,
            'location_types': 'city',
            'active_only': 'true',
            'limit': 5,  # get 5 possible cities for suggestions
        }

        response = requests.get(LOCATIONS_URL, params=query)
        data = response.json()

        # if there is any data in response, set city's is_found field to False
        if 'locations' not in data or len(data['locations']) == 0:
            return City(is_found=False, input_name=city)

        cities = data['locations']

        # get 5 city names and their country for suggestions
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
