from flight_optimizer.cli import search
from flight_optimizer.utils import FlightOptimizer
from tests.fixtures import *
from tests.outputs import Output


def test_search_without_arguments(runner):
    response = runner.invoke(search, [])
    assert response.exit_code == 2
    assert response.output == Output.TEST_SEARCH_WITHOUT_ARGUMENTS


def test_search_one_argument_is_missing(runner):
    response = runner.invoke(search, ['--from', 'bishkek'])
    assert response.exit_code == 2
    assert response.output == Output.TEST_SEARCH_ONE_ARGUMENT_IS_MISSING


def test_search_with_wrong_argument(runner):
    response = runner.invoke(search, ['--fly', 'bishkek'])
    assert response.exit_code == 2
    assert response.output == Output.TEST_SEARCH_WITH_WRONG_ARGUMENT


def test_search_help_message(runner):
    response = runner.invoke(search, '--help')
    assert response.exit_code == 0
    assert response.output == Output.TEST_SEARCH_HELP_MESSAGE


def test_search(mocker, runner, test_city_london, test_location_london,
                test_flight_from_paris_to_london):
    mocker.patch('flight_optimizer.utils.FlightOptimizer.get_city', return_value=test_city_london)
    mocker.patch('flight_optimizer.utils.FlightOptimizer._get_airport', return_value=test_location_london)
    mocker.patch('flight_optimizer.utils.FlightOptimizer._get_best_flight',
                 return_value=test_flight_from_paris_to_london)

    result = runner.invoke(search, ('--from', 'paris', '--to', 'london', '-a'))
    assert result.exit_code == 0
    assert result.output == Output.TEST_SEARCH


def test_search_all_destinations(mocker, runner, test_city_new_york,
                                 test_location_new_york, test_flight_from_paris_to_new_york):
    mocker.patch('flight_optimizer.utils.FlightOptimizer.get_city', return_value=test_city_new_york)
    mocker.patch('flight_optimizer.utils.FlightOptimizer._get_airport', return_value=test_location_new_york)
    mocker.patch('flight_optimizer.utils.FlightOptimizer._get_best_flight',
                 return_value=test_flight_from_paris_to_new_york)

    result = runner.invoke(search,
                           ('--from', 'paris', '--to', 'new york',
                            '--to', 'new york', '--to', 'new york', '--all-destinations'))
    assert result.exit_code == 0
    assert result.output == Output.TEST_SEARCH_ALL_DESTINATIONS


def test_search_explain_result(mocker, runner, test_city_new_york,
                               test_location_new_york, test_flight_from_paris_to_new_york):
    mocker.patch('flight_optimizer.utils.FlightOptimizer.get_city', return_value=test_city_new_york)
    mocker.patch('flight_optimizer.utils.FlightOptimizer._get_airport', return_value=test_location_new_york)
    mocker.patch('flight_optimizer.utils.FlightOptimizer._get_best_flight',
                 return_value=test_flight_from_paris_to_new_york)

    result = runner.invoke(search, ('--from', 'pari', '--to', 'new york', '--explain-result'))
    assert result.exit_code == 0
    assert result.output == Output.TEST_SEARCH_EXPLAIN_RESULTS


def test_search_flight_not_found(mocker, runner, test_city_new_york,
                                 test_location_new_york, test_flight_not_found):
    mocker.patch('flight_optimizer.utils.FlightOptimizer.get_city', return_value=test_city_new_york)
    mocker.patch('flight_optimizer.utils.FlightOptimizer._get_airport', return_value=test_location_new_york)
    mocker.patch('flight_optimizer.utils.FlightOptimizer._get_best_flight',
                 return_value=test_flight_not_found)

    result = runner.invoke(search, ('--from', 'pari', '--to', 'new york'))
    assert result.exit_code == 0
    assert result.output == Output.TEST_SEARCH_FLIGHT_NOT_FOUND


def test_search_city_not_found(mocker, runner, test_city_not_found,
                               test_location_london, test_no_flight_due_to_city_not_found):
    mocker.patch('flight_optimizer.utils.FlightOptimizer.get_city', return_value=test_city_not_found)
    mocker.patch('flight_optimizer.utils.FlightOptimizer._get_airport', return_value=test_location_london)
    mocker.patch('flight_optimizer.utils.FlightOptimizer._get_best_flight',
                 return_value=test_no_flight_due_to_city_not_found)

    result = runner.invoke(search, ('--from', 'asdghjaskgdj', '--to', 'new york', '-e'))
    assert result.exit_code == 0
    assert result.output == Output.TEST_SEARCH_NO_FLIGHT_DUE_TO_CITY_NOT_FOUND


def test_flight_optimizer_get_result_explanation(mocker, test_city_paris, test_location_london,
                                                 test_flight_from_paris_to_london):
    mocker.patch('flight_optimizer.utils.FlightOptimizer.get_city', return_value=test_city_paris)
    mocker.patch('flight_optimizer.utils.FlightOptimizer._get_airport', return_value=test_location_london)
    mocker.patch('flight_optimizer.utils.FlightOptimizer._get_best_flight',
                 return_value=test_flight_from_paris_to_london)

    optimizer = FlightOptimizer('pari', ['london'])
    flights = optimizer.process()
    assert len(flights) == 1
    assert optimizer.get_result_explanation(flights) == Output.TEST_FLIGHT_OPTIMIZER_GET_RESULT_EXPLANATION


def test_flight_optimizer_process(mocker, test_city_paris,
                                  test_location_london, test_flight_from_paris_to_london):
    mocker.patch('flight_optimizer.utils.FlightOptimizer.get_city', return_value=test_city_paris)
    mocker.patch('flight_optimizer.utils.FlightOptimizer._get_airport', return_value=test_location_london)
    mocker.patch('flight_optimizer.utils.FlightOptimizer._get_best_flight',
                 return_value=test_flight_from_paris_to_london)

    optimizer = FlightOptimizer('paris', ['london', 'new york', 'bishkek'])
    flights = optimizer.process()
    assert len(flights) == 3
    assert flights[0].departure.city.name == 'Paris'
    assert flights[0].departure.airport.code == 'ORY'
    assert flights[0].destination.city.name == 'London'
    assert flights[0].destination.airport.code == 'LHR'
    assert flights[0].is_found
    assert flights[0].price_per_kilometer == 1.9910164726855917
