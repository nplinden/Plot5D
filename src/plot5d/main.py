import socket

import click
import dash
from dash import Dash

from plot5d.callbacks import *
from plot5d.components.appshell import appshell


def get_free_port():
    # Create a temporary socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        # Bind to port 0 tells OS to find an available port
        s.bind(("", 0))
        # Get the port number assigned by the OS
        return s.getsockname()[1]


@click.command()
@click.option("--debug", "-d", is_flag=True, help="Run the Flask app in debug mode")
def main(debug: bool) -> None:
    dash._dash_renderer._set_react_version("18.2.0")

    app = Dash(
        __name__,
        title="Plot5D",
        external_scripts=["https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.5/MathJax.js?config=TeX-MML-AM_CHTML"],
    )
    app.layout = appshell()
    port = get_free_port()

    app.run(debug=debug, port=port, host="0.0.0.0")
