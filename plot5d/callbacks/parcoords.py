from dash import Output, Input, State
from dash.exceptions import PreventUpdate
from plot5d.plotdata import sample
import re
from loguru import logger
import plotly.express as px


def define_parcoords_callbacks(app):
    @app.callback(
        Output("parcoords", "figure"),
        Output("parcoords_dropdown_memory", "data"),
        Input("5DPlot", "selectedData"),
        Input("parcoord_dropdown", "value"),
    )
    def select_data_for_parcoord(selected, parcoord_dropdown):
        if parcoord_dropdown is None:
            raise PreventUpdate
        if selected is None:
            raise PreventUpdate

        idx = [d["customdata"] for d in selected["points"]]
        df = sample.df.iloc[idx]
        columns = {k: k for k in parcoord_dropdown}
        parcoords = px.parallel_coordinates(
            df[parcoord_dropdown],
            labels=columns,
        )
        storage = {str(i): v for i, v in enumerate(columns)}
        logger.info("parcoords columns: {}", storage)
        return parcoords, storage

    @app.callback(
        Output("parcoords_memory", "data"),
        Input("parcoords", "restyleData"),
        State("parcoords_memory", "data"),
    )
    def store_parcoord_style(restyle_data, data):
        if restyle_data is None:
            raise PreventUpdate
        if data is None:
            data = {}

        key = list(restyle_data[0].keys())[0]
        dim = re.match(r"dimensions\[(\d+)\].constraintrange", key).groups()[0]
        ranges = restyle_data[0][key][0]
        if isinstance(ranges[0], float):
            ranges = [ranges]
        data[dim] = ranges
        logger.info("Parallel Coordinates Style: {}", data)
        return data
