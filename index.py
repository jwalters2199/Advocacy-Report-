import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import os

from app import app
from apps import base_explore, report
from static.constants import URL_SLUGS

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='hidden-nav', children='intro', style={'display' : 'none'}),
    html.Div(id='page-content')
], style={'font-family' : 'Avenir'})

@app.callback(
	Output('page-content', 'children'),
    Input('url', 'pathname'))
def display_page(pathname):
    if pathname == '/':
        return report.layout
    if pathname in URL_SLUGS.keys():
        return base_explore.layout
    return '404'

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run_server(debug=True, host='0.0.0.0', port=port)
    # app.run_server(debug=True, host='10.250.227.126')