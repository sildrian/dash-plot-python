# standard library
import os

# dash libs
import dash
from dash.dependencies import Input, Output
import plotly.figure_factory as ff

import dash_core_components as dcc
import dash_html_components as html
from models.report_smr_model import get_operator, get_product_by_productcode, get_productcode_by_tsel, get_date_by_range, draw_product_points_graph, get_productcode_by_operator, get_product_by_operator

from datetime import datetime as dt
from dateutil.relativedelta import relativedelta

import pandas as pd
import numpy as np
import array as array 
from random import randint

import random
import string
import plotly.graph_objs as go

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
            dcc.Graph(
                style={'height': 700},
                id='product-graph'
            )
            # style={},

        ], className='six columns')
    ]),
])

# Update Season Point Graph
@app.callback(
    Output(component_id='product-graph', component_property='figure'),
    # Output(component_id='output-container-date-picker-range', component_property='children'),
    [
        Input(component_id='date-picker-range', component_property='start_date'),
        Input(component_id='date-picker-range', component_property='end_date'),
        Input(component_id='operator-selector', component_property='value')
    ]
)
def load_product_points_graph(start_date, end_date, operator):
    string_prefix = ''
    if start_date is not None:
        start_date = dt.strptime(start_date.split(' ')[0], '%Y-%m-%d')
        start_date_string = start_date.strftime('%Y-%m-%d')
        string_prefix = string_prefix + 'Start Date: ' + start_date_string + ' | '
        
    if end_date is not None:
        end_date = dt.strptime(end_date.split(' ')[0], '%Y-%m-%d')
        end_date_string = end_date.strftime('%Y-%m-%d')
        string_prefix = string_prefix + 'End Date: ' + end_date_string

    if operator is not None:
        # productcode = get_productcode_by_tsel(start_date, end_date)
        productcode = get_productcode_by_operator(start_date, end_date, operator)
        daterange = get_date_by_range(start_date, end_date)
        productcode_arr = pd.DataFrame(productcode).to_numpy()
        daterange_arr = pd.DataFrame(daterange).to_numpy()
        # daterange_arr_new = pd.DataFrame(daterange).values.tolist()

        new_daterange_arr = []
        temp_results = []
        results = []
        
        for i in range(len(daterange_arr)):
            new_daterange_arr.append(daterange_arr[i,0].strftime('%Y-%m-%d'))

        for kode_produk in productcode_arr:
            # results = get_product_by_tsel(start_date, end_date, kode_produk[0])
            results = get_product_by_productcode(start_date, end_date, kode_produk[0])
            resultsproduct_arr = pd.DataFrame(results).to_numpy()
            temp_results.append(resultsproduct_arr) 

        showresult = []
        all_results = []
        getresult = []

        # for i in range(len(temp_results)):
        #     for j in range(len(daterange_arr)):
        #         codeproduct = temp_results[i][0][0]
        #         try:
        #             # if daterange_arr[j] in temp_results[i]:
        #             showresult.append(temp_results[i][j][2])
        #             if temp_results[2][0][2] is not None:
        #                 showresult.append(temp_results[i][j][1])
        #                 # None
        #             # else:
        #             #     showresult.append(0)
        #         except:
        #             showresult.append(10)
                    # None
                # else:
                #     try:
                #         if daterange_arr[j] in temp_results[i]:
                #             None
                #     except:
                #         showresult.append(0)
                # try:
                #     if temp_results[0][1][2] is not None:
                #     # if temp_results[0][1][1] is not None:
                #         showresult.append(temp_results[i][j][1])
                # except:
                #     showresult.append(12)
                #     # None
                # else:
                #     try:
                #         # print(isinstance(temp_results[i][j][2], dt.date))
                #         if type(temp_results[i][j][2]) is datetime:
                #             showresult.append(13)
                #     except:
                #         None
                    
            # all_results.append(showresult)
            # showresult = []
            # codeproduct = ''
        
        # for datas in temp_results.index:
        #     print(datas)
        def checkDate(arrDateData,arrAllData):
            m=0 
            for k in range(len(daterange_arr)):
                try:
                    if arrDateData == daterange_arr[k,0]:
                        showresult.append(arrAllData)
                        # m = m + 1
                except:
                    showresult.append(0)           
            return showresult

        for i in range(len(temp_results)):
            for j in range(len(daterange_arr)):
                codeproduct = temp_results[i][0][0]
                getresult = map(temp_results[i][j][2], temp_results[i][j][1]) 
                # for datedata in daterange_arr:
                #     try:
                #         if temp_results[i][j][2] == datedata:
                #         # if temp_results[i][j][2] == daterange_arr[z,0]:
                #             showresult.append(temp_results[i][j][1])
                #     except:
                #         # showresult.append(10)
                #         break
                # try:
                #     if temp_results[i][j][2] == daterange_arr[j,0]:
                #         showresult.append(temp_results[i][j][1])
                # except:
                    # try:
                    #     if temp_results[i][j][2] is not None:
                    #         if temp_results[i][j][2] != daterange_arr[j,0]:
                    #             showresult.append(temp_results[i][j][1])
                    # except:
                    #     None
                    # showresult.append(0)

                # for z in range(len(daterange_arr)):
                #     finally:
                #         try:
                #             if temp_results[i][j][2] != daterange_arr[z,0]:
                #                 showresult.append(0)
                #             # None
                #         except:
                #             None

            all_results.append(getresult)
            showresult = []
            codeproduct = ''
        
        print(all_results)
           
        figure = []
        if len(results) > 0:
            figure = draw_product_points_graph(temp_results,daterange_arr,operator,new_daterange_arr)
        # else:
        #     figure = 
        string_prefix = figure

    return string_prefix
