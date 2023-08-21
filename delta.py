import requests
import datetime
from dateutil.relativedelta import relativedelta


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

    # Читаем данные с API
    data_dict = requests.get(link).json()
    data_list = data_dict["data"]["data"]
    ticker = data_dict["data"]["ticker"]
    name = data_dict["name"]


    # Задаем начальные переменные
    step = relativedelta(years=years, months=months, days=days, hours=hours, minutes=minutes, seconds=seconds)
    ohlc_cluster = ''
    ohlc_open = 0.0
    ohlc_high = 0.0
    ohlc_low = 0.0
    ohlc_close = 0.0
    volume = {}
    vol_sum = 0
    sel_vol = {}
    buy_vol = {}
    delta_type = ""
    start_date = datetime.datetime.strptime(data_list[0][0][:10], '%Y-%m-%d').date()
    cluster_date_time = datetime.datetime.combine(start_date, datetime.time(0, 0, 0)) - step
    previously_cost = float(data_list[0][1])
    file_report = open("report.txt", "w")
    file_report.write('<DATE>,<TIME>,<OPEN>,<HIGH>,<LOW>,<CLOSE>, <{SEL_VOL...}>, <{BUY_VOL...}>, <DELTA_TYPE>, <{VOLUME...}>\n')

    # Перебор строк с формированием кластера
    for line in data_list:
        cost = float(line[1])
        vol = int(line[2])
        date = datetime.datetime.strptime(line[0][:10], '%Y-%m-%d').date()
        time = datetime.datetime.strptime(line[0][11:], '%H:%M:%S').time()
        date_time = datetime.datetime.combine(date, time)


        # Если время в строке данных в диапазоне кластера  - собираем данные по кластеру
        if cluster_date_time + step > date_time >= cluster_date_time:
            ohlc_close = cost
            ohlc_high = max(cost, ohlc_high)
            ohlc_low = min(cost, ohlc_high)
            if cost in volume:
                volume[cost] += vol
            else:
                volume.setdefault(cost, vol)

            # Подсчет кол-ва позиций (buy_vol, sel_vol)
            if cost < previously_cost:
                if cost in sel_vol:
                    sel_vol[cost] += vol
                else:
                    sel_vol.setdefault(cost, vol)
            elif cost > previously_cost:
                if cost in buy_vol:
                    buy_vol[cost] += vol
                else:
                    buy_vol.setdefault(cost, vol)

            ohlc = [ohlc_cluster, ohlc_open, ohlc_high, ohlc_low, ohlc_close, sel_vol, buy_vol, delta_type, volume]
        # Иначе печатаем кластер и переходим к следующему диапазону
        else:
            if 'ohlc' in locals():
                if sum(buy_vol.values()) > sum(sel_vol.values()):
                    delta_type = 'buy_vol'
                elif sum(buy_vol.values()) < sum(sel_vol.values()):
                    delta_type = 'sel_vol'
                ohlc = [ohlc_cluster, ohlc_open, ohlc_high, ohlc_low, ohlc_close, sel_vol, buy_vol, delta_type, volume]
                file_report.write(str(ohlc)+'\n')
                volume = {}
                buy_vol = {}
                sel_vol = {}
            while date_time >= cluster_date_time + step:
                cluster_date_time += step
            ohlc_cluster = str(cluster_date_time)
            ohlc_open = cost
            ohlc_close = cost
            ohlc_high = cost
            ohlc_low = cost
            if cost in volume:
                volume[cost] += vol
            else:
                volume.setdefault(cost, vol)

            # Подсчет кол-ва позиций (buy_vol, sel_vol)
            if cost < previously_cost:
                if cost in sel_vol:
                    sel_vol[cost] += vol
                else:
                    sel_vol.setdefault(cost, vol)
            elif cost > previously_cost:
                if cost in buy_vol:
                    buy_vol[cost] += vol
                else:
                    buy_vol.setdefault(cost, vol)
            ohlc = [ohlc_cluster, ohlc_open, ohlc_high, ohlc_low, ohlc_close, sel_vol, buy_vol, delta_type, volume]
        previously_cost = cost
    file_report.write(str(ohlc) + '\n')

    file_report.close()


ohlc_delta("https://api.meridian.trade/api/dataset_p8dvpe3dcnezte8hq491?name=GAZP", seconds=2)
