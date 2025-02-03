import dash_mantine_components as dmc
from dash import html, dcc
from components.text import helper
from components.settings import settings


def mainpanel():
    return dmc.AppShellMain(
        children=[
            dmc.Affix(
                dmc.Button("Download Selection", id="download-selection-btn"),
                position={"bottom": 20, "right": 20},
                style={"display": "none"},
                id="download-selection-affix",
            ),
            dcc.Download(id="download-selection"),
            dmc.Modal(
                title=helper["title"],
                children=helper["children"],
                id="helper-modal",
                size="60%",
            ),
            settings,
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
            dcc.Store(id="metadata-storage", storage_type="memory"),
            dcc.Store(id="mainplot-storage", storage_type="memory"),
            dcc.Graph(id="mainplot", style={"width": "90h", "height": "90vh", "display": "none"}, mathjax=True),
            dcc.Store(id="spider-storage", storage_type="memory"),
            dcc.Graph(id="spider", style={"width": "90h", "height": "90vh", "display": "none"}, mathjax=True),
        ]
    )
