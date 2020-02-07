from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html

from app import app
from apps import app1, app2, soccer, report_smr


app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])


@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/apps/app1':
         return app1.layout
    elif pathname == '/apps/app2':
         return app2.tester
    elif pathname == '/apps/soccer':
         return soccer.layout_soccer
    elif pathname == '/apps/report':
         return report_smr.layout
    else:
        return '404'

if __name__ == '__main__':
    app.run_server(debug=True)