import pandas as pd
import numpy as np
# import openpyxl


# Если байер присвоит 1 в ячейку
def buyer(s):
    s_diff = s - s.shift(1)
    s_diff = s_diff.map(np.sign)
    s_diff = s_diff.replace(to_replace=0, method='ffill')
    return s_diff[s_diff == 1]


# Если селлер присвоит 1 в ячейку
def seller(s):
    s_diff = s - s.shift(1)
    s_diff = s_diff.map(np.sign)
    s_diff = s_diff.replace(to_replace=0, method='ffill')
    return abs(s_diff[s_diff == -1])


# Присвоит тип дельты в кластере
def delta_type(s):
    s = s.map(np.sign).fillna(0)
    s = s.replace({0: 'equals',
                   1: 'buyer',
                   -1: 'seller'})
    return s


def ohlc_delta(link: str, time_cluster: str):
    """Функция парсинга json данных в данные ohlc с объемами и дельтой
    :param link: Ссылка на API с данными
    :param time_cluster: Кластер формата pd.Grouper(freq=...)"""

    # Получаем датафрейм с API
    data_json = pd.read_json(link)
    data_list = data_json["data"]["data"]
    data_np = np.array(data_list)
    df1 = pd.DataFrame(data_np, columns=['date_time', 'cost', 'value'])
    df1['cost'] = pd.to_numeric(df1['cost'])
    df1['value'] = pd.to_numeric(df1['value'])
    df1['date_time'] = pd.to_datetime(df1['date_time'])

    # Определяем колличество байеров и селлеров
    df1['buyer'] = (buyer(df1['cost']) * df1['value']).fillna(0).astype(int)
    df1['seller'] = (seller(df1['cost']) * df1['value']).fillna(0).astype(int)

    # Группируем в кластер
    df_cluster = df1.groupby(pd.Grouper(key='date_time', axis=0, freq=time_cluster)).agg({'cost': ['first', 'max', 'min', 'last'],
                                                                                          'seller': 'sum',
                                                                                          'buyer': 'sum',
                                                                                          'value': 'sum'}).dropna()
    # Добавляем тип дельты
    df_cluster['delta_type'] = df_cluster['buyer'] - df_cluster['seller']
    df_cluster['delta_type'] = delta_type(df_cluster['delta_type'])

    # Оформляем
    df_cluster = df_cluster.reset_index()
    df_cluster.columns = ['date_time', 'open', 'high', 'low', 'close', 'buyer', 'seller', 'value', 'delta_type']
    df_cluster.index.name = 'index'
    # print(df_cluster)
    df_cluster.to_csv('report.csv')


# ohlc_delta("data.json", '2S')
ohlc_delta("https://api.meridian.trade/api/dataset_p8dvpe3dcnezte8hq491?name=GAZP", '15Min')
