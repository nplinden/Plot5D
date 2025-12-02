import dash_mantine_components as dmc
from dash import dcc

colors = dmc.DEFAULT_THEME["colors"]

mainplot_navbar = dmc.Box(
    children=[
        dmc.Title("5DPlot Selection", 3, mt="sm"),
        dmc.Select(label="Row", placeholder="Discrete Valued QOI", id="row-slct", data=[], mt="sm", searchable=True),
        dmc.MultiSelect(placeholder="Values", id="row-value-slct", data=[], mt="sm", searchable=True),
        dmc.Select(label="Column", placeholder="Discrete Valued QOI", id="col-slct", data=[], mt="sm", searchable=True),
        dmc.MultiSelect(placeholder="Values", id="col-value-slct", data=[], mt="sm", searchable=True),
        dmc.Select(label="X", placeholder="QOI", id="x-slct", data=[], mt="sm", searchable=True),
        dmc.Select(label="Y", placeholder="QOI", id="y-slct", data=[], mt="sm", searchable=True),
        dmc.Select(label="Color", placeholder="QOI", id="color-slct", data=[], mt="sm", searchable=True),
    ],
    id="mainplot-navbar",
)

spider_navbar = dmc.Box(
    children=[
        dmc.Title("Spider Selection", 3, mt="sm"),
        dmc.MultiSelect(
            label="Spider Columns", placeholder="Columns", id="spider-slct", data=[], mt="sm", searchable=True
        ),
        dcc.Store(id="spider-slct-memory", storage_type="memory"),
        dcc.Store(id="spider-filters-memory", storage_type="memory"),
    ],
    id="spider-navbar",
)


def navbar():
    return dmc.AppShellNavbar(
        id="navbar",
        children=dmc.ScrollArea(
            [mainplot_navbar, spider_navbar],
            id="navbar-scroll-area",
        ),
        p="md",
    )
