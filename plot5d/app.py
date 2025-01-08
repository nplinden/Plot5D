from .server import app
from dash import html, dcc
import dash_bootstrap_components as dbc
from plot5d.plotdata import sample
from plot5d.callbacks import *

columns = list(sample.df.columns)

app.layout = html.Div(
        [html.H1("Plot5D"),
        html.H3("Plot Size"),
        dcc.Input(id="x_size", type="number", value=800, step=50, placeholder="X Size"),
        dcc.Input(id="y_size", type="number", value=800, step=50, placeholder="Y Size"),
        dbc.Row(
            [
                dbc.Col(html.H3("Row QOI")),
                dbc.Col(html.H3("Column QOI")),
             ],
        ),
        dbc.Row(
            [
                dbc.Col(dcc.Dropdown(columns, id="row_dropdown")),
                dbc.Col(dcc.Dropdown([], id="row_val_dropdown", multi=True)),
                dbc.Col(dcc.Dropdown(columns, id="col_dropdown")),
                dbc.Col(dcc.Dropdown([], id="col_val_dropdown", multi=True)),
             ],
        ),
        dbc.Row(
            [
                dbc.Col(html.H3("X axis QOI")),
                dbc.Col(html.H3("Y axis QOI")),
                dbc.Col(html.H3("Color QOI")),
             ],
        ),
        dbc.Row(
            [
                dbc.Col(dcc.Dropdown(columns, id="x_dropdown")),
                dbc.Col(dcc.Dropdown(columns, id="y_dropdown")),
                dbc.Col(dcc.Dropdown(columns, id="color_dropdown")),
             ],
        ),
        dcc.Graph(id="5DPlot")
                  ]
)