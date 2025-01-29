import dash_mantine_components as dmc
from dash import html, dcc


def navbar():
    return dmc.AppShellNavbar(
        id="navbar",
        children=dmc.ScrollArea(
            [
                "",
                dcc.Upload(
                    id="state_upload",
                    children=html.Div(dmc.Button("Upload State File", mt="sm", fullWidth=True)),
                    multiple=False,
                ),
                dmc.Button(
                    "Download State",
                    mt="sm",
                    color="grape",
                    w="100%",
                    id="download-state-btn",
                ),
                dcc.Download(id="download-state"),
                dmc.Select(
                    label="Row",
                    placeholder="Discrete Valued QOI",
                    id="row-slct",
                    data=[],
                    mt="sm",
                ),
                dmc.MultiSelect(placeholder="Values", id="row-value-slct", data=[], mt="sm"),
                dmc.Select(
                    label="Column",
                    placeholder="Discrete Valued QOI",
                    id="col-slct",
                    data=[],
                    mt="sm",
                ),
                dmc.MultiSelect(placeholder="Values", id="col-value-slct", data=[], mt="sm"),
                dmc.Select(label="X", placeholder="QOI", id="x-slct", data=[], mt="sm"),
                dmc.Group(
                    grow=True,
                    wrap="nowrap",
                    children=[
                        dmc.NumberInput(placeholder="Min", mt="sm", id="x-min"),
                        dmc.NumberInput(placeholder="Max", mt="sm", id="x-max"),
                    ],
                ),
                dmc.Select(label="Y", placeholder="QOI", id="y-slct", data=[], mt="sm"),
                dmc.Group(
                    grow=True,
                    wrap="nowrap",
                    children=[
                        dmc.NumberInput(placeholder="Min", mt="sm", id="y-min"),
                        dmc.NumberInput(placeholder="Max", mt="sm", id="y-max"),
                    ],
                ),
                dmc.Select(
                    label="Color",
                    placeholder="QOI",
                    id="color-slct",
                    data=[],
                    mt="sm",
                ),
                dmc.Group(
                    grow=True,
                    wrap="nowrap",
                    children=[
                        dmc.NumberInput(placeholder="Min", mt="sm", id="color-min"),
                        dmc.NumberInput(placeholder="Max", mt="sm", id="color-max"),
                    ],
                ),
                dmc.MultiSelect(
                    label="Spider Columns",
                    placeholder="Columns",
                    id="spider-slct",
                    data=[],
                    mt="sm",
                ),
                dcc.Store(id="spider-slct-memory", storage_type="memory"),
                dcc.Store(id="spider-filters-memory", storage_type="memory"),
            ]
        ),
        p="md",
    )
