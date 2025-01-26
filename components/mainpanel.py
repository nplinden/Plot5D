import dash_mantine_components as dmc
from dash import html, dcc, dash_table

table = dash_table.DataTable(
    id="table",
    page_current=0,
    page_size=12,
    page_action="custom",
    style_cell={"fontSize": 20, "font-familiy": "monospace"},
    sort_action="custom",
    sort_mode="single",
    sort_by=[],
    tooltip_duration=None,
    fill_width=False,
)


def mainpanel():
    return dmc.AppShellMain(
        children=[
            dcc.Upload(
                id="df_upload",
                children=html.Div("Upload csv file"),
                className="upload",
                multiple=False,
            ),
            dmc.LoadingOverlay(
                visible=False,
                id="loading-overlay",
                overlayProps={"radius": "sm", "blur": 2},
                zIndex=10,
            ),
            dcc.Store(id="storage", storage_type="memory"),
            dcc.Store(id="mainplot-storage", storage_type="memory"),
            dcc.Graph(
                id="mainplot",
                # className="graph",
                style={"width": "90h", "height": "90vh", "display": "none"},
            ),
            dcc.Store(id="spider-storage", storage_type="memory"),
            dcc.Graph(
                id="spider",
                # className="graph",
                style={"width": "90h", "height": "90vh", "display": "none"},
            ),
            dmc.Center(style={"width": "100%"}, children=[table], mt="sm", id="table-center"),
        ]
    )
