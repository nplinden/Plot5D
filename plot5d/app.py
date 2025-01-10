from .server import app
from dash import html, dcc, dash_table
import dash_bootstrap_components as dbc
from plot5d.plotdata import sample
from plot5d.callbacks import *
from plot5d.components.textbox import textbox
from plot5d.components.menu import menu

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

row_dropdown = dcc.Dropdown(columns, id="row_dropdown", className="dropdown")
row_val_dropdown = dcc.Dropdown([], id="row_val_dropdown", multi=True, className="dropdown")
col_dropdown = dcc.Dropdown(columns, id="col_dropdown", className="dropdown")
col_val_dropdown = dcc.Dropdown([], id="col_val_dropdown", multi=True, className="dropdown")
x_dropdown = dcc.Dropdown(columns, id="x_dropdown", className="dropdown")
y_dropdown = dcc.Dropdown(columns, id="y_dropdown", className="dropdown")
color_dropdown = dcc.Dropdown(columns, id="color_dropdown", className="dropdown")
x_min = dcc.Input(id="x_min", type="number", placeholder="Min", className="input")
x_max = dcc.Input(id="x_max", type="number", placeholder="Max", className="input")
y_min = dcc.Input(id="y_min", type="number", placeholder="Min", className="input")
y_max = dcc.Input(id="y_max", type="number", placeholder="Max", className="input")
color_min = dcc.Input(id="color_min", type="number", placeholder="Min", className="input")
color_max = dcc.Input(id="color_max", type="number", placeholder="Max", className="input")
table_dropdown = dcc.Dropdown(columns, id="column_dropdown", className="dropdown", multi=True)
parcoord_dropdown = dcc.Dropdown(columns, id="parcoord_dropdown", className="dropdown", multi=True)

core = dbc.Container(
    [
        dbc.Row(
            textbox("An app to explore your favourite DataFrames", "Plot5D by Nicolas Linden"),
            className="textbox-container",
        ),
        dcc.Upload(
            id="load_state",
            children=html.Div("Upload state file"),
            className="upload",
            multiple=False,
        ),
        dbc.Row(
            [
                menu("Row Quantity", components=[row_dropdown, row_val_dropdown], col=True),
                menu("Column Quantity", components=[col_dropdown, col_val_dropdown], col=True),
            ]
        ),
        dbc.Row(
            [
                menu("X Axis Quantity", components=[x_dropdown, x_max, x_min], col=True),
                menu("Y Axis Quantity", components=[y_dropdown, y_min, y_max], col=True),
                menu(
                    "Color Axis Quantity",
                    components=[color_dropdown, color_min, color_max],
                    col=True,
                ),
            ]
        ),
        dbc.Row(
            [
                html.Button("Save State", id="btn-download-txt", className="upload"),
                dcc.Download(id="download-text"),
            ]
        ),
        dbc.Row(
            html.Div(
                dcc.Graph(id="5DPlot", className="graph"),
                className="graph-div",
            )
        ),
        dbc.Row(
            html.Div(
                [table_dropdown, table],
                className="table-div",
            )
        ),
        dbc.Row(
            html.Div(
                [parcoord_dropdown, dcc.Graph(id="parcoords", className="graph")],
                className="graph-div",
            )
        ),
    ]
)

app.layout = html.Div(children=[core])
