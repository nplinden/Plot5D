import dash_mantine_components as dmc
from dash_iconify import DashIconify
from dash import dcc

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


def header():
    return dmc.AppShellHeader(
        dmc.Group(
            [
                dmc.Group(
                    [
                        dmc.Burger(
                            id="burger",
                            size="sm",
                            hiddenFrom="sm",
                            opened=False,
                        ),
                        dmc.Title("Plot5D by Nicolas Linden", c="blue"),
                    ]
                ),
                dmc.Group(
                    [
                        dmc.ActionIcon(
                            DashIconify(icon="clarity:help-line", width=50),
                            variant="subtle",
                            size="sm",
                        ),
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