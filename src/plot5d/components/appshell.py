import dash_mantine_components as dmc

from plot5d.components.header import header
from plot5d.components.mainpanel import mainpanel
from plot5d.components.navbar import navbar


def appshell():
    return dmc.MantineProvider(
        id="provider",
        forceColorScheme="dark",
        children=[
            dmc.AppShell(
                [header(), navbar(), mainpanel()],
                header={"height": 60},
                padding="md",
                navbar={
                    "width": 300,
                    "breakpoint": "sm",
                    "collapsed": {"mobile": True},
                },
                id="appshell",
            )
        ],
    )
