import dash_core_components as dcc
import dash_html_components as html
from models.soccer_model import get_divisions


#########################
# Dashboard Layout / View
#########################

def onLoad_division_options():
    '''Actions to perform upon initial page load'''

    division_options = (
        [division
         for division in get_divisions()]
    )
    return division_options

tester = html.Div([
    html.H3('App 2'),
    dcc.Dropdown(
        id='app-2-dropdown',
        options=[
            {'label': '{}'.format(i), 'value': i} for i in 
            onLoad_division_options()
        ]
    ),
    html.Div(id='app-2-display-value'),
    dcc.Link('Go to App 1', href='/apps/app1')
])