import pandas as pd
import plotly.graph_objs as go
from plotly.subplots import make_subplots
from statsmodels.tsa.arima.model import ARIMA
from dash import Dash, dcc, html
from dash.dependencies import Input, Output

def load_data(file_path):
    data = pd.read_csv(file_path)
    data['Date'] = pd.to_datetime(data['Date'], format='%d.%m.%y')
    data = data.sort_values('Date')
    data.set_index('Date', inplace=True)
    return data

def create_forecast(ts, forecast_steps=15):
    model = ARIMA(ts, order=(p, d, q))
    model_fit = model.fit()
    
    last_date = ts.index[-1]
    forecast_index = pd.date_range(start=last_date + pd.Timedelta(days=1), periods=forecast_steps, freq='D')
    
    forecast = model_fit.forecast(steps=forecast_steps)
    
    return forecast, forecast_index

app = Dash(__name__)

file_path = 'file_path.csv' 
data = load_data(file_path)
ts_energy_met_mu = data['Energy Met (MU)']
ts_energy_met_mw = (ts_energy_met_mu * 1000) / 24

ts_energy_hydro = data['Hydro Gen (MU)']
ts_hydro = (ts_energy_hydro * 1000) / 24
ts_energy_wind = data['Wind Gen (MU)']
ts_wind = (ts_energy_wind * 1000) / 24
ts_energy_solar = data['Solar Gen (MU)*']
ts_solar = (ts_energy_solar * 1000) / 24

ts_day = data['Maximum Demand Met During the Day (MW) (From NLDC SCADA)']
ts_evening = data['Demand Met during Evening Peak hrs(MW) (at 20:00 hrs; from RLDCs)']

forecast_steps = 15
forecast_energy_met, forecast_energy_met_index = create_forecast(ts_energy_met_mw, forecast_steps)
forecast_day, forecast_day_index = create_forecast(ts_day, forecast_steps)
forecast_evening, forecast_evening_index = create_forecast(ts_evening, forecast_steps)
forecast_hydro, forecast_hydro_index = create_forecast(ts_hydro, forecast_steps)
forecast_wind, forecast_wind_index = create_forecast(ts_wind, forecast_steps)
forecast_solar, forecast_solar_index = create_forecast(ts_solar, forecast_steps)

fig_energy_met = make_subplots(rows=1, cols=1)
fig_energy_met.add_trace(go.Scatter(x=ts_energy_met_mw.index, y=ts_energy_met_mw, mode='lines', name='Original'))
fig_energy_met.add_trace(go.Scatter(x=forecast_energy_met_index, y=forecast_energy_met, mode='lines+markers', name='Forecast', line=dict(color='red')))
fig_energy_met.update_layout(
     title='Energy Met (MW)',
     xaxis_title='Date',
     yaxis_title='(MW)',
     hovermode='x unified'
)

fig_day = make_subplots(rows=1, cols=1)
fig_day.add_trace(go.Scatter(x=ts_day.index, y=ts_day, mode='lines', name='Original'))
fig_day.add_trace(go.Scatter(x=forecast_day_index, y=forecast_day, mode='lines+markers', name='Forecast', line=dict(color='red')))
fig_day.update_layout(
     title='Maximum Demand Met During the Day',
     xaxis_title='Date',
     yaxis_title='(MW)',
     hovermode='x unified'
)

fig_evening = make_subplots(rows=1, cols=1)
fig_evening.add_trace(go.Scatter(x=ts_evening.index, y=ts_evening, mode='lines', name='Original'))
fig_evening.add_trace(go.Scatter(x=forecast_evening_index, y=forecast_evening, mode='lines+markers', name='Forecast', line=dict(color='red')))
fig_evening.update_layout(
    title='Demand Met during Evening Peak hrs (20:00 hrs)',
    xaxis_title='Date',
    yaxis_title='(MW)',
    hovermode='x unified'
)
fig_hydro = make_subplots(rows=1, cols=1)
fig_hydro.add_trace(go.Scatter(x=ts_hydro.index, y=ts_hydro, mode='lines', name='Original'))
fig_hydro.add_trace(go.Scatter(x=forecast_hydro_index, y=forecast_hydro, mode='lines+markers', name='Forecast', line=dict(color='red')))
fig_hydro.update_layout(
    title='Hydro Generation',
    xaxis_title='Date',
    yaxis_title='(MW)',
    hovermode='x unified'
)
fig_wind = make_subplots(rows=1, cols=1)
fig_wind.add_trace(go.Scatter(x=ts_wind.index, y=ts_wind, mode='lines', name='Original'))
fig_wind.add_trace(go.Scatter(x=forecast_wind_index, y=forecast_wind, mode='lines+markers', name='Forecast', line=dict(color='red')))
fig_wind.update_layout(
    title='Wind Generation',
    xaxis_title='Date',
    yaxis_title='(MW)',
    hovermode='x unified'
)
fig_solar = make_subplots(rows=1, cols=1)
fig_solar.add_trace(go.Scatter(x=ts_solar.index, y=ts_solar, mode='lines', name='Original'))
fig_solar.add_trace(go.Scatter(x=forecast_solar_index, y=forecast_solar, mode='lines+markers', name='Forecast', line=dict(color='red')))
fig_solar.update_layout(
    title='Solar Generation',
    xaxis_title='Date',
    yaxis_title='(MW)',
    hovermode='x unified'
)

