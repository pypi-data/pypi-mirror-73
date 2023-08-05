import numpy as np
import pandas as pd
from datetime import datetime
from fbprophet import Prophet

from release_one.decomp import generic_yearly_decomp, generic_weekly_decomp


def gen_future(df, periods=30, freq='1D'):
    start_0 = df.iloc[-1, 0]
    future = pd.date_range(start=start_0, freq=freq, periods=periods) + pd.Timedelta(freq)
    future = pd.DataFrame(future)
    future.rename(columns={0: 'ds'}, inplace=True)
    return future


def forecast_far(sales_history,
                 yearly_decomp,
                 weekly_decomp,
                 forecast_length=90,
                 daily_lift_est=0,
                 output_format='dict'):

    # generate predictions
    predictions = pd.DataFrame(columns=['woy', 'dow', 'base', 'weekly', 'daily'])
    predictions['woy'] = np.repeat(range(1, 54), 7)  # 52.14 'week of year' -> 53
    predictions['dow'] = [0, 1, 2, 3, 4, 5, 6] * 53  # 7 'day of week' each week of year

    if type(sales_history) != pd.core.frame.DataFrame:  # no historical sales data
        predictions['base'] = daily_lift_est  # user input
        weekly = np.repeat(predictions.base.iloc[1] * 7 * generic_yearly_decomp, 7)
        weekly.index = range(0, 371)
        predictions['weekly'] = weekly
        weekly_decomp_rep = pd.concat([generic_weekly_decomp] * 53, ignore_index=True)
        predictions['daily'] = (predictions.weekly * (1 / 7) * weekly_decomp_rep)
        data = {'date': [pd.to_datetime(datetime.now()), pd.to_datetime(datetime.now())],
                'sales': [0, 0]}
        sales_history = pd.DataFrame(data=data)
        sales_history.ds = sales_history.ds.dt.date
    else:
        predictions['base'] = sales_history.y[-365:].mean()

    if len(yearly_decomp) <= 52:  # less than 1 year sales data, use generic yearly trends
        weekly = np.repeat(predictions.base[1] * 7 * generic_yearly_decomp, 7)
    else:  # more than 1 year sales data, use tank specific yearly trends
        weekly = np.repeat(predictions.base[1] * 7 * yearly_decomp, 7)

    weekly.index = range(0, 371)
    predictions['weekly'] = weekly
    weekly_decomp_rep = pd.concat([weekly_decomp] * 53, ignore_index=True)
    predictions['daily'] = (predictions.weekly * (1 / 7) * weekly_decomp_rep)

    # match predictions to future dataframe
    future = gen_future(sales_history, periods=forecast_length, freq='1D')
    future['dow'] = future.ds.dt.weekday
    future['woy'] = future.ds.dt.weekofyear
    output = pd.merge(future, predictions, left_on=['woy', 'dow'], right_on=['woy', 'dow'])
    output = output[['ds', 'daily']]
    output.rename(columns={'daily': 'yhat'}, inplace=True)

    # confidence interval
    output['lower'] = output['yhat'] - 2*output['yhat'].std()
    output['upper'] = output['yhat'] + 2*output['yhat'].std()

    # non-negative predictions
    for field in ["yhat", 'lower', 'upper']:
        output.loc[output[field] < 0, field] = 0

    # output format
    if output_format == 'df':
        return output
    else:
        return output.to_dict(orient='records')


def forecast_near(validated_tank_history,
                  forecast_freq='30min',
                  forecast_length=144,
                  output_format='dict'):

    # generate future ds
    future = gen_future(validated_tank_history,
                        periods=forecast_length,
                        freq=forecast_freq)

    # calculate model
    m = Prophet(changepoint_prior_scale=0.05,
                daily_seasonality=True,
                weekly_seasonality=True,
                yearly_seasonality=False)
    m.fit(validated_tank_history)
    forecast = m.predict(future)

    # format output
    output = forecast.loc[:, ['ds', 'yhat_lower', 'yhat_upper', 'yhat']]
    output.rename(columns={'yhat_lower': 'lower', 'yhat_upper': 'upper'}, inplace=True)

    # non-negative predictions
    for field in ["yhat", "lower", "upper"]:
        output.loc[output[field] < 0, field] = 0

    # desired output
    if output_format == 'df':
        return output
    else:
        return output.to_dict(orient='records')

