# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from functools import wraps
import re
import pandas as pd
import utils
import txt_related
import xyq_draw


from pages import (
    overview,
    pricePerformance,
)

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css',
                        dbc.themes.BOOTSTRAP]
app = dash.Dash(
    __name__, meta_tags=[{"name": "viewport", "content": "width=device-width"}],
    external_stylesheets=external_stylesheets
)
server = app.server

app.config.suppress_callback_exceptions = True
# Describe the layout/ UI of the app
app.layout = html.Div(
    [dcc.Location(id="url", refresh=False), html.Div(id="page-content")]
)

# Update page
@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def display_page(pathname):
    if pathname == "/dash-financial-report/price-performance":
        return pricePerformance.create_layout(app)

        return (
            overview.create_layout(app),
            pricePerformance.create_layout(app),
        )
    else:
        return overview.create_layout(app)

@app.callback(Output('output-upload-info', 'children'),
              [Input('upload-data', 'contents')],
              [State('upload-data', 'filename'),
               State('upload-data', 'last_modified')])
def update_output(list_of_contents, list_of_names, list_of_dates):
    if list_of_contents is not None:
        children = [
            utils.parse_contents(c, n, d) for c, n, d in
            zip(list_of_contents, list_of_names, list_of_dates)
        ]
        return children

#---------显示章节---------
def dash_kwarg(inputs):
    def accept_func(func):
        @wraps(func)
        def wrapper(*args):
            input_names = [item.component_id for item in inputs]
            kwargs_dict = dict(zip(input_names, args))
            return func(**kwargs_dict)
        return wrapper
    return accept_func
length = txt_related.returnLength()
outputs = [Output(f"collapse-{i}", "is_open") for i in range(1, length)]
inputs = [Input(f"group-{i}-toggle", "n_clicks") for i in range(1, length)]
states = [State(f"collapse-{i}", "is_open") for i in range(1, length)]
@app.callback(outputs, inputs, states)
@dash_kwarg(inputs + states)
def generate_graph(**kwargs):
    ctx = dash.callback_context
    if not ctx.triggered:
        return ""
    else:
        button_id = ctx.triggered[0]["prop_id"].split(".")[0]
    number = re.sub("\D", "", button_id)
    collapse = 'collapse-' + str(number)
    ans = []
    i = 0
    for arg in kwargs:
        if i < length - 1:
            if arg == button_id and kwargs[button_id]:
                ans.append(not kwargs[collapse])
            else:
                ans.append(False)
        i = i + 1
    return ans

@app.callback(
    [Output('wordcloud_figure', 'figure'),
     Output("frequency_figure", "figure"),]
    ,
    [Input('crossfilter-chapter', 'value'),
     Input('crossfilter-character', 'value')]
)
def update_x_timeseries(chapter, character):
    if(chapter == '-' or character == '-'):
        return xyq_draw.plotly_wordcloud(1)
    else:
        df = pd.read_csv('df_theme.csv')
    data = df[(df['chapter'] == chapter) & (df['character'] == character)]
    text = ""
    for index, row in data.iterrows():
        text = text + row['sentence']
#    print(text)
    return xyq_draw.plotly_wordcloud(text)

@app.callback(
    dash.dependencies.Output('sentiment-analysis', 'figure'),
    [dash.dependencies.Input('crossfilter-sentiment-character', 'value')]
)
def update_x_timeseries(column):
    df = pd.read_csv('df_sentiment.csv')
    dff = df[df['character'] == column]
    return xyq_draw.create_time_series(dff, column)

if __name__ == "__main__":
    app.run_server(debug=True, port=8059)
