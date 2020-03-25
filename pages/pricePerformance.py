import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import plotly.graph_objs as go
from utils import Header, make_dash_table
import pandas as pd
import pathlib
import txt_related

chapter = txt_related.returnChapter()
content = txt_related.returnContent()

txt = []
for i in range(len(chapter)):
    txt.append(content[i].split("\n\n") )


def make_item(i):
    # we use this function to make the example items to avoid code duplication
#    txt = content[i].split("\n\n")
    #print(txt)
    return dbc.Card(
        [
            html.Div(
                html.H2(
                    dbc.Button(
                        f"CHAPTER #{i}",
                        color="link",
                        id=f"group-{i}-toggle",
                        style={
                            'border':'none',
                            'box-shadow':'none'
                        }
                    ),
                className="subtitle padded"
                ),
                #className="row",
                style={'width':'100%'}
            ),
            dbc.Collapse(
                dbc.CardBody([
                    html.P(f"CHAPTER {i} {txt[i][0]}", style={'color':'red', 'font-size':'18px'}),
                    html.Div([
                        html.P(txt[i][j]) for j in range(1, len(txt[i]))
                    ], style={'font-size':'16px'})
                ]),
                id=f"collapse-{i}",
                className="twelve columns",
            ),
        ]
    )


accordion = html.Div(
    [make_item(i) for i in range(1, len(chapter))], className="accordion", style={"width":"100%"}
)

def create_layout(app):
    return html.Div(
        [
            Header(app),
            # page 2
            html.Div(
                [
                    # Row 2
                    html.Div(
                        [
                            accordion
                        ],
                        className="row ",
                    ),

                    # Row 3
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.H6(
                                        [
                                            "Average annual returns--updated monthly as of 02/28/2018"
                                        ],
                                        className="subtitle padded",
                                    ),
                                    html.Div(
                                        [
                                            html.Table(
                                                make_dash_table(df_avg_returns),
                                                className="tiny-header",
                                            )
                                        ],
                                        style={"overflow-x": "auto"},
                                    ),
                                ],
                                className="twelve columns",
                            )
                        ],
                        className="row ",
                    ),

                ],
                className="sub_page",
            ),
        ],
        className="page",
    )
