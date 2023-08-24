import pandas as pd
import numpy as np

ticker = pd.DataFrame({"open": [1, 0, -1, 4, 4, 3, 4, 5, 2, 1, 2],
                       'date': [1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2]})
print(ticker)


def buyer(s):
    s_diff = s - s.shift(1)
    s_diff = s_diff.map(np.sign)
    # s_diff = s_diff.fillna(0)
    s_diff = s_diff.replace(to_replace=0, method='ffill')
    return s_diff[s_diff == 1]
    # return s_diff[s_diff==1].shape[0]


def seller(s):
    s_diff = s - s.shift(1)
    print('s---', s_diff)
    # s_diff = s_diff.map(np.sign)
    # s_diff = s_diff.fillna(0)
    # s_diff = s_diff.replace(to_replace=0, method='ffill')
    # print('---s \n', s_diff, '\n---d \n', s_diff[s_diff == -1].shape[0])

    return s_diff


# ticker['buyer'] = ticker['open']-ticker['open'].shift(1)
ticker['buyer'] = buyer(ticker['open'])
ticker['seller'] = ticker['open']
ticker['close'] = ticker['open']
ticker['group_all'] = 1
print('gr', ticker)
# ticker2 = ticker.groupby('group_all').agg({'buyer': my_func_buyer,
#                                            'seller': my_func_seller})

# ticker2 = ticker.agg({'buyer': my_func_buyer,
#                       'seller': my_func_seller})
# ticker2 = ticker.groupby('date').agg({'open': 'first',
#                                       'close': 'last',
#                                       'buyer': my_func_buyer,
#                                       'seller': my_func_seller})
# print(ticker2)
