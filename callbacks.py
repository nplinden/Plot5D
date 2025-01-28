from dash import (
    Input,
    Output,
    State,
    callback,
    clientside_callback,
    ClientsideFunction,
)
from dash_mantine_components import add_figure_templates
from dash.exceptions import PreventUpdate
import plotly.graph_objects as go
import base64
import pandas as pd
from io import StringIO
import json
import numpy as np


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
    Output("storage", "data"),
    Output("df_upload", "style"),
    Output("loading-overlay", "visible", allow_duplicate=True),
    Input("df_upload", "contents"),
    State("df_upload", "filename"),
    prevent_initial_call=True,
)
def store_data(contents, filename):
    if contents is None:
        raise PreventUpdate
    print(filename)
    _, string = contents.split(",")
    decoded = base64.b64decode(string).decode("utf-8")
    df = pd.read_csv(StringIO(decoded))
    df["index"] = df.index
    return df.to_dict("records"), {"display": "none"}, False


clientside_callback(
    ClientsideFunction(namespace="clientside", function_name="loading_overlay"),
    Output("loading-overlay", "visible", allow_duplicate=True),
    Input("df_upload", "filename"),
    prevent_initial_call=True,
)

clientside_callback(
    ClientsideFunction(namespace="clientside", function_name="update_dropdown"),
    Output("row-slct", "data"),
    Output("col-slct", "data"),
    Output("x-slct", "data"),
    Output("y-slct", "data"),
    Output("color-slct", "data"),
    Output("spider-slct", "data"),
    Output("table-slct", "data"),
    Input("storage", "data"),
    prevent_initial_call=True,
)

clientside_callback(
    ClientsideFunction(namespace="clientside", function_name="update_row_dropdown"),
    Output("row-value-slct", "data"),
    Output("row-value-slct", "value"),
    Input("row-slct", "value"),
    State("storage", "data"),
    State("state_upload", "contents"),
)

clientside_callback(
    ClientsideFunction(namespace="clientside", function_name="update_col_dropdown"),
    Output("col-value-slct", "data"),
    Output("col-value-slct", "value"),
    Input("col-slct", "value"),
    State("storage", "data"),
    State("state_upload", "contents"),
)

clientside_callback(
    ClientsideFunction(namespace="clientside", function_name="update_subplot"),
    # Output("mainplot", "figure"),
    Output("mainplot-storage", "data"),
    Output("mainplot", "style"),
    Input("x-slct", "value"),
    Input("y-slct", "value"),
    Input("color-slct", "value"),
    Input("row-slct", "value"),
    Input("row-value-slct", "value"),
    Input("col-slct", "value"),
    Input("col-value-slct", "value"),
    Input("x-min", "value"),
    Input("x-max", "value"),
    Input("y-min", "value"),
    Input("y-max", "value"),
    Input("color-min", "value"),
    Input("color-max", "value"),
    State("storage", "data"),
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
    State("x-min", "value"),
    State("x-max", "value"),
    State("y-min", "value"),
    State("y-max", "value"),
    State("color-min", "value"),
    State("color-max", "value"),
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
    x_min,
    x_max,
    y_min,
    y_max,
    color_min,
    color_max,
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
        "x_min": x_min,
        "x_max": x_max,
        "y_min": y_min,
        "y_max": y_max,
        "color_min": color_min,
        "color_max": color_max,
    }
    return dict(content=json.dumps(state, indent=2), filename="state.json")


@callback(
    Output("row-slct", "value"),
    Output("col-slct", "value"),
    Output("x-slct", "value"),
    Output("y-slct", "value"),
    Output("color-slct", "value"),
    Output("x-min", "value"),
    Output("x-max", "value"),
    Output("y-min", "value"),
    Output("y-max", "value"),
    Output("color-min", "value"),
    Output("color-max", "value"),
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
        state["x_min"],
        state["x_max"],
        state["y_min"],
        state["y_max"],
        state["color_min"],
        state["color_max"],
    )


clientside_callback(
    ClientsideFunction(namespace="clientside", function_name="build_spider"),
    Output("spider-storage", "data"),
    Output("spider-slct-memory", "data"),
    Output("spider", "style"),
    Input("mainplot", "selectedData"),
    Input("spider-slct", "value"),
    State("storage", "data"),
    State("spider", "style"),
)

clientside_callback(
    ClientsideFunction(namespace="clientside", function_name="store_spider_filters"),
    Output("spider-memory", "data"),
    Input("spider", "restyleData"),
    State("spider-memory", "data"),
)

clientside_callback(
    ClientsideFunction(namespace="clientside", function_name="draw_table"),
    Output("table", "data"),
    Output("table", "columns"),
    Output("table", "page_count"),
    Input("spider-slct-memory", "data"),
    Input("spider-memory", "data"),
    Input("table", "page_current"),
    Input("table-slct", "value"),
    State("mainplot", "selectedData"),
    State("table", "page_size"),
    State("storage", "data"),
)


@callback(
    Output("appshell", "navbar"),
    Input("burger", "opened"),
    State("appshell", "navbar"),
)
def navbar_is_open(opened, navbar):
    navbar["collapsed"] = {"mobile": not opened}
    return navbar


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
