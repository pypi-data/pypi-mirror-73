import click


@click.command()
@click.option('--from', '-f', 'departure', required=True, type=str, help="Departure City")
@click.option('--to', '-t', 'destinations', required=True, type=str, help="Destination City (can be multiple)",
              multiple=True)
@click.option('--all-destinations', '-a', is_flag=True, default=False)
def search(departure, destinations, all_destinations):
    # click.echo(str(departure), str(destinations))
    print(departure, destinations, all_destinations)
