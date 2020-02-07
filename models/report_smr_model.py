# pydata stack
import pandas as pd
from setting.conn_db_smtel import conn

import plotly.graph_objs as go

###########################
# Data Manipulation / Model
###########################

def fetch_data(q):
    result = pd.read_sql(
        sql=q,
        con=conn()
    )
    return result


def get_operator():
    '''Returns the list of operators that are stored in the database'''

    operator_query = (
        f'''
        SELECT DISTINCT vgrp_operator as operator
        FROM daily_sales_perdenom
        '''
    )
    operators = fetch_data(operator_query)
    operators = list(operators['operator'].sort_values(ascending=True))
    return operators


# def get_results(division='', season='', team=''):
#     '''Returns match results for the selected prompts'''

#     results_query = (
#         f'''
#         SELECT date, team, opponent, goals, goals_opp, result, points
#         FROM results
#         WHERE division='{division}'
#         AND season='{season}'
#         AND team='{team}'
#         ORDER BY date ASC
#         '''
#     )
#     match_results = fetch_data(results_query)
#     return match_results


# def draw_season_points_graph(results=''):
#     dates = results['date']
#     points = results['points'].cumsum()

#     figure = go.Figure(
#         data=[
#             go.Scatter(x=dates, y=points, mode='lines+markers')
#         ],
#         layout=go.Layout(
#             title='Points Accumulation',
#             showlegend=False
#         )
#     )

#     return figure