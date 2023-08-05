import numpy as np
import scipy
import pandas as pd
from scipy.stats import linregress

from napoleontoolbox.signal import signal_utility

from sklearn import preprocessing
from sklearn.preprocessing import StandardScaler
from functools import partial
from numpy.lib.stride_tricks import as_strided as stride
import pandas as pd
from scipy.optimize import Bounds, LinearConstraint, minimize
from napoleontoolbox.utility import metrics
import numpy as np
from napoleontoolbox.signal import signal_utility
from napoleontoolbox.connector import napoleon_connector
import json

from napoleontoolbox.parallel_run import signal_result_analyzer
from sklearn.metrics import accuracy_score
from functools import partial


class SimpleThresholdModel():

    def __init__(self, leading_correlation=5,  nb_selected=10, number_per_year=365):
        self.model = None
        self.seed = 0
        self.nb_selected = nb_selected
        self.number_per_year = number_per_year
        self.leading_correlation = leading_correlation


    def calibrate(self, X, y):
        return

    def fit(self, X_train, y_train, X_val, y_val):
        print(f'finding the {self.nb_selected} most correlated features with the output')

        X = X_train.copy().fillna(0.)
        y = y_train.copy().fillna(0.)

        output_correlations = []
        leading_output_correlations = []

        for daily_feat in X_train.columns:
            correlation_matrix = np.corrcoef(X[daily_feat], y)
            output_correlations.append(
                {
                    'feature': daily_feat,
                    'correlation': correlation_matrix[0][1]
                }
            )
            leading_correlation_matrix = np.corrcoef(X.iloc[-self.leading_correlation:, X.columns.get_loc(daily_feat)], y.iloc[-self.leading_correlation:])
            leading_output_correlations.append(
                {
                    'feature': daily_feat,
                    'correlation': leading_correlation_matrix[0][1]
                }
            )
        output_correlations_df = pd.DataFrame(output_correlations)
        output_correlations_df['abs_correlation'] = abs(output_correlations_df['correlation'])
        output_correlations_df = output_correlations_df.sort_values(by='abs_correlation', ascending=False)
        output_correlations_df['effect_sign']=np.sign(output_correlations_df['correlation'])
        output_correlations_df.index = output_correlations_df.feature

        leading_output_correlations_df = pd.DataFrame(leading_output_correlations)
        leading_output_correlations_df['abs_correlation'] = abs(leading_output_correlations_df['correlation'])
        leading_output_correlations_df = leading_output_correlations_df.sort_values(by='abs_correlation', ascending=False)
        leading_output_correlations_df['effect_sign'] = np.sign(leading_output_correlations_df['correlation'])
        leading_output_correlations_df.index = leading_output_correlations_df.feature



        selected_output_correlations_df = output_correlations_df.head(self.nb_selected)


        self.selected_features = list(selected_output_correlations_df.feature)

        selected_leading_output_correlations_df = leading_output_correlations_df[leading_output_correlations_df.feature.apply(lambda x: x in self.selected_features) ]

        self.leading_correlation_effects = selected_leading_output_correlations_df['correlation'].to_dict()

        self.correlation_effects = selected_output_correlations_df['correlation'].to_dict()
        selected_X = X[self.selected_features].copy()
        scaler = StandardScaler()
        scaler.fit(selected_X)
        transformed_selected_X = scaler.transform(selected_X)
        transformed_selected_X_df = pd.DataFrame(data = transformed_selected_X, columns = selected_X.columns, index = selected_X.index)

        past_values_dic = {}
        for feature_to_investigate in self.selected_features:

            x = transformed_selected_X_df[feature_to_investigate].values.copy()
            past_values_dic[feature_to_investigate] = x[:-self.leading_correlation]
        self.past_values_dic = past_values_dic
        self.scaler = scaler
        return

    def predict(self, X_test):
        X = X_test.copy()
        selected_X = X[self.selected_features].copy()
        transformed_selected_X = self.scaler.transform(selected_X)
        transformed_selected_X_df = pd.DataFrame(data = transformed_selected_X, columns = selected_X.columns, index = selected_X.index)
        for feature_to_investigate in self.selected_features:
            #print(feature_to_investigate)
            whole_correlation = self.correlation_effects[feature_to_investigate]
            leading_past_values = self.past_values_dic[feature_to_investigate]
            leading_correlations = self.leading_correlation_effects[feature_to_investigate]

            # long correlation way
            lag_signal_way = np.sign(whole_correlation)
            lead_signal_way = np.sign(leading_correlations)

            x = transformed_selected_X_df[feature_to_investigate].values.copy()
            lead_lag_ar =  x.mean()/leading_past_values.mean()

            lead_lag_correlation_coefficient = leading_correlations/whole_correlation

            # the two signals are in the same way
            if lead_signal_way == lag_signal_way:
                x = x*lag_signal_way
            else:
                x[:] =  0.

            transformed_selected_X_df[feature_to_investigate]=x
        return transformed_selected_X_df.mean(axis = 1)

    def get_features_importance(self, features_names):
        return
