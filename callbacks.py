from dash import Input, Output, State, callback, clientside_callback, ClientsideFunction, html
from dash_mantine_components import add_figure_templates
from dash.exceptions import PreventUpdate
import plotly.graph_objects as go
import base64
import pandas as pd
from io import StringIO
import json
import numpy as np
import csv


def generate_sample(maxval, nrows):
    np.random.seed(1)
    Q1 = np.linspace(1, maxval, nrows)
    Q2 = Q1 ** np.sqrt(2 + np.random.normal(1, 0.1, Q1.shape))
    Q3 = np.random.choice([100, 200, 300, 400, 500], Q1.shape)
    Q4 = np.log(Q3 * np.random.normal(1, 0.2, Q3.shape)) * np.log(Q2)
    Q5 = np.astype((np.floor(Q4) % 27 % 5 + 10) * 100, int)
    df = pd.DataFrame(data={"Q1": Q1, "Q2": Q2, "Q3": Q3, "Q4": Q4, "Q5": Q5})
    return df


@callback(
    Output("download-sample", "data"),
    Input("download-sample-btn", "n_clicks"),
    State("download-sample-lines", "value"),
)
def download_sample(n_clicks, data):
    if n_clicks is None:
        raise PreventUpdate
    return dict(content=generate_sample(400, data).to_csv(index=False), filename="sample.csv")


@callback(
    Output("data-storage", "data"),
    Output("df_upload", "children"),
    Output("loading-overlay", "visible", allow_duplicate=True),
    Output("metadata-storage", "data"),
    Output("df_upload", "className"),
    Input("df_upload", "contents"),
    State("df_upload", "filename"),
    prevent_initial_call=True,
)
def store_data(contents, filename):
    if contents is None:
        raise PreventUpdate
    _, string = contents.split(",")
    decoded = base64.b64decode(string).decode("utf-8")
    delim = csv.Sniffer().sniff(StringIO(decoded).read(4096)).delimiter
    df = pd.read_csv(StringIO(decoded), delimiter=delim)
    metadata = {
        "discrete": list(df.columns[df.nunique() / len(df) <= 0.05]),
        "continuous": list(df.columns[df.nunique() / len(df) > 0.05]),
    }
    df["_index"] = df.index
    return df.to_dict("records"), html.Div(f"{filename}"), False, metadata, "uploaded"


@callback(
    Output("loading-overlay", "visible", allow_duplicate=True),
    Input("df_upload", "filename"),
    prevent_initial_call=True,
)
def loading_overlay(filename):
    return True


clientside_callback(
    ClientsideFunction(namespace="clientside", function_name="update_dropdown"),
    Output("row-slct", "data"),
    Output("col-slct", "data"),
    Output("x-slct", "data"),
    Output("y-slct", "data"),
    Output("color-slct", "data"),
    Output("spider-slct", "data"),
    Input("data-storage", "data"),
    Input("metadata-storage", "data"),
    prevent_initial_call=True,
)

clientside_callback(
    ClientsideFunction(namespace="clientside", function_name="updateRowSelect"),
    Output("row-value-slct", "data"),
    Output("row-value-slct", "value"),
    Input("row-slct", "value"),
    State("data-storage", "data"),
    State("state_upload", "contents"),
)

clientside_callback(
    ClientsideFunction(namespace="clientside", function_name="update_col_dropdown"),
    Output("col-value-slct", "data"),
    Output("col-value-slct", "value"),
    Input("col-slct", "value"),
    State("data-storage", "data"),
    State("state_upload", "contents"),
)

clientside_callback(
    ClientsideFunction(namespace="clientside", function_name="buildMainplot"),
    Output("mainplot-storage", "data"),
    Output("mainplot", "style"),
    Input("x-slct", "value"),
    Input("y-slct", "value"),
    Input("color-slct", "value"),
    Input("row-slct", "value"),
    Input("row-value-slct", "value"),
    Input("col-slct", "value"),
    Input("col-value-slct", "value"),
    Input("filter-store", "data"),
    Input("alias-store", "data"),
    State("data-storage", "data"),
    State("mainplot", "style"),
)


@callback(
    Output("download-state", "data"),
    Input("download-state-btn", "n_clicks"),
    State("row-slct", "value"),
    State("row-value-slct", "value"),
    State("col-slct", "value"),
    State("col-value-slct", "value"),
    State("x-slct", "value"),
    State("y-slct", "value"),
    State("color-slct", "value"),
)
def save_state(
    n_clicks,
    row_dropdown,
    row_val_dropdown,
    col_dropdown,
    col_val_dropdown,
    x_dropdown,
    y_dropdown,
    color_dropdown,
):
    if n_clicks is None:
        raise PreventUpdate
    state = {
        "row_dropdown": row_dropdown,
        "row_val_dropdown": row_val_dropdown,
        "col_dropdown": col_dropdown,
        "col_val_dropdown": col_val_dropdown,
        "x_dropdown": x_dropdown,
        "y_dropdown": y_dropdown,
        "color_dropdown": color_dropdown,
    }
    return dict(content=json.dumps(state, indent=2), filename="state.json")


