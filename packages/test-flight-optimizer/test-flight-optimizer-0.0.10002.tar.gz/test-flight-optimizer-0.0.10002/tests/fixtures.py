import pytest
from click.testing import CliRunner
from flight_optimizer.dataclasses import Flight, Airport, City, Location


@pytest.fixture(scope='module')
def runner():
    return CliRunner()


@pytest.fixture()
def test_city_paris():
    return City(
        id='paris_fr',
        name='Paris',
        input_name='pari',
        is_found=True,
        correct_name_options=['Paris', 'Parikia', 'Parintins', 'Saint Joseph Parish']
    )


@pytest.fixture()
def test_airport_paris():
    return Airport(
        code='ORY',
        name='Paris Orly',
        location=(48.723333, 2.379444),
        is_found=True
    )


@pytest.fixture()
def test_location_paris(test_city_paris, test_airport_paris):
    return Location(
        city=test_city_paris,
        airport=test_airport_paris
    )


@pytest.fixture()
def test_city_london():
    return City(
        id='london_gb',
        name='London',
        input_name='london',
        is_found=True,
        correct_name_options=['Londrina', 'East London']
    )


@pytest.fixture()
def test_airport_london():
    return Airport(
        code='LHR',
        name='Heathrow',
        location=(51.4775, -0.461389),
        is_found=True
    )


@pytest.fixture()
def test_location_london(test_city_london, test_airport_london):
    return Location(
        city=test_city_london,
        airport=test_airport_london
    )


@pytest.fixture()
def test_city_new_york():
    return City(
        id='new-york-city_ny_us',
        name='New York',
        input_name='new york',
        is_found=True,
        correct_name_options=['New York']
    )


@pytest.fixture()
def test_city_not_found():
    return Location(
        city=City(is_found=False, input_name='asdghjaskgdj'),
        airport=Airport(is_found=False)
    )


@pytest.fixture()
def test_airport_new_york():
    return Airport(
        code='JFK',
        name='John F. Kennedy International',
        location=(40.639722, -73.778889),
        is_found=True
    )


@pytest.fixture()
def test_location_new_york(test_city_new_york, test_airport_new_york):
    return Location(
        city=test_city_new_york,
        airport=test_airport_new_york
    )


@pytest.fixture()
def test_flight_from_paris_to_london(test_location_paris, test_location_london):
    return Flight(
        departure=test_location_paris,
        destination=test_location_london,
        is_found=True,
        price=731
    )


@pytest.fixture()
def test_flight_from_paris_to_new_york(test_location_paris, test_location_new_york):
    return Flight(
        departure=test_location_paris,
        destination=test_location_new_york,
        is_found=True,
        price=383
    )


@pytest.fixture()
def test_flight_not_found(test_location_paris, test_location_new_york):
    return Flight(
        departure=test_location_paris,
        destination=test_location_new_york,
        is_found=False,
        price=383
    )


@pytest.fixture()
def test_no_flight_due_to_city_not_found(test_city_not_found, test_location_london):
    return Flight(
        departure=test_city_not_found,
        destination=test_location_london,
        is_found=False
    )
