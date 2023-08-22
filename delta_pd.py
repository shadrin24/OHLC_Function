import requests
import datetime
from dateutil.relativedelta import relativedelta
import pandas as pd


def ohlc_delta(link: str, years=0, months=0, days=0, hours=0, minutes=0, seconds=0):
    """Функция парсинга json данных в данные ohlc с объемами и дельтой
    :param link: Ссылка на API с данными
    :param years: Кол-во лет
    :param months: Кол-во месяцев
    :param days: Кол-во дней
    :param hours: Кол-во часов
    :param minutes: Кол-во минут
    :param seconds: Кол-во секунд
    :return: Файл с данными ohlc с объемами"""

    df = pd.read_json(link)
    print(df.head())
    print(df)


ohlc_delta("data.json", seconds=2)
# ohlc_delta("https://api.meridian.trade/api/dataset_p8dvpe3dcnezte8hq491?name=GAZP", seconds=2)