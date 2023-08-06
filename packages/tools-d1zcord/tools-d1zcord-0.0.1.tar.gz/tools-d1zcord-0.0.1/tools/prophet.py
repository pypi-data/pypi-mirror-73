#! python3
# -*- coding: utf-8 -*-

from datetime import datetime
from multiprocessing import Pool

from tqdm import tqdm
import pandas as pd
from fbprophet import Prophet

from tools.general import suppress_stdout_stderr


def fit_predict_model(df, interval_width=0.99, changepoint_range=0.8, verbose=False, **kwargs):
    m = Prophet(seasonality_mode='multiplicative', interval_width=interval_width,
                changepoint_range=changepoint_range, *kwargs)
    if verbose:
        m = m.fit(df)
    else:
        with suppress_stdout_stderr():
            m = m.fit(df)
    forecast = m.predict(df)
    forecast['fact'] = df['y'].reset_index(drop=True)
    return forecast


def detect_anomalies(forecast):
    forecast['anomaly'] = 0
    forecast.loc[forecast['fact'] > forecast['yhat_upper'], 'anomaly'] = 1
    forecast.loc[forecast['fact'] < forecast['yhat_lower'], 'anomaly'] = -1

    # anomaly importances
    forecast['importance'] = 0
    forecast.loc[forecast['anomaly'] == 1, 'importance'] = \
        (forecast['fact'] - forecast['yhat_upper']) / forecast['fact']
    forecast.loc[forecast['anomaly'] == -1, 'importance'] = \
        (forecast['yhat_lower'] - forecast['fact']) / forecast['fact']

    return forecast


def fit_detect(df, address):
    df = df.reset_index()
    df.columns = ['ds', 'y']
    forecast = fit_predict_model(df)
    forecast = forecast[['ds', 'trend', 'yhat', 'yhat_lower', 'yhat_upper', 'fact']]
    forecast = detect_anomalies(forecast)
    forecast['address'] = address
    forecast.set_index(['address', 'ds'], inplace=True)
    return forecast


def apply_unpacked(x):
    return fit_detect(*x)


def fit_value(df, value, value_name):
    total_frames = sum(1 for address, address_data in df.groupby(level='address') if address_data.dropna().shape[0] > 2)
    frames = ((address_data.droplevel(level='address'), address) for address, address_data in
              df.groupby(level='address') if address_data.dropna().shape[0] > 2)
    with Pool(7) as p:
        anomalies = p.imap(apply_unpacked, frames)
        anomalies = tqdm(anomalies, total=total_frames,
                         desc=f'{value:<15} {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
        anomalies = pd.concat(anomalies)
    anomalies = pd.concat([anomalies], keys=[value], names=[value_name], axis=1)
    return anomalies
