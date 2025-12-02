import socket
import os
import dash
from dash import Dash
from plot5d.components.appshell import appshell
from plot5d.callbacks import *

import argparse as ap

def get_free_port():
    # Create a temporary socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        # Bind to port 0 tells OS to find an available port
        s.bind(('', 0))
        # Get the port number assigned by the OS
        return s.getsockname()[1]

dash._dash_renderer._set_react_version("18.2.0")

def main():
    parser = ap.ArgumentParser(prog="Plot5D", description="A plotting tool for your favorite dataframes")
    parser.add_argument("-p", "--port", help="A port for the debug server", type=int)
    parser.add_argument("-d", "--debug", help="Run Flask server in debug mode", action="store_true")

    app = Dash(
        __name__,
        title="Plot5D",
        external_scripts=["https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.5/MathJax.js?config=TeX-MML-AM_CHTML"],
    )
    app.layout = appshell()
    server = app.server

    args = parser.parse_args()
    if args.port is not None:
        port = args.port
    elif os.getenv("PORTTCP") is not None:
        port = os.getenv("PORTTCP")
    else:
        port = get_free_port()

    app.run(debug=args.debug, port=port, host="0.0.0.0")
