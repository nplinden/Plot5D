from dash import Output, Input, State, clientside_callback, ClientsideFunction
from dash.exceptions import PreventUpdate
import base64
from io import StringIO
import pandas as pd
import json
import time


def define_clientside_callbacks(app):
    @app.callback(
        Output("storage", "data"),
        Output("df_upload", "children"),
        Output("spinner", "children"),
        Input("df_upload", "contents"),
        State("df_upload", "filename"),
    )
    def store_data(contents, filename):
        if contents is None:
            raise PreventUpdate
        _, string = contents.split(",")
        decoded = base64.b64decode(string).decode("utf-8")
        df = pd.read_csv(StringIO(decoded))
        df["index"] = df.index
        return df.to_dict("records"), filename, None

    clientside_callback(
        ClientsideFunction(namespace="clientside", function_name="update_dropdown"),
        Output("row_dropdown", "options"),
        Output("col_dropdown", "options"),
        Output("x_dropdown", "options"),
        Output("y_dropdown", "options"),
        Output("color_dropdown", "options"),
        Output("parcoord_dropdown", "options"),
        Output("table_dropdown", "options"),
        Input("storage", "data"),
    )

    clientside_callback(
        ClientsideFunction(namespace="clientside", function_name="update_row_dropdown"),
        Output("row_val_dropdown", "options"),
        Output("row_val_dropdown", "value"),
        Input("row_dropdown", "value"),
        State("storage", "data"),
        State("load_state", "contents"),
    )

    clientside_callback(
        ClientsideFunction(namespace="clientside", function_name="update_col_dropdown"),
        Output("col_val_dropdown", "options"),
        Output("col_val_dropdown", "value"),
        Input("col_dropdown", "value"),
        State("storage", "data"),
        State("load_state", "contents"),
    )

    clientside_callback(
        ClientsideFunction(namespace="clientside", function_name="update_subplot"),
        Output("5DPlot", "figure"),
        Input("x_dropdown", "value"),
        Input("y_dropdown", "value"),
        Input("color_dropdown", "value"),
        Input("row_dropdown", "value"),
        Input("row_val_dropdown", "value"),
        Input("col_dropdown", "value"),
        Input("col_val_dropdown", "value"),
        Input("x_min", "value"),
        Input("x_max", "value"),
        Input("y_min", "value"),
        Input("y_max", "value"),
        Input("color_min", "value"),
        Input("color_max", "value"),
        State("storage", "data"),
    )

    @app.callback(
        Output("download-text", "data"),
        Input("btn-download-txt", "n_clicks"),
        State("row_dropdown", "value"),
        State("row_val_dropdown", "value"),
        State("col_dropdown", "value"),
        State("col_val_dropdown", "value"),
        State("x_dropdown", "value"),
        State("y_dropdown", "value"),
        State("color_dropdown", "value"),
        State("x_min", "value"),
        State("x_max", "value"),
        State("y_min", "value"),
        State("y_max", "value"),
        State("color_min", "value"),
        State("color_max", "value"),
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

    @app.callback(
        Output("row_dropdown", "value"),
        Output("col_dropdown", "value"),
        Output("x_dropdown", "value"),
        Output("y_dropdown", "value"),
        Output("color_dropdown", "value"),
        Output("x_min", "value"),
        Output("x_max", "value"),
        Output("y_min", "value"),
        Output("y_max", "value"),
        Output("color_min", "value"),
        Output("color_max", "value"),
        Input("load_state", "contents"),
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
        ClientsideFunction(namespace="clientside", function_name="select_data_for_parcoord"),
        Output("parcoords", "figure"),
        Output("parcoords_dropdown_memory", "data"),
        Input("5DPlot", "selectedData"),
        Input("parcoord_dropdown", "value"),
        State("storage", "data"),
    )

    clientside_callback(
        ClientsideFunction(namespace="clientside", function_name="store_parcoord_style"),
        Output("parcoords_memory", "data"),
        Input("parcoords", "restyleData"),
        State("parcoords_memory", "data"),
    )

    clientside_callback(
        ClientsideFunction(namespace="clientside", function_name="draw_table"),
        Output("table", "data"),
        Output("table", "columns"),
        Output("table", "page_count"),
        Input("parcoords_dropdown_memory", "data"),
        Input("parcoords_memory", "data"),
        Input("table", "page_current"),
        Input("table_dropdown", "value"),
        State("5DPlot", "selectedData"),
        State("table", "page_size"),
        State("storage", "data"),
    )
