# standard library
import os

# dash libs
import dash
from dash.dependencies import Input, Output
import plotly.figure_factory as ff

import dash_core_components as dcc
import dash_html_components as html
from models.report_smr_model import get_operator

from datetime import datetime as dt
from dateutil.relativedelta import relativedelta

from app import app

#########################
# Dashboard Layout / View
#########################

time3month = dt.now() + relativedelta(months=-2)
dateNowEnd = dt.now() + relativedelta(days=+1)

def onLoad_operator_options():
    '''Actions to perform upon initial page load'''

    operator_options = (
        [operator
         for operator in get_operator()]
    )
    return operator_options

# Set up Dashboard and create layout
layout = html.Div([

    # Page Header
    html.Div([
        html.H1('Report show')
    ]),

    # Dropdown Grid
    html.Div([
        html.Div([
            #Select date
            html.Div([
                html.Div('Select Date', className='three columns'),
                html.Div(dcc.DatePickerRange(
                                id='date-picker-range',
                                min_date_allowed=time3month,
                                max_date_allowed=dateNowEnd,
                                start_date=dt.now(),
                                end_date_placeholder_text='Select a date!'
                            ),
                        className='nine columns')
            ]),

            # Select Operator Dropdown
            html.Div([
                html.Div('Select Operator', className='three columns'),
                html.Div(dcc.Dropdown(id='operator-selector',
                                    options=[
                                        {'label': '{}'.format(i), 'value': i} for i in 
                                        onLoad_operator_options()
                                    ]),
                        className='nine columns')
            ]),

        ], className='six columns'),

        # Empty
        html.Div(className='six columns'),
    ], className='twleve columns'),

    # Match Results Grid
    html.Div([
        #tester
        html.Div(id='output-container-date-picker-range'),

        # Season Summary Table and Graph
        html.Div([
            # graph
            dcc.Graph(id='season-graph')
            # style={},

        ], className='six columns')
    ]),
])

# Update Season Point Graph
@app.callback(
    # Output(component_id='season-graph', component_property='figure'),
    Output(component_id='output-container-date-picker-range', component_property='children'),
    [
        Input(component_id='date-picker-range', component_property='start_date'),
        Input(component_id='date-picker-range', component_property='end_date'),
        Input(component_id='operator-selector', component_property='value')
    ]
)
def load_season_points_graph(start_date, end_date, operator):
    if start_date is not None:
        start_date = dt.strptime(start_date.split(' ')[0], '%Y-%m-%d')
        string_prefix = string_prefix + 'Start Date: ' + start_date_string + ' | '
        
    if end_date is not None:
        end_date = dt.strptime(end_date.split(' ')[0], '%Y-%m-%d')
        string_prefix = string_prefix + 'End Date: ' + end_date_string

    return string_prefix

    # results = get_results(division, season, team)

    # figure = []
    # if len(results) > 0:
    #     figure = draw_season_points_graph(results)

    # return figure