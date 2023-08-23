import requests
import datetime
from dateutil.relativedelta import relativedelta
import pandas as pd
import numpy as np


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

    # Получаем датафрейм с API
    data_json = pd.read_json(link)
    data_list = data_json["data"]["data"]
    data_np = np.array(data_list)
    df1 = pd.DataFrame(data_np, columns=['date_time', 'cost', 'value']).set_index('date_time')
    df1.index = pd.to_datetime(df1.index)
    # df1['date_time'] = pd.to_datetime(df1['date_time'])
    df1['cost'] = pd.to_numeric(df1['cost'])
    df1['value'] = pd.to_numeric(df1['value'])
    # ticker = data_json["data"]["ticker"]
    # df2 = df1['date_time'].str.split(' ', expand=True)
    # df2.columns = ['date', 'time']
    # df = pd.concat([df2, df1], axis=1).drop('date_time', axis=1)

    # df_cluster = df1.groupby(pd.Grouper(key='date_time', axis=0, freq='2S')).agg({'cost': ['max', 'min', 'first', 'last']}).dropna()

    df_cluster = df1['cost'].resample('2S').ohlc().dropna()
    # df_cluster = df_cluster.loc[df_cluster['cost'] != 0]
    # print(df_cluster)
    # print(df_cluster)
    print(df_cluster)


ohlc_delta("data.json", seconds=2)
# ohlc_delta("https://api.meridian.trade/api/dataset_p8dvpe3dcnezte8hq491?name=GAZP", seconds=2)
