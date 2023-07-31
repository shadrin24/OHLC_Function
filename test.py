import datetime
from dateutil.relativedelta import relativedelta


def test(data_file: str, years=0, months=0, days=0, hours=0, minutes=0, seconds=0):
    # Чтение файла
    file = open(data_file, "r")
    file_report = open("report.txt", "w")
    lines = file.readlines()
    file.close()

    # Задаем начальные переменные
    step = relativedelta(years=years, months=months, days=days, hours=hours, minutes=minutes, seconds=seconds)
    ohlc_cluster = ''
    ohlc_open = 0.0
    ohlc_high = 0.0
    ohlc_low = 0.0
    ohlc_close = 0.0
    volume = {}
    vol_sum = 0
    file_report.write('<DATE>,<TIME>,<OPEN>,<HIGH>,<LOW>,<CLOSE>,<{VOLUME...}>\n')

    # Определение шага цены и начальной даты по первым строкам данных
    vol = 0
    for line in lines[1:1000]:
        line = line.strip().split(",")
        vol_new = float(line[4])
        # print(line, vol_new, vol)
        if 'date' not in locals():
            date = datetime.datetime.strptime(line[2], '%Y%m%d').date()
            cluster_date_time = datetime.datetime.combine(date, datetime.time(0, 0, 0)) - step
            dif_cost = abs(vol_new - vol)
        if vol_new - vol != 0 and dif_cost > abs(vol_new - vol):
            dif_cost = round(abs(vol_new - vol), 10)
            vol += vol_new

    # Перебор строк с формирование кластера
    for line in lines[1:]:
        line = line.strip().split(",")

        last = float(line[4])
        vol = int(line[5])
        date = datetime.datetime.strptime(line[2], '%Y%m%d').date()
        time = datetime.datetime.strptime(line[3], '%H%M%S').time()
        date_time = datetime.datetime.combine(date, time)

        # Если время в строке данных в диапазоне кластера  - собираем данные по кластеру
        if cluster_date_time + step > date_time >= cluster_date_time:
            ohlc_close = last
            if ohlc_high < last:
                ohlc_high = last
            if ohlc_low > last:
                ohlc_low = last
            if last in volume:
                volume[last] += vol
            else:
                volume.setdefault(last, vol)
            ohlc = [ohlc_cluster, ohlc_open, ohlc_high, ohlc_low, ohlc_close, volume]
        # Иначе печатаем кластер и переходим к следующему диапазону
        else:
            if 'ohlc' in locals():
                file_report.write(str(ohlc)+'\n')
                volume = {}
            while date_time >= cluster_date_time + step:
                cluster_date_time += step
            ohlc_cluster = str(cluster_date_time)
            ohlc_open = last
            ohlc_close = last
            ohlc_high = last
            ohlc_low = last
            if last in volume:
                volume[last] += vol
            else:
                volume.setdefault(last, vol)
            ohlc = [ohlc_cluster, ohlc_open, ohlc_high, ohlc_low, ohlc_close, volume]
    file_report.write(str(ohlc) + '\n')
    file_report.close()


test("GAZP_230310_230410.txt", days=1)
