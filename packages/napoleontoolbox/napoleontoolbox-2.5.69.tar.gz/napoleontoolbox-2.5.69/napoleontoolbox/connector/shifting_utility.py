from datetime import datetime
import pandas as pd


def shift_daily_crypto_compare_signal(ssj=None, local_root_directory=None, path_to_hourly_signal = None, shift = 1, starting_date=None, running_date=None, frequence='daily'):
    try:
        data = pd.read_pickle(path_to_hourly_signal)
    except:
        path_to_hourly_signal = '../'+path_to_hourly_signal
        local_root_directory =  '../'+local_root_directory
        data = pd.read_pickle(path_to_hourly_signal)

    data = data.drop_duplicates()
    delta = shift
    data['datetime'] = data.index.date
    data['hour'] = data.index.hour
    assert data.iloc[0]['hour'] == 0
    data[['close', 'high', 'low', 'open', 'volumefrom', 'volumeto']] = data[['close', 'high', 'low', 'open', 'volumefrom', 'volumeto']].shift(-delta)
    data = data.dropna()
    data = data.groupby(['datetime']).agg({'close': 'last', 'high': 'max', 'low': 'min', 'open': 'first', 'volumefrom': 'sum', 'volumeto' : 'sum'})
    if delta >0:
        data.index = pd.DatetimeIndex(data.index) + pd.DateOffset(1)
        data = data[data.index<datetime.today()]
    else:
        data = data[:-1]
    freqly_pkl_file_name_suffix = '_' + frequence + '_returns.pkl'
    dates_stub = starting_date.strftime('%d_%b_%Y') + '_' + running_date.strftime('%d_%b_%Y')
    saving_return_path = local_root_directory + ssj + '_' + dates_stub + freqly_pkl_file_name_suffix
    data.to_pickle(saving_return_path)
    return data