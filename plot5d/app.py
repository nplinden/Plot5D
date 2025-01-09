from .server import app
from dash import html, dcc, dash_table
import dash_bootstrap_components as dbc
from plot5d.plotdata import sample
from plot5d.callbacks import *

table = dash_table.DataTable(
    id="table",
    page_current=0,
    page_size=12,
    page_action="custom",
    style_cell={"fontSize": 20, "font-familiy": "monospace"},
    sort_action="custom",
    sort_mode="single",
    sort_by=[],
    tooltip_duration=None,
)

columns = list(sample.df.columns)

app.layout = html.Div(
    [
        html.H1("Plot5D"),
        dcc.Upload(
            id='load_state',
            children=html.Div([
                'Drag and Drop or ',
                html.A('Select Files')
            ]),
            style={
                'width': '100%',
                'height': '60px',
                'lineHeight': '60px',
                'borderWidth': '1px',
                'borderStyle': 'dashed',
                'borderRadius': '5px',
                'textAlign': 'center',
                'margin': '10px'
            },
            # Allow multiple files to be uploaded
            multiple=False
        ),
        html.Div(
            children = [
                html.P("X size ",  style={'display': 'inline-block', "margin": "10px"}),
                dcc.Input(id="x_size", type="number", value=1200, step=50, placeholder="X Size",  style={'display': 'inline-block', "margin": "10px"}),
                html.P("Y size:",  style={'display': 'inline-block', "margin": "10px"}),
                dcc.Input(id="y_size", type="number", value=1200, step=50, placeholder="Y Size",  style={'display': 'inline-block'}),
            ]
        ),
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
        dbc.Row(
            [
                dbc.Col(html.P("Min: ")),
                dbc.Col(dcc.Input(id="x_min", type="number")),
                dbc.Col(html.P("Max: ")),
                dbc.Col(dcc.Input(id="x_max", type="number")),
                dbc.Col(html.P("Min: ")),
                dbc.Col(dcc.Input(id="y_min", type="number")),
                dbc.Col(html.P("Max: ")),
                dbc.Col(dcc.Input(id="y_max", type="number")),
                dbc.Col(html.P("Min: ")),
                dbc.Col(dcc.Input(id="color_min", type="number")),
                dbc.Col(html.P("Max: ")),
                dbc.Col(dcc.Input(id="color_max", type="number")),
            ],
        ),
        html.Button("Save State", id="btn-download-txt"),
        dcc.Download(id="download-text"),
        dcc.Graph(id="5DPlot"),
        table,
    ]
)