app.layout = html.Div(children=[
    html.Div([
        html.Div([
            html.H1(children='Grid India Demand Forecast Dashboard', style={'textAlign': 'center'})
        ], style={'width': '70%', 'display': 'inline-block'}),
    ], style={'display': 'flex', 'alignItems': 'center', 'justifyContent': 'center'}),
    dcc.Graph(id='forecast-graph-energy-met', figure=fig_energy_met),
    dcc.Graph(id='forecast-graph-day', figure=fig_day),
    dcc.Graph(id='forecast-graph-evening', figure=fig_evening),
    dcc.Graph(id='forecast-graph-hydro', figure=fig_hydro),
    dcc.Graph(id='forecast-graph-wind', figure=fig_wind),
    dcc.Graph(id='forecast-graph-solar', figure=fig_solar),
    dcc.Interval(
        id='interval-component',
        interval=60*1000*60*12, 
        n_intervals=0
    ),
])

@app.callback(
    [Output('forecast-graph-energy-met', 'figure'),
     Output('forecast-graph-day', 'figure'),
     Output('forecast-graph-evening', 'figure'),
     Output('forecast-graph-hydro', 'figure'),
     Output('forecast-graph-wind', 'figure'),
     Output('forecast-graph-solar', 'figure')],
    Input('interval-component', 'n_intervals')
)

def update_graph(n):
    data = load_data(file_path)
    ts_energy_met_mu = data['Energy Met (MU)']
    ts_energy_met_mw = (ts_energy_met_mu * 1000) / 24

    ts_energy_hydro = data['Hydro Gen (MU)']
    ts_hydro = (ts_energy_hydro * 1000) / 24
    ts_energy_wind = data['Wind Gen (MU)']
    ts_wind = (ts_energy_wind * 1000) / 24
    ts_energy_solar = data['Solar Gen (MU)*']
    ts_solar = (ts_energy_solar * 1000) / 24

    ts_day = data['Maximum Demand Met During the Day (MW) (From NLDC SCADA)']
    ts_evening = data['Demand Met during Evening Peak hrs(MW) (at 20:00 hrs; from RLDCs)']

    forecast_steps = 15
    forecast_energy_met, forecast_energy_met_index = create_forecast(ts_energy_met_mw, forecast_steps)
    forecast_day, forecast_day_index = create_forecast(ts_day, forecast_steps)
    forecast_evening, forecast_evening_index = create_forecast(ts_evening, forecast_steps)
    forecast_hydro, forecast_hydro_index = create_forecast(ts_hydro, forecast_steps)
    forecast_wind, forecast_wind_index = create_forecast(ts_wind, forecast_steps)
    forecast_solar, forecast_solar_index = create_forecast(ts_solar, forecast_steps)

    fig_energy_met = make_subplots(rows=1, cols=1)
    fig_energy_met.add_trace(go.Scatter(x=ts_energy_met_mw.index, y=ts_energy_met_mw, mode='lines', name='Original'))
    fig_energy_met.add_trace(go.Scatter(x=forecast_energy_met_index, y=forecast_energy_met, mode='lines+markers', name='Forecast', line=dict(color='red')))
    fig_energy_met.update_layout(
        title='Energy Met (MW)',
        xaxis_title='Date',
        yaxis_title='(MW)',
        hovermode='x unified'
    )

    fig_day = make_subplots(rows=1, cols=1)
    fig_day.add_trace(go.Scatter(x=ts_day.index, y=ts_day, mode='lines', name='Original'))
    fig_day.add_trace(go.Scatter(x=forecast_day_index, y=forecast_day, mode='lines+markers', name='Forecast', line=dict(color='red')))
    fig_day.update_layout(
        title='Maximum Demand Met During the Day',
        xaxis_title='Date',
        yaxis_title='(MW)',
        hovermode='x unified'
    )

    fig_evening = make_subplots(rows=1, cols=1)
    fig_evening.add_trace(go.Scatter(x=ts_evening.index, y=ts_evening, mode='lines', name='Original'))
    fig_evening.add_trace(go.Scatter(x=forecast_evening_index, y=forecast_evening, mode='lines+markers', name='Forecast', line=dict(color='red')))
    fig_evening.update_layout(
        title='Demand Met during Evening Peak hrs (20:00 hrs)',
        xaxis_title='Date',
        yaxis_title='(MW)',
        hovermode='x unified'
    )
    fig_hydro = make_subplots(rows=1, cols=1)
    fig_hydro.add_trace(go.Scatter(x=ts_hydro.index, y=ts_hydro, mode='lines', name='Original'))
    fig_hydro.add_trace(go.Scatter(x=forecast_hydro_index, y=forecast_hydro, mode='lines+markers', name='Forecast', line=dict(color='red')))
    fig_hydro.update_layout(
        title='Hydro Generation',
        xaxis_title='Date',
        yaxis_title='(MW)',
        hovermode='x unified'
    )
    fig_wind = make_subplots(rows=1, cols=1)
    fig_wind.add_trace(go.Scatter(x=ts_wind.index, y=ts_wind, mode='lines', name='Original'))
    fig_wind.add_trace(go.Scatter(x=forecast_wind_index, y=forecast_wind, mode='lines+markers', name='Forecast', line=dict(color='red')))
    fig_wind.update_layout(
        title='Wind Generation',
        xaxis_title='Date',
        yaxis_title='(MW)',
        hovermode='x unified'
    )
    fig_solar = make_subplots(rows=1, cols=1)
    fig_solar.add_trace(go.Scatter(x=ts_solar.index, y=ts_solar, mode='lines', name='Original'))
    fig_solar.add_trace(go.Scatter(x=forecast_solar_index, y=forecast_solar, mode='lines+markers', name='Forecast', line=dict(color='red')))
    fig_solar.update_layout(
        title='Solar Generation',
        xaxis_title='Date',
        yaxis_title='(MW)',
        hovermode='x unified'
    )
    
    return fig_energy_met, fig_day, fig_evening, fig_hydro, fig_wind, fig_solar

if __name__ == '__main__':
    app.run_server(debug=True, port=8061)  
