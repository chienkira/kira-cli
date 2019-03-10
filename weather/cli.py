import click
from .functions import get_weather_info


@click.group()
@click.option("--city", help="City name.")
@click.pass_context
def main(context, city: str):
    context.obj["city"] = city


@main.command()
@click.pass_context
def daily(context):
    return


@main.command()
@click.pass_context
def hourly(context):
    return


def start():
    main(obj={})


if __name__ == "__main__":
    start()