@callback(
    Output("row-slct", "value"),
    Output("col-slct", "value"),
    Output("x-slct", "value"),
    Output("y-slct", "value"),
    Output("color-slct", "value"),
    Input("state_upload", "contents"),
)
def load_state(data):
    if data is None:
        raise PreventUpdate
    _, string = data.split(",")
    decoded = base64.b64decode(string).decode("utf-8")
    state = json.loads(decoded)
    return (
        state["row_dropdown"],
        state["col_dropdown"],
        state["x_dropdown"],
        state["y_dropdown"],
        state["color_dropdown"],
    )


clientside_callback(
    ClientsideFunction(namespace="clientside", function_name="buildSpider"),
    Output("spider-storage", "data"),
    Output("spider-slct-memory", "data"),
    Output("spider", "style"),
    Output("download-selection-affix", "style"),
    Input("mainplot-selection-storage", "data"),
    Input("spider-slct", "value"),
    State("data-storage", "data"),
    State("spider", "style"),
    State("download-selection-btn", "style"),
)

clientside_callback(
    ClientsideFunction(namespace="clientside", function_name="storeSpiderFilters"),
    Output("spider-filters-memory", "data"),
    Input("spider", "restyleData"),
    State("spider-filters-memory", "data"),
)

clientside_callback(
    ClientsideFunction(namespace="clientside", function_name="DownloadFilteredCsv"),
    Output("download-selection", "data"),
    Input("download-selection-btn", "n_clicks"),
    State("spider-selection-storage", "data"),
    prevent_initial_call=True,
)


clientside_callback(
    """function(n_clicks, theme) {
        console.log(n_clicks);
        console.log(theme);
        return theme === "light" ? "dark" : "light"
    }
    """,
    Output("color-scheme-storage", "data"),
    Input("color-scheme-toggle", "n_clicks"),
    State("color-scheme-storage", "data"),
    prevent_initial_call=True,
)


@callback(
    Output("appshell", "navbar"),
    Output("navbar-open-icon", "style"),
    Output("navbar-closed-icon", "style"),
    Input("navbar-toggle", "n_clicks"),
    State("navbar-open-icon", "style"),
    State("navbar-closed-icon", "style"),
    State("appshell", "navbar"),
)
def toggle_navbar(n_clicks, open_style, closed_style, navbar):
    _open_style = open_style
    _closed_style = closed_style
    if _open_style["display"] == "none":
        _open_style["display"] = "block"
    else:
        _open_style["display"] = "none"
    if _closed_style["display"] == "none":
        _closed_style["display"] = "block"
    else:
        _closed_style["display"] = "none"

    navbar["collapsed"] = {"desktop": _closed_style["display"] == "block"}
    return navbar, _open_style, _closed_style


clientside_callback(
    "function(colorScheme) {return colorScheme}",
    Output("provider", "forceColorScheme"),
    Input("color-scheme-storage", "data"),
)

add_figure_templates()


@callback(
    Output("mainplot", "figure"),
    Input("mainplot-storage", "data"),
    Input("color-scheme-storage", "data"),
)
def figure_theme(figdata, theme):
    fig = go.Figure(figdata)
    if theme == "light":
        fig.layout.template = "mantine_light"
    else:
        fig.layout.template = "mantine_dark"

    return fig


@callback(
    Output("spider", "figure"),
    Input("spider-storage", "data"),
    Input("color-scheme-storage", "data"),
)
def spider_theme(figdata, theme):
    fig = go.Figure(figdata)
    if theme == "light":
        fig.layout.template = "mantine_light"
    else:
        fig.layout.template = "mantine_dark"

    return fig


@callback(
    Output("helper-modal", "opened"),
    Input("help", "n_clicks"),
    State("helper-modal", "opened"),
    prevent_initial_call=True,
)
def helper_overlay(n_clicks, opened):
    return not opened


@callback(
    Output("settings-modal", "opened"),
    Input("settings", "n_clicks"),
    State("settings-modal", "opened"),
    prevent_initial_call=True,
)
def settings_overlay(n_clicks, opened):
    return not opened


@callback(
    Output("mainplot-navbar", "style"),
    Input("tabs", "value"),
)
def display_mainplot_navbar(active_tab):
    if active_tab == "mainplot":
        return {"display": "block"}
    return {"display": "none"}


@callback(
    Output("spider-navbar", "style"),
    Input("tabs", "value"),
)
def display_spider_navbar(active_tab):
    if active_tab == "spider":
        return {"display": "block"}
    return {"display": "none"}


clientside_callback(
    ClientsideFunction("clientside", "storeMainplotSelection"),
    Output("mainplot-selection-storage", "data"),
    Input("mainplot", "selectedData"),
    Input("data-storage", "data"),
)

clientside_callback(
    ClientsideFunction("clientside", "storeSpiderSelection"),
    Output("spider-selection-storage", "data"),
    Input("spider-filters-memory", "data"),
    State("spider-slct-memory", "data"),
    State("mainplot-selection-storage", "data"),
)


@callback(
    Output("table", "rowData"),
    Output("table", "columnDefs"),
    Input("spider-selection-storage", "data"),
)
def build_table(data):
    print(data)
    if data is None:
        raise PreventUpdate
    if len(data) == 0:
        raise PreventUpdate
    return data, [{"field": k} for k in data[0].keys() if k != "_index"]
