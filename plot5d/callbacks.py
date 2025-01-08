from dash import callback, Output, Input
from dash.exceptions import PreventUpdate
from plot5d.plotdata import sample
from loguru import logger


@callback(
    Output("row_val_dropdown", "options"),
    Input("row_dropdown", "value"),
)
def update_row_val_dropdown(row_dropdown):
    if row_dropdown is None:
        raise PreventUpdate
    return sorted(set(sample.df[row_dropdown]))

@callback(
    Output("col_val_dropdown", "options"),
    Input("col_dropdown", "value"),
)
def update_col_val_dropdown(col_dropdown):
    if col_dropdown is None:
        raise PreventUpdate
    return sorted(set(sample.df[col_dropdown]))

@callback(
    Output("5DPlot", "figure"),
    Input("row_dropdown", "value"),
    Input("row_val_dropdown", "value"),
    Input("col_dropdown", "value"),
    Input("col_val_dropdown", "value"),
    Input("x_dropdown", "value"),
    Input("y_dropdown", "value"),
    Input("color_dropdown", "value"),
    Input("x_size", "value"),
    Input("y_size", "value"),
)
def update_5dplot(
    row_dropdown,
    row_val_dropdown,
    col_dropdown,
    col_val_dropdown,
    x_dropdown,
    y_dropdown,
    color_dropdown,
    x_size,
    y_size
):
    logger.info("row_dropdown={}", row_dropdown)
    logger.info("row_val_dropdown={}", row_val_dropdown)
    logger.info("col_dropdown={}", col_dropdown)
    logger.info("col_val_dropdown={}", col_val_dropdown)
    logger.info("x_dropdown={}", x_dropdown)
    logger.info("y_dropdown={}", y_dropdown)
    logger.info("color_dropdown={}", color_dropdown)
    logger.info("x_size={}", x_size)
    logger.info("y_size={}", y_size)
    if None in [row_dropdown, row_val_dropdown, col_dropdown, col_val_dropdown, x_dropdown, y_dropdown, color_dropdown]:
        raise PreventUpdate
    return sample.subplots(
        rows=(row_dropdown, row_val_dropdown),
        cols=(col_dropdown, col_val_dropdown),
        x=x_dropdown,
        y=y_dropdown,
        color=color_dropdown,
        figsize=(x_size, y_size)
    )
