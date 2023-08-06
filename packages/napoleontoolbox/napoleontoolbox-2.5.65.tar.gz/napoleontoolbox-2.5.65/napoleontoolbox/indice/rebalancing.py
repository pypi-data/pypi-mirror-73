from napoleontoolbox.utility import date_utility
import pandas as pd
import numpy as np
from napoleontoolbox.utility import metrics
import operator

def past_volatility(x):
    return np.sqrt(252)*np.std(x)

def vol_target_indice_rebalancing(weight_data=None, vol_target = None, volatility_window = 252, vol_target_inception_date = None, initial_value = 100.):
    assert vol_target is not None
    weight_data['indice_returns'] = weight_data['indice'].pct_change()
    weight_data['rolling_vol_indice'] = weight_data['indice_returns'].rolling(volatility_window).apply(past_volatility)
    is_past_volatility_not_available_at_start =  np.isnan(weight_data.loc[vol_target_inception_date,'rolling_vol_indice'])
    assert not is_past_volatility_not_available_at_start
    print(f'date range before filtering {min(weight_data.index)} {max(weight_data.index)}')
    weight_data = weight_data.loc[weight_data.index >= vol_target_inception_date, :]
    print(f'date range after filtering {min(weight_data.index)} {max(weight_data.index)}')
    assert vol_target_inception_date in weight_data.index
    volatility_factor = None
    target_vol_values_list = []
    for date_index, row in weight_data.iterrows():
        if date_index == vol_target_inception_date:
            assert row['is_rebalancing']
            volatility_factor = vol_target / weight_data.loc[vol_target_inception_date,'rolling_vol_indice']
            previous_value = initial_value
            target_vol_values_list.append({'Date': vol_target_inception_date, 'indice': initial_value, 'volatility_factor':np.nan})
            continue
        current_return = weight_data.loc[date_index, 'indice_returns']
        value = previous_value * (1 + current_return * volatility_factor)
        current_values = {'Date' : date_index, 'indice': value, 'volatility_factor':volatility_factor}
        target_vol_values_list.append(current_values)
        # we readjust the volatility factor    
        if row['is_rebalancing']:
            volatility_factor = vol_target / weight_data.loc[date_index,'rolling_vol_indice']
        previous_value = value

    target_vol_values_df = pd.DataFrame(target_vol_values_list)
    target_vol_values_df.index = pd.to_datetime(target_vol_values_df['Date'])
    target_vol_values_df.drop('Date', axis=1, inplace=True)
    return target_vol_values_df

def vol_capped_indice_rebalancing(weight_data=None, target_weights = None, vol_cap = None, volatility_window = 252, vol_cap_inception_date = None, initial_value = 100.):
    max_size_constituent = max(target_weights.iteritems(), key=operator.itemgetter(1))[0]
    assert vol_cap is not None
    weight_data['indice_returns'] = weight_data['indice'].pct_change()
    weight_data['rolling_vol_indice'] = weight_data['indice_returns'].rolling(volatility_window).apply(past_volatility)
    is_past_volatility_not_available_at_start =  np.isnan(weight_data.loc[vol_cap_inception_date,'rolling_vol_indice'])
    assert not is_past_volatility_not_available_at_start
    print(f'date range before filtering {min(weight_data.index)} {max(weight_data.index)}')
    weight_data = weight_data.loc[weight_data.index >= vol_cap_inception_date, :]
    print(f'date range after filtering {min(weight_data.index)} {max(weight_data.index)}')
    assert vol_cap_inception_date in weight_data.index
    volatility_factor = None
    target_vol_values_list = []
    for date_index, row in weight_data.iterrows():
        if date_index == vol_cap_inception_date:
            assert row['is_rebalancing']
            volatility_factor = vol_cap / weight_data.loc[vol_cap_inception_date,'rolling_vol_indice']
            previous_value = initial_value
            target_vol_values_list.append({'Date': vol_cap_inception_date, 'indice': initial_value, 'volatility_factor':np.nan})
            continue
        current_return = weight_data.loc[date_index, 'indice_returns']
        value = previous_value * (1 + current_return * volatility_factor)
        current_values = {'Date' : date_index, 'indice': value, 'volatility_factor':volatility_factor}
        target_vol_values_list.append(current_values)
        # we readjust the volatility factor
        if row['is_rebalancing']:
            volatility_factor = vol_cap / weight_data.loc[date_index,'rolling_vol_indice']
        previous_value = value

    target_vol_values_df = pd.DataFrame(target_vol_values_list)
    target_vol_values_df.index = pd.to_datetime(target_vol_values_df['Date'])
    target_vol_values_df.drop('Date', axis=1, inplace=True)
    return target_vol_values_df

