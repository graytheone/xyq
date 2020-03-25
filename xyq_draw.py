from wordcloud import WordCloud, STOPWORDS
import xyq_nlp
import txt_related
import plotly.graph_objs as go
import pandas as pd
import numpy as np
import csv
import plotly.graph_objs as go
import xyq_tools

#--------------词云-------------------------
def wordcould():
    wordcloud_figure_data, frequency_figure_data, treemap_figure = plotly_wordcloud()
    return wordcloud_figure_data, frequency_figure_data

def plotly_wordcloud(flag):
    if(flag == 1):
        text = xyq_nlp.getCleanText()
    else:
        text = flag
    print(flag)
    if len(text) < 1:
        return {}, {}
    word_cloud = WordCloud(stopwords=set(STOPWORDS), max_words=100, max_font_size=90)
    word_cloud.generate(text)

    word_list = []
    freq_list = []
    fontsize_list = []
    position_list = []
    orientation_list = []
    color_list = []

    for (word, freq), fontsize, position, orientation, color in word_cloud.layout_:
        word_list.append(word)
        freq_list.append(freq)
        fontsize_list.append(fontsize)
        position_list.append(position)
        orientation_list.append(orientation)
        color_list.append(color)

    # get the positions
    x_arr = []
    y_arr = []
    for i in position_list:
        x_arr.append(i[0])
        y_arr.append(i[1])

    # get the relative occurence frequencies
    new_freq_list = []
    for i in freq_list:
        new_freq_list.append(i * 80)

    trace = go.Scatter(
        x=x_arr,
        y=y_arr,
        textfont=dict(size=new_freq_list, color=color_list),
        hoverinfo="text",
        textposition="top center",
        hovertext=["{0} - {1}".format(w, f) for w, f in zip(word_list, freq_list)],
        mode="text",
        text=word_list,
    )

    layout = go.Layout(
        {
            "xaxis": {
                "showgrid": False,
                "showticklabels": False,
                "zeroline": False,
                "automargin": True,
                "range": [-100, 250],
            },
            "yaxis": {
                "showgrid": False,
                "showticklabels": False,
                "zeroline": False,
                "automargin": True,
                "range": [-100, 450],
            },
            "margin": dict(t=20, b=20, l=10, r=10, pad=4),
            "hovermode": "closest",
        }
    )

    wordcloud_figure_data = {"data": [trace], "layout": layout}
    word_list_top = word_list[:20]
    word_list_top.reverse()
    freq_list_top = freq_list[:20]
    freq_list_top.reverse()

    frequency_figure_data = {
        "data": [
            {
                "y": word_list_top,
                "x": freq_list_top,
                "type": "bar",
                "name": "",
                "orientation": "h",
            }
        ],
        "layout": {"height": "400", "margin": dict(t=20, b=20, l=100, r=20, pad=4)},
    }
    treemap_trace = go.Treemap(
        labels=word_list_top, parents=[""] * len(word_list_top), values=freq_list_top
    )
    treemap_layout = go.Layout({"margin": dict(t=10, b=10, l=5, r=5, pad=4)})
    treemap_figure = {"data": [treemap_trace], "layout": treemap_layout}
    return wordcloud_figure_data, frequency_figure_data


def generate_heatmap(value):
    df = xyq_tools.getEntity()
    if value is None:
        return {'data': []}
    else:
        dff = df.loc[value, :]
        scaled_size = 200 + 150 + 50 * len(value)
        #        for row in dff.iterrows():
        z = dff.values.T.tolist()
        y = dff.columns.tolist()
        x = dff.index.T.tolist()
        print(x)
        print(y)
        print(z)
        annotations = []
        for n, row in enumerate(z):
            for m, val in enumerate(row):
                annotations.append(go.Annotation(text=str(z[n][m]), x=x[m], y=y[n],
                                                 xref='x1', yref='y1', showarrow=False))
        return {
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
                'height': 750,
                'width': scaled_size,
                'xaxis': {'side': 'top'},
                'annotations': annotations,
                'margin': {
                    'l': 200,
                    'r': 100,
                    'b': 150,
                    't': 100,
                }
            }
        }



def create_time_series(dff, column):
    print(column)
    return {
        'data': [dict(
            x=dff['chapter'],
            y=dff['polarity'],
            mode='lines+markers'
        )],
        'layout': {
            'height': 225,
            'margin': {'l': 50, 'b': 30, 'r': 10, 't': 10},
            'annotations': [{
                'x': 0, 'y': 0.85, 'xanchor': 'left', 'yanchor': 'bottom',
                'xref': 'paper', 'yref': 'paper', 'showarrow': False,
                'align': 'left', 'bgcolor': 'rgba(255, 255, 255, 0.5)',
                'text': 'sentiment analysis of '+ str(column)
            }],
            'yaxis': {'type': 'linear', 'title': 'Sentiment Polarity' },
            'xaxis': {'tickmode': 'array', 'ticktext': dff['chapter'], 'title': 'Chapter'}
        }
    }