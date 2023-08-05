from napoleontoolbox.utility import date_utility
import pandas as pd
import numpy as np
from napoleontoolbox.utility import metrics

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

    annualized_return = (ending_value/starting_value)**(365/(days_lapse))-1
    vol = np.sqrt(252)*np.std(indice_track.loc[starting_date:ending_date].pct_change().fillna(0.).values)
    annualized_return = annualized_return * 100
    vol = vol*100
    dd = max(metrics.drawdown(indice_track.loc[starting_date:ending_date]))*100
    result_df = pd.DataFrame({
        'volatility':[vol],
        'drawdown':[dd],
        'annualized_return':[annualized_return]
    })
    return result_df


def indice_rebalancing(price_data= None, inception_date=None, target_weights=None, initial_value= 100., rebalancing_method = None):
    constituents = target_weights.keys()
    assert len([constituent for constituent in constituents if constituent in price_data.columns]) == len(constituents)
    assert sum(target_weights.values()) == 1.
    print(f'backtesting with {rebalancing_method} method rebalancing since {inception_date}')
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
        for constituent in constituents:
            if row['is_rebalancing']:
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
    weights_df.drop('Date', axis=1, inplace=True)

    for me_constituent in constituents:
        weights_df[me_constituent] = weights_df[me_constituent] / weights_df['indice']

    weights_df['indice'] = weights_df['indice']*initial_value
    return weights_df