def indice_rebalancing(price_data= None, inception_date=None, target_weights=None, initial_value= 100., rebalancing_method = None , early_rebalancing = False):
    if target_weights is None:
        target_weights = {}
    constituents = target_weights.keys()
    assert len([constituent for constituent in constituents if constituent in price_data.columns]) == len(constituents)
    total_values = sum(target_weights.values())
    assert total_values <= 1.001
    cash_value = 1. - total_values
    target_weights['cash'] = cash_value
    price_data['cash'] = 1.

    if inception_date is None:
        inception_date = min(price_data.index)
    print(f'backtesting with {rebalancing_method} method rebalancing since {inception_date} with early rebalancing {early_rebalancing}')
    print(f'date range before filtering {min(price_data.index)} {max(price_data.index)}')
    price_data = price_data.loc[price_data.index >= inception_date, :]
    print(f'date range after filtering {min(price_data.index)} {max(price_data.index)}')
    assert inception_date in price_data.index
    date_utility.add_rebalancing_datepart(price_data, 'Date', rebalancing_method = rebalancing_method)
    assert price_data.shape[0] > 0
    initial_weights = target_weights.copy()
    initial_weights.update({
        'Date' : inception_date,
        'indice': 1.
    })
    weights_list = []
    weights_list.append(initial_weights)
    previous_weights = None
    previous_prices = None
    for date_index, row in price_data.iterrows():
        if date_index == inception_date :
            previous_weights = target_weights.copy()
            previous_prices = price_data.loc[inception_date].to_dict()
            previous_value = sum(previous_weights.values())
            continue
        current_weights = {}
        current_prices = price_data.loc[date_index].to_dict()
        must_rebalance = row['is_rebalancing']
        if early_rebalancing:
            threshold_reached = False
            for constituent in constituents:
                if constituent != 'cash':
                    value_to_check = previous_weights[constituent] * current_prices[constituent]/previous_prices[constituent]
                    if value_to_check > target_weights[constituent] :
                        threshold_reached = True
            must_rebalance = must_rebalance or threshold_reached
        for constituent in constituents:
            if must_rebalance :
                #### rebalancing to match the target : the actual previous weight is replaced by the total value equally sep
                current_weights[constituent] = previous_value * target_weights[constituent] * current_prices[constituent]/previous_prices[constituent]
            else:
                ##### drifting
                current_weights[constituent] = previous_weights[constituent] * current_prices[constituent]/previous_prices[constituent]


        current_value = sum(current_weights.values())
        current_weights.update({'Date' : date_index, 'indice': current_value})
        weights_list.append(current_weights)

        previous_weights = current_weights.copy()
        previous_prices = current_prices.copy()
        previous_value = current_value


    weights_df = pd.DataFrame(weights_list)
    weights_df.index = pd.to_datetime(weights_df['Date'])
    date_utility.add_rebalancing_datepart(weights_df, 'Date', rebalancing_method = rebalancing_method)

    for me_constituent in constituents:
        weights_df[me_constituent] = weights_df[me_constituent] / weights_df['indice']

    weights_df['indice'] = weights_df['indice']*initial_value
    return weights_df


def indice_rebalancing_kpi(weight_data= None, starting_date=None, ending_date=None):
    indice_track = weight_data['indice']
    indice_track=indice_track.dropna()
    if starting_date is None:
        starting_date = min(indice_track.index)
    if ending_date is None:
        ending_date = max(indice_track.index)
    starting_value = indice_track.loc[starting_date]
    ending_value = indice_track.loc[ending_date]

    days_lapse = (ending_date - starting_date).days

    vol = np.nan
    annualized_return = np.nan
    dd = np.nan

    try:
        annualized_return = (ending_value/starting_value)**(365/(days_lapse))-1
        vol = np.sqrt(252)*np.std(indice_track.loc[starting_date:ending_date].pct_change().fillna(0.).values)
        annualized_return = annualized_return * 100
        vol = vol*100
        dd = max(metrics.drawdown(indice_track.loc[starting_date:ending_date]))*100
    except Exception as e:
        print(f'Trouble computing kpis {e}')

    result_df = pd.DataFrame({
        'volatility':[vol],
        'drawdown':[dd],
        'annualized_return':[annualized_return]
    })
    return result_df


def join_forex_data(weight_data = None, rates_data = None):
    assert min(weight_data.index) in rates_data.index
    assert max(weight_data.index) in rates_data.index
    weight_data = pd.merge(weight_data, rates_data, how = 'left', left_index= True, right_index= True)
    weigth_data = weight_data.rename(columns={'VM-EUR-USD' : 'EUR-USD'})
    return weigth_data[['indice' , 'EUR-USD']].copy()



def to_euro(weight_data = None, rates_data = None):
    data = join_forex_data(weight_data = weight_data, rates_data = rates_data)
    data['indice_usd'] = data['indice']
    data['indice_eur'] = data['indice_usd']/data['EUR-USD']
    data['indice'] = data['indice_eur']
    return data

def to_hedged_euro(weight_data = None, rates_data = None):
    data = join_forex_data(weight_data = weight_data, rates_data = rates_data)
    data['indice_usd'] = data['indice']
    data['indice_eur'] = data['indice_usd']/data['EUR-USD']
    data['indice'] = data['indice_eur']
    return data







