import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import plotly.graph_objs as go

from utils import Header, make_dash_table, make_my_table
import xyq_nlp
import xyq_tools
import drawChord
import txt_related

import pandas as pd
import pathlib
import wikipedia
import numpy as np
import csv
from wordcloud import WordCloud, STOPWORDS

# get relative data folder
PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("../data").resolve()

chapter = txt_related.returnChapter()

#df_fund_facts = pd.read_csv(DATA_PATH.joinpath("df_fund_facts.csv"))
#df_price_perf = pd.read_csv(DATA_PATH.joinpath("df_price_perf.csv"))


HEATMAP = [
    html.Div([
        dcc.Dropdown(
            multi=True,
            id='isv_select'
        ),
        dcc.Graph(id='heatmap_output'),]
)]

def create_layout(app):
    text = xyq_nlp.getCleanText()
    if len(text) < 1:
        return {}, {}, {}
    word_cloud = WordCloud(stopwords=set(STOPWORDS), max_words=100, max_font_size=90)
    word_cloud.generate(text)

    # -------------热力图-------------
    value = xyq_tools.generateTag()
    df = xyq_tools.getEntity()
    dff = df.loc[value, :]
    scaled_size = 200 + 150 + 50 * len(value)
    #        for row in dff.iterrows():
    z = dff.values.T.tolist()
    y = dff.columns.tolist()
    x = dff.index.T.tolist()
    annotations = []
    for n, row in enumerate(z):
        for m, val in enumerate(row):
            annotations.append(go.layout.Annotation(text=str(z[n][m]), x=x[m], y=y[n],
                                             xref='x1', yref='y1', showarrow=False))
    heatmap_figure = {
        'data': [{
            'z': dff.values.T.tolist(),
            'y': dff.columns.tolist(),
            'x': dff.index.tolist(),
            'ygap': 2,
            'reversescale': 'true',
            'colorscale': [[0, "#caf3ff"], [1, "#2c82ff"]],
            'type': 'heatmap',
        }],
        'layout': {
            'height': 700,
            'width': scaled_size,
            'xaxis': {'side': 'top'},
            'annotations': annotations,
            'margin': {
                'l': 100,
                'r': 100,
                'b': 50,
                't': 20,
            }
        }
    }
    #-------------人物情感分析-------------
    df = pd.read_csv('data\df_sentiment.csv')
    cha_df = pd.read_csv('data\df_character.csv')
    character = list(cha_df)
   # print(dff_s['chapter'])

    arr = []
    with open('relevance.csv', 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        lows = [low for low in reader]
        col = [lows[0][j] for j in range(10)]

        for i in range(1, 11):
            arr.append([lows[i][j] for j in range(10)])

    matrix = np.array(arr, dtype=int)
    M = pd.DataFrame(matrix, columns=col)
    return html.Div(
        [
            html.Div([Header(app)]),
            # page 1
            html.Div(
                [
                    # Row 3
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.H5(txt_related.returnTitle()),
                                    html.Br([]),
                                    html.P(
                                        "xyq",
#                                        wikipedia.summary("Alice's Adventures in Wonderland", sentences=5),
                                        style={"color": "#ffffff", 'width':'100%'},
                                        className="row",
                                    ),
                                ],
                                className="product",
                            )
                        ],
                        className="row",
                    ),
                    # Row 4
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.H6(
                                        ["Word Frequency"], className="subtitle padded"
                                    ),
                                    dcc.Dropdown(
                                        id='crossfilter-chapter',
                                        options=[{'label': chapter[i], 'value': i+1} for i in range(len(chapter))],
                                        value='-'
                                    ),
                                    dcc.Loading(
                                        id="loading-frequencies",
                                        children=[dcc.Graph(id="frequency_figure",
                                                            #figure=frequency_figure_data
                                                            )],
                                        type="default",
                                    )
                                ],
                                className="six columns",
                            ),
                            html.Div(
                                [
                                    html.H6(
                                        "WordCloud",
                                        className="subtitle padded",
                                    ),
                                    dbc.Alert(
                                        "Not enough data to render these plots, please adjust the filters",
                                        id="no-data-alert",
                                        color="warning",
                                        style={"display": "none"},
                                    ),
                                    dcc.Dropdown(
                                        id='crossfilter-character',
                                        options=[{'label': i, 'value': i} for i in character],
                                        value='-'
                                    ),
                                    dcc.Loading(
                                        id="loading-wordcloud",
                                        children=[
                                            dcc.Graph(
                                                id="wordcloud_figure",
                                                #figure=wordcloud_figure_data
                                            )
                                        ],
                                        type="default",
                                    )
                                ],
                                className="six columns",
                            ),
                        ],
                        className="row",
                        style={"margin-bottom": "35px"},
                    ),
                    # Row 5
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.H6(
                                        "Heatmap",
                                        className="subtitle padded",
                                    ),
                                    dcc.Graph(id='heatmap_output', figure=heatmap_figure)
                                ],
                                className="row",
                            ),

                        ],
                        className="row ",
                    ),
                    # Row 6
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.H6(
                                        "character relevance",
                                        className="subtitle padded",
                                    ),
                                    html.Table(make_my_table(M)),
                                ],
                                className="six columns",
                            ),
                            html.Div(
                                [
                                    html.H6(
                                        ["Character Relationship"], className="subtitle padded"
                                    ),
                                    dcc.Graph(id='chord-diagram', figure=drawChord.make_filled_chord(M))
                                ],
                                className="six columns",
                            ),
                        ],
                        className="row"
                    ),
                    #Row 7
                    html.Div(
                        [
                            html.H6(
                                ["Sentiment Analysis"], className="subtitle padded", style={'width':'100%'}
                            ),
                            html.P(
                                ["Select the name of the character:"], style={'paddingTop':'13px', 'margin':'0px', 'marginRight':'10px'}
                            ),
                            dcc.Dropdown(
                                id='crossfilter-sentiment-character',
                                options=[{'label': i, 'value': i} for i in character],
                                value='Alice',
                                style={'width':'100px'}
                            ),
                            dcc.Graph(id='sentiment-analysis',
                                      #figure=sentiment_figure
                                      )
                        ],
                        className="row"
                    )

                ],
                className="sub_page",
            ),
        ],
        className="page",
    )
