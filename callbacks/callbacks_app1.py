from dash.dependencies import Input, Output

from app import app

@app.callback(
    Output(component_id='app-1-display-value', component_property='children'),
    [Input(component_id='app-1-dropdown', component_property='value')])
def display_value(value):
    return 'You have selected "{}"'.format(value)