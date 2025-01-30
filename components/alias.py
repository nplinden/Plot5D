import dash_mantine_components as dmc
from dash_iconify import DashIconify
from dash import callback, Input, Output, State, Patch, dcc, ALL
from dash.exceptions import PreventUpdate


def new_alias(id, select_data):
    selector = dmc.Select(
        label=None,
        placeholder="Column",
        id={"type": "alias-slct", "index": id},
        data=select_data,
        searchable=True,
    )
    text = dmc.TextInput(label=None, placeholder="Alias", id={"type": "alias-text", "index": id})
    group = dmc.Group(children=[selector, text])
    return group


@callback(
    Output("alias-stack", "children", allow_duplicate=True),
    Output("alias-rows-store", "data", allow_duplicate=True),
    Input("alias-plus", "n_clicks"),
    State("storage", "data"),
    State("alias-rows-store", "data"),
    prevent_initial_call=True,
)
def add_alias(n_clicks, data, rows_storage):
    if data is None:
        raise PreventUpdate
    if rows_storage is None:
        rows_storage = {"length": 0}
    rows_storage["length"] += 1
    keys = list(data[0].keys())
    patched_children = Patch()
    patched_children.append(new_alias(id=rows_storage["length"], select_data=keys))
    return patched_children, rows_storage


@callback(
    Output("alias-stack", "children", allow_duplicate=True),
    Output("alias-rows-store", "data", allow_duplicate=True),
    Input("alias-minus", "n_clicks"),
    State("alias-rows-store", "data"),
    prevent_initial_call=True,
)
def remove_alias(n_clicks, rows_storage):
    patched_children = Patch()
    del patched_children[-1]
    rows_storage["length"] -= 1
    return patched_children, rows_storage


@callback(
    Output("alias-store", "data"),
    Input("alias-modal", "opened"),
    State({"type": "alias-slct", "index": ALL}, "value"),
    State({"type": "alias-text", "index": ALL}, "value"),
    State("alias-store", "data"),
    prevent_initial_call=True,
)
def set_alias(opened, columns, aliases, alias_data):
    if opened:
        raise PreventUpdate
    if alias_data is None:
        alias_data = {}
    return {k: v for (k, v) in zip(columns, aliases)}


alias = {
    "title": "Add Custom Column Aliases",
    "children": [
        dmc.Stack([], align="center", gap="sm", id="alias-stack"),
        dcc.Store(id="alias-rows-store", storage_type="memory"),
        dcc.Store(id="alias-store", storage_type="memory", data={}),
        dmc.Center(
            children=[
                dmc.ActionIcon(
                    DashIconify(icon="clarity:minus-line", width=25), variant="subtle", size="lg", id="alias-minus"
                ),
                dmc.ActionIcon(
                    DashIconify(icon="clarity:plus-line", width=25), variant="subtle", size="lg", id="alias-plus"
                ),
            ],
            mt="sm",
        ),
    ],
}
