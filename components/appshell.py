import dash_mantine_components as dmc
from components.header import header
from components.navbar import navbar
from components.mainpanel import mainpanel


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
