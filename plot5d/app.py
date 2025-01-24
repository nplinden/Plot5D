from .server import app
from dash import html, dcc, dash_table
import dash_bootstrap_components as dbc
from plot5d.callbacks import define_clientside_callbacks


def menu(title, components=None, col=False):
    if components is None:
        components = []
    if col:
        menu_component = dbc.Col(
            html.Div(
                [html.Div(title, className="menu-title"), *components],
                className="menu-div",
            ),
            className="col-menu",
        )
    else:
        menu_component = html.Div([html.Div(title, className="menu-title"), *components], className="menu-div")
    return menu_component


def textbox(text, title=None):
    text_component = html.Div(html.Div(text, className="textbox-text"))

    if title is not None:
        title_component = html.Div(children=title, className="textbox-title")

        return [title_component, text_component]
    return [text_component]


define_clientside_callbacks(app)

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

row_dropdown = dcc.Dropdown([], id="row_dropdown", className="dropdown")
row_val_dropdown = dcc.Dropdown([], id="row_val_dropdown", multi=True, className="dropdown")
row_dropdown_title = dcc.Checklist(
    [" Display title"], [" Display title"], id="row_dropdown_title", style={"textAlign": "right"}
)
col_dropdown = dcc.Dropdown([], id="col_dropdown", className="dropdown")
col_val_dropdown = dcc.Dropdown([], id="col_val_dropdown", multi=True, className="dropdown")
col_dropdown_title = dcc.Checklist(
    [" Display title"], [" Display title"], id="col_dropdown_title", style={"textAlign": "right"}
)
x_dropdown = dcc.Dropdown([], id="x_dropdown", className="dropdown")
x_dropdown_title = dcc.Checklist(
    [" Display title"], [" Display title"], id="x_dropdown_title", style={"textAlign": "right"}
)
y_dropdown = dcc.Dropdown([], id="y_dropdown", className="dropdown")
y_dropdown_title = dcc.Checklist(
    [" Display title"], [" Display title"], id="y_dropdown_title", style={"textAlign": "right"}
)
color_dropdown = dcc.Dropdown([], id="color_dropdown", className="dropdown")
color_dropdown_title = dcc.Checklist(
    [" Display title"], [" Display title"], id="color_dropdown_title", style={"textAlign": "right"}
)
x_min = dcc.Input(id="x_min", type="number", placeholder="Min", className="input")
x_max = dcc.Input(id="x_max", type="number", placeholder="Max", className="input")
y_min = dcc.Input(id="y_min", type="number", placeholder="Min", className="input")
y_max = dcc.Input(id="y_max", type="number", placeholder="Max", className="input")
color_min = dcc.Input(id="color_min", type="number", placeholder="Min", className="input")
color_max = dcc.Input(id="color_max", type="number", placeholder="Max", className="input")
table_dropdown = dcc.Dropdown([], id="table_dropdown", className="dropdown", multi=True)
parcoord_dropdown = dcc.Dropdown([], id="parcoord_dropdown", className="dropdown", multi=True)

core = dbc.Container(
    [
        dbc.Row(
            textbox(
                "An app to explore your favourite DataFrames. Sur une idée originale de Corentin Reiss",
                "Plot5D by Nicolas Linden",
            ),
            className="textbox-container",
        ),
        dcc.Upload(
            id="df_upload",
            children=html.Div("Upload csv file"),
            className="upload",
            multiple=False,
        ),
        dcc.Store(id="storage", storage_type="memory"),
        dcc.Upload(
            id="load_state",
            children=html.Div("Upload state file"),
            className="upload",
            multiple=False,
        ),
        dbc.Row(
            [
                dbc.Col(
                    html.Div(
                        [
                            html.Div("Row Quantity", className="menu-title"),
                            row_dropdown,
                            row_val_dropdown,
                            row_dropdown_title,
                        ],
                        className="menu-div",
                    ),
                    className="col-menu",
                ),
                dbc.Col(
                    html.Div(
                        [
                            html.Div("Column Quantity", className="menu-title"),
                            col_dropdown,
                            col_val_dropdown,
                            col_dropdown_title,
                        ],
                        className="menu-div",
                    ),
                    className="col-menu",
                ),
            ]
        ),
        dbc.Row(
            [
                menu("X Axis Quantity", components=[x_dropdown, x_min, x_max, x_dropdown_title], col=True),
                menu("Y Axis Quantity", components=[y_dropdown, y_min, y_max, y_dropdown_title], col=True),
                menu(
                    "Color Axis Quantity",
                    components=[color_dropdown, color_min, color_max, color_dropdown_title],
                    col=True,
                ),
            ]
        ),
        dbc.Row(
            [
                html.Div(
                    children=html.Button("Save State", id="btn-download-txt", className="upload"),
                ),
                dcc.Download(id="download-text"),
            ]
        ),
        dbc.Row(
            [
                html.Div(
                    dcc.Graph(id="5DPlot", className="graph"),
                    className="graph-div",
                )
            ]
        ),
        dbc.Row(
            html.Div(
                [
                    parcoord_dropdown,
                    dcc.Store(id="parcoords_dropdown_memory", storage_type="memory"),
                    dcc.Store(id="parcoords_memory", storage_type="memory"),
                    dcc.Graph(id="parcoords", className="graph", style={"height": "90%"}),
                ],
                className="graph-div",
            )
        ),
        dbc.Row(
            html.Div(
                [table_dropdown, table],
                className="table-div",
            )
        ),
    ]
)

app.layout = html.Div(children=[core])
