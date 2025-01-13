from dash import html
import dash_bootstrap_components as dbc


def menu(title, components=None, col=False):
    if components is None:
        components = []
    if col:
        menu_component = dbc.Col(
            html.Div(
                [html.Div(title, className="menu-title"), *components],
                className="menu-div",
            ),
            className="col-menu",
        )
    else:
        menu_component = html.Div([html.Div(title, className="menu-title"), *components], className="menu-div")
    return menu_component
