from dash import callback, Output, Input, State
from dash.exceptions import PreventUpdate
from plot5d.plotdata import sample
from loguru import logger
import json
import base64


@callback(
    Output("row_val_dropdown", "options"),
    Output("row_val_dropdown", "value"),
    Input("row_dropdown", "value"),
    State("load_state", "contents"),
)
def update_row_val_dropdown(row_dropdown, data):
    if row_dropdown is None:
        raise PreventUpdate
    if data is not None:
        _, string = data.split(",")
        decoded = base64.b64decode(string).decode("utf-8")
        state = json.loads(decoded)
        value = state["row_val_dropdown"]
    else:
        value = []
    return sorted(set(sample.df[row_dropdown])), value


@callback(
    Output("col_val_dropdown", "options"),
    Output("col_val_dropdown", "value"),
    Input("col_dropdown", "value"),
    State("load_state", "contents"),
)
def update_col_val_dropdown(col_dropdown, data):
    if col_dropdown is None:
        raise PreventUpdate
    if data is not None:
        _, string = data.split(",")
        decoded = base64.b64decode(string).decode("utf-8")
        state = json.loads(decoded)
        value = state["col_val_dropdown"]
    else:
        value = []
    return sorted(set(sample.df[col_dropdown])), value


@callback(
    Output("5DPlot", "figure"),
    Input("row_dropdown", "value"),
    Input("row_val_dropdown", "value"),
    Input("col_dropdown", "value"),
    Input("col_val_dropdown", "value"),
    Input("x_dropdown", "value"),
    Input("y_dropdown", "value"),
    Input("color_dropdown", "value"),
    Input("x_min", "value"),
    Input("x_max", "value"),
    Input("y_min", "value"),
    Input("y_max", "value"),
    Input("color_min", "value"),
    Input("color_max", "value"),
)
def update_5dplot(
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
    logger.info("row_dropdown={}", row_dropdown)
    logger.info("row_val_dropdown={}", row_val_dropdown)
    logger.info("col_dropdown={}", col_dropdown)
    logger.info("col_val_dropdown={}", col_val_dropdown)
    logger.info("x_dropdown={}", x_dropdown)
    logger.info("y_dropdown={}", y_dropdown)
    logger.info("color_dropdown={}", color_dropdown)
    if None in [
        row_dropdown,
        row_val_dropdown,
        col_dropdown,
        col_val_dropdown,
        x_dropdown,
        y_dropdown,
        color_dropdown,
    ]:
        raise PreventUpdate
    return sample.subplots(
        rows=(row_dropdown, row_val_dropdown),
        cols=(col_dropdown, col_val_dropdown),
        x=x_dropdown,
        y=y_dropdown,
        color=color_dropdown,
        x_min=x_min,
        x_max=x_max,
        y_min=y_min,
        y_max=y_max,
        color_min=color_min,
        color_max=color_max,
    )


@callback(
    [
        Output("table", "data"),
        Output("table", "columns"),
        Output("table", "page_count"),
    ],
    Input("5DPlot", "selectedData"),
    Input("table", "page_current"),
    State("table", "page_size"),
)
def select_data(selected, page_current, page_size):
    if selected is None:
        raise PreventUpdate
    idx = [d["customdata"] for d in selected["points"]]
    df = sample.df.iloc[idx]
    print(df)
    print(len(df))
    page_count = len(df) // page_size + 1
    if len(df) > 0 and len(df) % page_size == 0:
        page_count -= 1
    df = df.iloc[page_current * page_size : (page_current + 1) * page_size]

    return df.to_dict("records"), [{"name": c, "id": c} for c in df.columns], page_count


@callback(
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
    prevent_initial_call=True,
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


# # @callback(
# #     Input("upload_data", "contents")
# # )
# # def load_data(data):
# #     tpe, string = data.split(",")
# #     decoded = base64.b64decode(string).decode("utf-8")
# #     with open("tmp.csv", "w") as f:
# #         f.write(decoded)
# #     # return PlotData("tmp.csv")
# #     print(PlotData("tmp.csv").df)
