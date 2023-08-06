from napoleontoolbox.utility import date_utility
import pandas as pd
import numpy as np
from napoleontoolbox.utility import metrics
import operator
from datetime import timedelta, date


def distribute_weights_risk(historic_volatilities, capped_weights, risk_budget_allocations, target_vol):
    capped_weights = capped_weights.copy()
    allocated_compo = {}
    while(len(capped_weights) > 0):
        #### we compute the allocation for the biggest component
        biggest_alloc_constituent = max(capped_weights, key=capped_weights.get)
        biggest_alloc_weight = capped_weights[biggest_alloc_constituent]
        biggest_alloc_risk_budget = risk_budget_allocations[biggest_alloc_constituent]
        histo_vol_biggest_alloc_constituent = historic_volatilities[f'vol_histo_{biggest_alloc_constituent}']
        biggest_alloc_final_weight = min(biggest_alloc_weight ,(target_vol * biggest_alloc_risk_budget)/ histo_vol_biggest_alloc_constituent)
        #target_vol = target_vol - target_vol * biggest_alloc_risk_budget
        target_vol = target_vol - biggest_alloc_final_weight*histo_vol_biggest_alloc_constituent
        capped_weights.pop(biggest_alloc_constituent, None)
        allocated_compo[biggest_alloc_constituent] = biggest_alloc_final_weight

    cash_value = 1-sum(allocated_compo.values())
    allocated_compo['cash'] = cash_value
    return allocated_compo


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

def drift_weight(previous_weights, current_returns):
    drifted_weights = previous_weights.copy()
    for key, value in previous_weights.items():
        if key == 'cash':
            drifted_weights[key] = previous_weights[key]
        else:
            drifted_weights[key] = previous_weights[key] * (1 + current_returns[f'returns_{key}'])
    return drifted_weights

def compound_weight(previous_weights,current_returns):
    compounded_return = 0.
    for key, value in previous_weights.items():
        if key != 'cash':
            compounded_return = compounded_return +  previous_weights[key]*current_returns[f'returns_{key}']
    return compounded_return

def global_drift_weight(previous_weights,current_returns):
    global_drift_weight = 0.
    for key, value in previous_weights.items():
        if key != 'cash':
            global_drift_weight = global_drift_weight +  previous_weights[key]*(1+current_returns[f'returns_{key}'])
        else:
            global_drift_weight = global_drift_weight +  previous_weights[key]
    return global_drift_weight

def vol_saturation_indice_rebalancing(price_data= None, inception_date=None, risk_budget_allocations = None, capped_weights=None, target_vol = None, initial_value= 100., rebalancing_method = None, volatility_window = 252, early_rebalancing = False, last = True):
    ### we must be able to assess the historical volatility on the beginning day
    assert inception_date >= min(price_data.index) + timedelta(days=volatility_window)
    assert risk_budget_allocations is not None
    assert capped_weights is not None
    assert target_vol is not None
    capped_weights = drop_cap_weight_to_key(capped_weights.copy())
    risk_budget_allocations = drop_budget_risk_to_key(risk_budget_allocations.copy())

    constituents = capped_weights.keys()
    print(constituents)
    print(price_data.columns)
    assert len([constituent for constituent in constituents if constituent in price_data.columns]) == len(constituents)
    #############
    #############
    #############
    ### computing volatility estimation for all our sets
    #############
    #############
    #############
    vol_histo_underlyings = []
    returns_underlyings = []
    for me_constituent in constituents:
        return_constituent = f'returns_{me_constituent}'
        price_data[return_constituent] = price_data[me_constituent].pct_change()
        vol_histo_constituent =  f'vol_histo_{me_constituent}'
        vol_histo_underlyings.append(vol_histo_constituent)
        price_data[vol_histo_constituent] = price_data[return_constituent].rolling(volatility_window).apply(past_volatility)
        returns_underlyings.append(return_constituent)
    date_utility.add_rebalancing_datepart(price_data, 'Date', rebalancing_method = rebalancing_method, last = last)

    print(f'backtesting with {rebalancing_method} method rebalancing since {inception_date} with early rebalancing {early_rebalancing}')

    starting_indice = price_data.index.get_loc(inception_date)
    previous_opened_date = price_data.index[starting_indice - 1]
    previous_histo_volatilities = price_data.loc[previous_opened_date, vol_histo_underlyings].to_dict()

    print(f'date range before filtering {min(price_data.index)} {max(price_data.index)}')
    price_data = price_data.loc[price_data.index >= inception_date, :]
    print(f'date range after filtering {min(price_data.index)} {max(price_data.index)}')

    assert inception_date in price_data.index
    assert price_data.loc[inception_date,'is_rebalancing']

    assert price_data.shape[0] > 0

    print(f'beginning regbalancing at {inception_date}')

    weights_list = []

    current_weights = {}

    previous_value = None
    for date_index, row in price_data.iterrows():
        must_rebalance = row['is_rebalancing']
        current_returns = price_data.loc[date_index, returns_underlyings].to_dict()
        if must_rebalance:
            #### rebalancing to match the target : the actual previous weight is replaced by the total value equally sep
            current_weights = distribute_weights_risk(previous_histo_volatilities, capped_weights,
                                                      risk_budget_allocations, target_vol)
            if previous_value is None:
                value = initial_value
            else:
                value = previous_value * (global_drift_weight(previous_weights, current_returns) / sum(previous_weights.values()))
        else :
            value = previous_value * (global_drift_weight(previous_weights,current_returns)/sum(previous_weights.values()))
            current_weights = drift_weight(previous_weights,current_returns)

        previous_histo_volatilities = price_data.loc[date_index, vol_histo_underlyings].to_dict()

        previous_value = value
        previous_weights = current_weights.copy()
        iteration = current_weights.copy()
        iteration.update({'Date' : date_index, 'indice' : value})
        weights_list.append(iteration)

    weights_df = pd.DataFrame(weights_list)
    weights_df.index = pd.to_datetime(weights_df['Date'])
    date_utility.add_rebalancing_datepart(weights_df, 'Date', rebalancing_method = rebalancing_method, last = last)

    return weights_df


def append_weight_to_key(current_weights):
    translated_weights = {}
    for key, val in current_weights.items():
        translated_weights[f'weight_{key}'] = val
    return translated_weights


def drop_cap_weight_to_key(current_weights):
    translated_weights = {}
    for key, val in current_weights.items():
        translated_weights[key.replace('weight_cap_', '')] = val
    return translated_weights

def drop_budget_risk_to_key(current_weights):
    translated_weights = {}
    for key, val in current_weights.items():
        translated_weights[key.replace('budget_risk_', '')] = val
    return translated_weights

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








