from dash import Output, Input, State, no_update
from dash.exceptions import PreventUpdate
from plot5d.plotdata import sample
from loguru import logger
import json
import base64


def define_graph_callbacks(app):
    @app.callback(
        Output("5DPlot", "figure"),
        Output("5DPlot", "selectedData"),
        Output("5DPlot", "relayoutData"),
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
        Input("row_dropdown_title", "value"),
        Input("col_dropdown_title", "value"),
        Input("x_dropdown_title", "value"),
        Input("y_dropdown_title", "value"),
        Input("color_dropdown_title", "value"),
        State("load_state", "contents"),
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
        row_title,
        col_title,
        x_title,
        y_title,
        color_title,
        upload_content,
    ):
        logger.info("row_dropdown={}", row_dropdown)
        logger.info("row_val_dropdown={}", row_val_dropdown)
        logger.info("col_dropdown={}", col_dropdown)
        logger.info("col_val_dropdown={}", col_val_dropdown)
        logger.info("x_dropdown={}", x_dropdown)
        logger.info("y_dropdown={}", y_dropdown)
        logger.info("color_dropdown={}", color_dropdown)
        logger.info("row_title={}", row_title)
        logger.info("col_title={}", col_title)
        logger.info("x_title={}", x_title)
        logger.info("y_title={}", y_title)
        logger.info("color_title={}", color_title)

        if None in [
            x_dropdown,
            y_dropdown,
            color_dropdown,
        ]:
            raise PreventUpdate
        graph = sample.subplots(
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
            row_title=row_title,
            col_title=col_title,
            x_title=x_title,
            y_title=y_title,
            color_title=color_title,
        )
        if upload_content is None:
            selected_data = no_update
            relayout_data = no_update
        else:
            _, string = upload_content.split(",")
            decoded = base64.b64decode(string).decode("utf-8")
            state = json.loads(decoded)
            selected_data = state.get("selected_data", None)
            relayout_data = state.get("relayout_data", None)
        return graph, selected_data, relayout_data
