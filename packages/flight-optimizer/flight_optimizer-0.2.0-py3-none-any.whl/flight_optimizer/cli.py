import click
from .utils import FlightOptimizer


@click.command()
@click.option('--from', '-f', 'departure', required=True, type=str, help="Departure City")
@click.option('--to', '-t', 'destinations', required=True, type=str, help="Destination City (can be multiple)",
              multiple=True)
@click.option('--all-destinations', '-a', is_flag=True, default=False,
              help="Shows flights for every destination. (default - shows only the best destination")
@click.option('--explain-result', '-e', is_flag=True, default=False,
              help="If entered cities were misspelled, then it explains what cities were searched and "
                   "suggests correct city name options")
def search(departure, destinations, all_destinations, explain_result):
    """CLI that searches for the cheapest airplane flights per kilometer."""

    try:
        flight_optimizer = FlightOptimizer(departure, destinations)
        flights = flight_optimizer.process()

        best_flight = flights[0]

        if best_flight.is_found:
            click.echo(f'From {best_flight.departure}:')
            click.echo(best_flight)

            if all_destinations:
                for flight in flights[1:]:
                    click.echo(flight)
        else:
            click.echo("Unfortunately, there is no any flights to all destinations. Try other routes.")

        if explain_result:
            click.echo(FlightOptimizer.get_result_explanation(flights))

    except Exception:
        click.echo("Something went wrong.")
