import pandas as pd
import numpy as np

ticker = pd.DataFrame({"open":[1,0,-1,4,4,3,4,5,2,1,2],
'date':[1,1,1,1,1,1,1,2,2,2,2]})
print(ticker)

def my_func_buyer(s):
    s_diff = s - s.shift(1)
    s_diff = s_diff.map(np.sign)
    s_diff = s_diff.fillna(0)
    s_diff = s_diff.replace(to_replace=0, method='ffill')

    return s_diff[s_diff==1].shape[0]


def my_func_saler(s):
    s_diff = s - s.shift(1)
    s_diff = s_diff.map(np.sign)
    s_diff = s_diff.fillna(0)
    print('---s \n', s_diff, '\n---d \n', s_diff.replace(to_replace=0, method='ffill'))
    s_diff = s_diff.replace(to_replace=0, method='ffill')

    return s_diff[s_diff==-1].shape[0]

ticker['buyer'] = ticker['open']
ticker['saler'] = ticker['open']
ticker['close'] = ticker['open']
ticker2 = ticker.groupby('date').agg({'open':'first',
'close':'last',
'buyer':my_func_buyer,
'saler':my_func_saler})
print(ticker2)