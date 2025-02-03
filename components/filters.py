from dash import Input, Output, State, callback, Patch, ALL, dcc
from dash_iconify import DashIconify
import dash_mantine_components as dmc
from dash.exceptions import PreventUpdate


def filter_component(id):
    return (
        dmc.Select(
            placeholder="QOI",
            id={"type": "filter-slct", "index": id},
            data=[],
            mt="sm",
            searchable=True,
        ),
        dmc.NumberInput(placeholder="Min", mt="sm", id={"type": "filter-min", "index": id}),
        dmc.NumberInput(placeholder="Max", mt="sm", id={"type": "filter-max", "index": id}),
    )


@callback(
    Output("filter-stack", "children", allow_duplicate=True),
    Input("filter-plus", "n_clicks"),
    State("data-storage", "data"),
    prevent_initial_call=True,
)
def add_filter(n_clicks, data):
    if data is None:
        raise PreventUpdate
    select, plus, minus = filter_component(n_clicks)
    select.data = list(data[0].keys())
    patched_children = Patch()
    patched_children.append(dmc.Group(children=[select, plus, minus]))
    return patched_children


@callback(
    Output("filter-store", "data"),
    Input({"type": "filter-slct", "index": ALL}, "value"),
    Input({"type": "filter-min", "index": ALL}, "value"),
    Input({"type": "filter-max", "index": ALL}, "value"),
)
def get_filters(values, mins, maxs):
    if all(v is None for v in values):
        raise PreventUpdate
    return {k: {"min": mins[i], "max": maxs[i]} for (i, k) in enumerate(values)}


filters = [
    dmc.Stack([], align="left", gap="sm", id="filter-stack", mt="sm"),
    dcc.Store(id="filter-store", storage_type="memory"),
    dmc.Group(
        children=[
            dmc.ActionIcon(
                DashIconify(icon="clarity:minus-line", width=25), variant="subtle", size="lg", id="filter-minus"
            ),
            dmc.ActionIcon(
                DashIconify(icon="clarity:plus-line", width=25), variant="subtle", size="lg", id="filter-plus"
            ),
            # dmc.Button("Apply", id="filter-apply", color="blue"),
        ],
        mt="sm",
    ),
]
