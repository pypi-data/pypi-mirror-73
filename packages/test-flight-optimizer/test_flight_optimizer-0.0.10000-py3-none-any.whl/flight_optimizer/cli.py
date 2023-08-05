import click
from .utils import FlightOptimizer


@click.command()
@click.option('--from', '-f', 'departure', required=True, type=str, help="Departure City")
@click.option('--to', '-t', 'destinations', required=True, type=str, help="Destination City (can be multiple)",
              multiple=True)
@click.option('--show-all-destinations', '-a', is_flag=True, default=False,
              help="Shows flights for every destination. Otherwise shows only the best destination")
@click.option('--explain-result', '-e', is_flag=True, default=False,
              help="If entered cities were misspelled, than it explains what cities were searched and "
                   "suggests correct city name options")
def search(departure, destinations, show_all_destinations, explain_result):
    try:
        flight_optimizer = FlightOptimizer(departure, destinations)
        flights = flight_optimizer.process()

        best_flight = flights[0]

        if best_flight.is_found:
            click.echo(f'From {best_flight.departure}:')
            click.echo(best_flight)

            if show_all_destinations:
                for flight in flights[1:]:
                    click.echo(flight)
        else:
            click.echo("Unfortunately, there is no any flights to all destinations. Try other routes.")

        if explain_result:
            click.echo(flight_optimizer.get_result_explanation(flights))

        destinations = [
            {
                'city': flight.destination.city.name,
                'airport': flight.destination.airport.name,
                'price': flight.price,
                'distance': f'{flight.distance:.0f}',
                'price_per_km': f'{flight.price_per_kilometer:.2f}',
                'is_reachable': flight.is_found
            }
            if flight.is_found else
            {
                'city': flight.destination.city.name,
                'is_reachable': flight.is_found
            }
            for flight in flights
        ]

        result = {
            'departure': {
                'city': flights[0].departure.city.name,
                'airport': flights[0].departure.airport.name
            },
            'destinations': destinations
        }

        print('\n\n Api Response')
        print(result['departure'])
        for d in result['destinations']:
            print(d)

    except Exception:
        click.echo("Something went wrong. Try again.")


@click.command()
@click.option('--from', '-f', 'city', required=True, type=str, help="City")
def get_locations(city):
    try:
        response = FlightOptimizer.get_city(city)
        ret = {
            "city": response.input_name,
            "possible_cities": response.correct_name_options
        }
        print(ret)
        print(response)

    except Exception as exception:
        click.echo(str(exception))


