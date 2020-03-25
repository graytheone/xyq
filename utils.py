import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import base64
import pandas as pd
import io

from dash.dependencies import Input, Output, State
global FILE
FILE=''
#-----------------上传文件---------------
UPLOAD = dcc.Upload(
            id='upload-data',
            children=html.Div([
                '将文件拖拽至此',
                html.A(' 或 选择文件')
            ], style={'color': '#98151b'}),
            # Allow multiple files to be uploaded
            multiple=True
        )


def Header(app):
    return html.Div([get_header(app), html.Br([]), get_menu()])


def get_header(app):
    header = html.Div(
        [
            html.Div(
                [

                    html.Img(
                        src=app.get_asset_url("dash-financial-logo.png"),
                        className="logo",
                    ),
                    html.Button((
                        html.Div(UPLOAD)
                    ), id="learn-more-button"),
                    html.Div("——————————", id="output-upload-info"),
                ],
                className="row",
            ),
            html.Div(
                [
                    html.Div(
                        [html.H5("文本可视化系统")],
                        className="seven columns main-title",
                    ),
                    html.Div(
                        [
                            dcc.Link(
                                "Full View",
                                href="/dash-financial-report/full-view",
                                className="full-view-link",
                            )
                        ],
                        className="five columns",
                    ),
                ],
                className="twelve columns",
                style={"padding-left": "0"},
            ),
        ],
        className="row",
    )

    return header


def get_menu():
    menu = html.Div(
        [
            dcc.Link(
                "Overview",
                href="/dash-financial-report/overview",
                className="tab first",
            ),
            dcc.Link(
                "Book Chapter",
                href="/dash-financial-report/price-performance",
                className="tab",
            )
        ],
        className="row all-tabs",
    )
    return menu


def make_my_table(df):
    """ Return a dash definition of an HTML table for a Pandas dataframe """
    table = []
    column = df.columns.values.tolist()
    html_row = [html.Td(' ')]
    for i in range(len(column)):
        html_row.append(html.Td([column[i]]))
    table.append(html.Tr(html_row))
    j = 0
    for index, row in df.iterrows():
        html_row = [column[j]]
        j = j + 1
        for i in range(len(row)):
            html_row.append(html.Td([row[i]]))
        table.append(html.Tr(html_row))
    return table

def make_dash_table(df):
    table = []
    for index, row in df.iterrows():
        html_row = []
        for i in range(len(row)):
            html_row.append(html.Td([row[i]]))
        table.append(html.Tr(html_row))
    return table
#------------------上传文件--------------------
def parse_contents(contents, filename, date):
    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)

    try:
        if 'csv' in filename:
            # Assume that the user uploaded a CSV file
            df = pd.read_csv(
                io.StringIO(decoded.decode('utf-8')))
        elif 'xls' in filename:
            # Assume that the user uploaded an excel file
            df = pd.read_excel(io.BytesIO(decoded))
        elif 'txt' in filename:
            txt = decoded.decode('utf-8')
        else:
            return html.Div([
                dbc.Alert("仅支持.txt格式的文件", color="warning")
            ])
    except Exception as e:
        print(e)
        return html.Div([
            '仅支持.txt格式的文件',
            dbc.Alert("仅支持.txt格式的文件", color="warning")
        ])
    with open(filename,'a') as file_handle:   # .txt可以不自己新建,代码会自动新建
        file_handle.write(txt)     # 写入
        file_handle.write('\n')
        global FILE
        FILE = filename
    return html.Div([
        dbc.Alert("上传成功", color="primary")
    ])

