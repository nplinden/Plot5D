import dash_mantine_components as dmc
from dash_iconify import DashIconify
from dash import dcc

colors = dmc.DEFAULT_THEME["colors"]

theme_toggle = dmc.ActionIcon(
    [
        DashIconify(
            icon="radix-icons:sun",
            width=25,
            id="light-theme-icon",
        ),
        DashIconify(
            icon="radix-icons:moon",
            width=25,
            id="dark-theme-icon",
        ),
    ],
    variant="transparent",
    color="yellow",
    id="color-scheme-toggle",
    size="lg",
)

navbar_toggle = dmc.ActionIcon(
    [
        DashIconify(
            icon="material-symbols:left-panel-close-rounded",
            width=25,
            id="navbar-closed-icon",
            style={"display": "block"},
        ),
        DashIconify(
            icon="material-symbols:left-panel-open-rounded", width=25, id="navbar-open-icon", style={"display": "none"}
        ),
    ],
    variant="transparent",
    id="navbar-toggle",
    size="lg",
)

helper = dmc.ActionIcon(DashIconify(icon="clarity:help-line", width=25), variant="subtle", size="lg", id="help")

settings = dmc.ActionIcon(
    DashIconify(icon="clarity:settings-line", width=25), variant="subtle", size="lg", id="settings"
)


def header():
    return dmc.AppShellHeader(
        dmc.Group(
            [
                dmc.Group(
                    [
                        dmc.Image(
                            src="assets/logo.png",
                            h="60",
                        ),
                        dmc.Title("by Nicolas Linden", c="blue"),
                    ]
                ),
                dmc.Group(
                    [
                        navbar_toggle,
                        settings,
                        helper,
                        dcc.Store(id="color-scheme-storage", storage_type="local"),
                        theme_toggle,
                    ]
                ),
            ],
            justify="space-between",
            style={"flex": 1},
            h="100%",
            px="md",
        ),
    )
