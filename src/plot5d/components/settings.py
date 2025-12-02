import dash_mantine_components as dmc
from dash import dcc

settings = dmc.Modal(
    title="Settings",
    children=[
        dcc.Download(id="download-sample"),
        dmc.Text("Download Sample data"),
        dmc.Group(
            grow=True,
            wrap="nowrap",
            children=[
                dmc.NumberInput(
                    placeholder="Lines",
                    id="download-sample-lines",
                ),
                dmc.Button(
                    "Download",
                    color="grape",
                    id="download-sample-btn",
                ),
            ],
        ),
    ],
    id="settings-modal",
    size="60%",
)
