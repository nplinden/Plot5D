import dash_mantine_components as dmc
from dash import html, dcc

colors = dmc.DEFAULT_THEME["colors"]


def navbar():
    return dmc.AppShellNavbar(
        id="navbar",
        children=dmc.ScrollArea(
            [
                "",
                dcc.Upload(
                    id="state_upload",
                    children=html.Div(
                        dmc.Button("Upload State File", mt="sm", fullWidth=True, color=colors["grape"][9])
                    ),
                    multiple=False,
                ),
                dmc.Button(
                    "Download State",
                    mt="sm",
                    color="blue",
                    w="100%",
                    id="download-state-btn",
                ),
                dcc.Download(id="download-state"),
                dmc.Select(
                    label="Row", placeholder="Discrete Valued QOI", id="row-slct", data=[], mt="sm", searchable=True
                ),
                dmc.MultiSelect(placeholder="Values", id="row-value-slct", data=[], mt="sm", searchable=True),
                dmc.Select(
                    label="Column", placeholder="Discrete Valued QOI", id="col-slct", data=[], mt="sm", searchable=True
                ),
                dmc.MultiSelect(placeholder="Values", id="col-value-slct", data=[], mt="sm", searchable=True),
                dmc.Select(label="X", placeholder="QOI", id="x-slct", data=[], mt="sm", searchable=True),
                dmc.Select(label="Y", placeholder="QOI", id="y-slct", data=[], mt="sm", searchable=True),
                dmc.Select(label="Color", placeholder="QOI", id="color-slct", data=[], mt="sm", searchable=True),
                dmc.MultiSelect(
                    label="Spider Columns", placeholder="Columns", id="spider-slct", data=[], mt="sm", searchable=True
                ),
                dcc.Store(id="spider-slct-memory", storage_type="memory"),
                dcc.Store(id="spider-filters-memory", storage_type="memory"),
                dmc.Button(
                    "Add Filter",
                    mt="sm",
                    color="grape",
                    w="100%",
                    id="add-filter-btn",
                ),
                html.Div(id="filter-div", children=[]),
                dcc.Store(id="filter-store", storage_type="memory"),
            ],
            id="navbar-scroll-area",
        ),
        p="md",
    )
