#!/usr/bin/env python3
# -*- coding=utf-8 -*-

import base64
import io

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State

import plotly.graph_objs as go

import pandas as pd
import numpy as np

__author__ = "Germain Salvato Vallverdu"
__title__ = "Abaque: a contour plot"

#drc = importlib.import_module("apps.dash-svm.utils.dash_reusable_components")
#figs = importlib.import_module("apps.dash-svm.utils.figures")

ext_css = ["https://use.fontawesome.com/releases/v5.8.1/css/all.css"]
app = dash.Dash(
    __name__,
    meta_tags=[
        {"name": "viewport", "content": "width=device-width, initial-scale=1.0"}
    ],
    url_base_pathname="/abaque/",
    external_stylesheets=ext_css,
)
server = app.server

def mySlider(name, **kwargs):
    return html.Div(
        className="slider_bloc",
        children=[
            html.P(name, className="slider_name"),
            html.Div(dcc.Slider(**kwargs), className="slider")
        ]
    )

#
# Layout
# ------------------------------------------------------------------------------

# --- header ---
header = html.Div(className="head", children=[
    html.H1(children=[html.Span(className="fas fa-atom"), " ", __title__]),
    # html.H2(__subtitle__)
    html.A(
        id="github-link",
        href="https://github.com/gVallverdu/abaque",
        children=[
            "View on GitHub",
        ]
    ),
    html.Span(id="github-icon", className="fab fa-github fa-2x"),
])

# --- Footer ---
footer = html.Div(className="foot", children=[
    html.Div(className="container scalable", children=[
        html.Div(className="about", children=[
            html.H5("About:"),
            html.P([
                html.A("Germain Salvato Vallverdu",
                       href="https://gsalvatovallverdu.gitlab.io/")]),
            html.P(
                html.A(href="https://www.univ-pau.fr", children=[
                    "University of Pau & Pays Adour"
                ])
            )
        ]),
        html.Div(className="uppa-logo", children=[
            html.A(href="https://www.univ-pau.fr", children=[
                html.Img(
                    src=app.get_asset_url("img/LogoUPPAblanc.png"),
                )
            ])]
        )
    ])
])

# --- Body ---
body = html.Div(
    id="body",
    className="container scalable", 
    children=[
        html.Div(
            id="app-container",
            children=[
                html.Div(
                    id="left-column",
                    children=[

                        # --- select a data set
                        html.P("Select Dataset:"),
                        dcc.Dropdown(
                            id="dropdown-dataset",
                            options=[{"label": "miel", "value": "data/miel.csv"},
                                     {"label": "rhum", "value": "data/rhum.csv"}],
                            value="data/miel.csv",                            
                        ),

                        # --- upload
                        dcc.Upload(
                            id='file-upload',
                            children=html.Div(
                                className="upload-area",
                                children="Upload data here"
                            ),
                        ),

                        # --- fit parameters
                        mySlider(
                            name="kx",
                            id="x-slider",
                            min=0, max=5, step=1, value=1,
                            marks={i: {"label": str(i)} for i in range(6)},
                        ),

                        mySlider(
                            name="ky",
                            id="y-slider",
                            min=0, max=5, step=1, value=1,
                            marks={i: {"label": str(i)} for i in range(6)},
                        ),
                    ]
                ),
                html.Div(
                    id="graph",
                    children=dcc.Graph(
                        id="contour-plot",
                    )
                )
            ]
        )

    ]
)

app.layout = html.Div([header, body, footer])


#
# Callbacks
# ------------------------------------------------------------------------------

@app.callback(
    Output("contour-plot", "figure"),
    [Input("file-upload", "contents"),
     Input("file-upload", "filename"),
     Input("dropdown-dataset", "value")]
)
def upload_data(contents, filename, dataset):

    if contents is None:
        filename = app.get_asset_url(dataset)
        print(filename)
        filename = "assets/" + dataset
        df = pd.read_csv(filename, sep=";", index_col=0)
        return dict(data=[go.Scatter(x=df.iloc[:, 0], y=df.iloc[:, 1])], layout=dict(title=dataset))

    _, content_string = contents.split(',')

    decoded = base64.b64decode(content_string)
    try:
        if 'csv' in filename:
            # Assume that the user uploaded a CSV file
            df = pd.read_csv(io.StringIO(decoded.decode('utf-8')), sep=";", decimal=",")
        elif 'xls' in filename:
            # Assume that the user uploaded an excel file
            df = pd.read_excel(io.BytesIO(decoded))
    except Exception as e:
        print(e)
        return html.Div([
            'There was an error processing this file.'
        ])

    print(df.iloc[:, 0])

    figure = dict(data=[go.Scatter(x=df.iloc[:, 0], y=df.iloc[:, 1])], layout=dict(title=filename))

    return figure

# Running the server
if __name__ == "__main__":
    app.run_server(debug=True)
