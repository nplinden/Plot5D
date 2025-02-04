import dash_mantine_components as dmc
from dash import html, dcc
from components.text import helper
from components.settings import settings
from components.alias import alias
from components.filters import filters
import dash_ag_grid as dag

colors = dmc.DEFAULT_THEME["colors"]


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
            dcc.Store(id="data-storage", storage_type="memory"),
            dcc.Store(id="metadata-storage", storage_type="memory"),
            dmc.Tabs(
                [
                    dmc.TabsList(
                        [
                            dmc.TabsTab("Home", value="home"),
                            dmc.TabsTab("5DPlot", value="mainplot"),
                            dmc.TabsTab("SpiderPlot", value="spider"),
                            dmc.TabsTab("Table", value="table"),
                        ]
                    ),
                    dmc.TabsPanel(
                        children=[
                            dmc.Title("Data Upload", 3, mt="sm"),
                            dcc.Upload(
                                id="df_upload",
                                children=html.Div("Upload csv file"),
                                className="upload",
                                multiple=False,
                            ),
                            dmc.Title("State Management", 3, mt="sm"),
                            dmc.Group(
                                [
                                    dcc.Upload(
                                        id="state_upload",
                                        children=html.Div(
                                            dmc.Button(
                                                "Upload State File", mt="sm", fullWidth=True, color=colors["grape"][9]
                                            )
                                        ),
                                        multiple=False,
                                    ),
                                    dmc.Button(
                                        "Download State",
                                        mt="sm",
                                        color="blue",
                                        id="download-state-btn",
                                    ),
                                ]
                            ),
                            dmc.Title("Column Name Aliases", 3, mt="sm"),
                            *alias,
                            dcc.Download(id="download-state"),
                            dmc.LoadingOverlay(
                                visible=False,
                                id="loading-overlay",
                                overlayProps={"radius": "sm", "blur": 2},
                                zIndex=10,
                            ),
                            dmc.Title("Data Filters", 3, mt="sm"),
                            *filters,
                        ],
                        value="home",
                    ),
                    dmc.TabsPanel(
                        children=[
                            dcc.Store(id="mainplot-storage", storage_type="memory"),
                            dcc.Store(id="mainplot-selection-storage", storage_type="memory"),
                            dcc.Graph(
                                id="mainplot", style={"width": "90h", "height": "90vh", "display": "none"}, mathjax=True
                            ),
                        ],
                        value="mainplot",
                    ),
                    dmc.TabsPanel(
                        children=[
                            dcc.Store(id="spider-storage", storage_type="memory"),
                            dcc.Store(id="spider-selection-storage", storage_type="memory"),
                            dcc.Graph(
                                id="spider", style={"width": "90h", "height": "90vh", "display": "none"}, mathjax=True
                            ),
                        ],
                        value="spider",
                    ),
                    dmc.TabsPanel(
                        children=[
                            dag.AgGrid(
                                id="table", className="ag-theme-quartz-dark", dashGridOptions={"pagination": True}
                            )
                        ],
                        value="table",
                    ),
                ],
                id="tabs",
                color="orange",  # default is blue
                orientation="horizontal",  # or "vertical"
                variant="default",  # or "outline" or "pills"
                value="home",
            ),
        ]
    )
