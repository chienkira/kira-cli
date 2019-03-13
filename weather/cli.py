from colorama import init
import click
from .functions import get_weather_info, pretty_print

init(autoreset=True)


@click.command()
@click.argument("city")
@click.option("--language", help="Language Ex: ja, en.", default="en")
@click.option("--interval", help="Interval (daily or hourly). Default is daily.", default="daily")
def main(city: str, language: str, interval: str):
    """Kira-cli | display weather information that retrieve from darksky API"""
    data = get_weather_info(city, language, interval)
    pretty_print(data)


def start():
    main(obj={})


if __name__ == "__main__":
    start()
