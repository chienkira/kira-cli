from colorama import Fore, Back, Style
import requests
import time
import sys
import itertools
import threading
import datetime

done = False
timeout = 100  # 10 seconds


def get_weather_info(city: str, lang: str, interval: str):
    """
    Get weather information using darksky api
    :param city: city name, ex: Tokyo
    :param interval: daily or hourly
    :param lang: language
    :return:
    """
    global done
    # start displaying loader
    t = threading.Thread(target=animate_loader)
    t.start()

    lat_lon = get_lat_lon_of_city(city)
    api_key = "3b758a15a05e9e710e440f11cc110e1d"
    url = " https://api.darksky.net/forecast/{}/{}".format(api_key, lat_lon)
    parameters = {
        "lang": lang,
        "units": "si",
        "exclude": "minutely,hourly,daily,alerts,flags".replace(interval + ',', '')
    }
    response = requests.get(url, params=parameters)

    # mark that "hard job" was done
    done = True
    print()

    if response.status_code != 200:
        print(Fore.RED + "Failed")
        print(Fore.RED + 'Could not connect darksky api.')
        response and print(response.json())
        return {}

    return response.json()


def get_lat_lon_of_city(city: str):
    api_key = "pk.eyJ1IjoiY2hpZW5raXJhIiwiYSI6ImNqdDZ2ajZiNTA3Ym40M2p6NTc0ejdiN2IifQ.axZZIqJfI0N-eA-GPHI9Ow"
    url = "https://api.mapbox.com/geocoding/v5/mapbox.places/{}.json?access_token={}".format(city, api_key)
    response = requests.get(url)
    data = response.json()
    coordinates = data['features'][0]['geometry']['coordinates']

    return "{},{}".format(coordinates[1], coordinates[0])


def pretty_print(data):
    currently = data.get('currently')
    daily = data.get('daily')
    hourly = data.get('hourly')

    if data:
        print(Fore.WHITE + "<Tìm thấy trong khu vực {}> ".format(data['timezone']))

    if currently:
        print(Back.LIGHTCYAN_EX + Fore.BLACK + ' Hiện tại__________')
        print(Fore.LIGHTCYAN_EX + "Thời tiết {}, nhiệt độ khoảng {:.1f}°C và vận tốc gió khoảng {:.1f}m/s.".format(
            currently['summary'],
            currently['apparentTemperature'],
            currently['windSpeed']))
        print()

    if daily:
        print(Back.LIGHTBLUE_EX + Fore.BLACK + ' Trong 7 ngày tới__')
        print(Fore.LIGHTBLUE_EX + "Dự báo: " + daily['summary'])
        for day in daily['data']:
            print(Fore.LIGHTYELLOW_EX + " __{}__\t".format(
                datetime.datetime.fromtimestamp(day['time']).strftime("%m/%d(%a)")), end='')
        print()
        for day in daily['data']:
            print(Fore.LIGHTBLUE_EX + "   {}\t".format(get_readable_icon(day['icon'])), end='')
        print()
        for day in daily['data']:
            print("  {:.1f} ~ {:.1f}°C\t".format(day['temperatureLow'], day['temperatureHigh']), end='')
        print()
        for day in daily['data']:
            print(" 〻 {:.1f}m/s\t".format(day['windSpeed']), end='')
        print()
        print()

    if hourly:
        print(Back.LIGHTMAGENTA_EX + Fore.BLACK + ' Trong 24 giờ tới__')
        print(Fore.LIGHTMAGENTA_EX + "Dự báo: " + hourly['summary'])
        print()


def animate_loader():
    global timeout
    for c in itertools.cycle(['|', '/', '-', '\\']):
        if done:
            break
        sys.stdout.write('\rĐang hỏi ông trời ' + c)
        sys.stdout.flush()
        time.sleep(0.1)
        # prevent infinite loop
        timeout -= 1
        if timeout < 0:
            break


def get_readable_icon(icon):
    mapping = {
        "rain": "trời mưa",
        "cloudy": "trời mây",
        "snow": "có tuyết",
        "wind": "có gió",
        "clear": "trời nắng"
    }
    matching = [v for k, v in mapping.items() if k in icon]
    return ','.join(matching)
