import os
import dash
from dash import Dash
import socket
from components.appshell import appshell
from callbacks import *

import argparse as ap

dash._dash_renderer._set_react_version("18.2.0")

parser = ap.ArgumentParser(prog="Plot5D", description="A plotting tool for your favorite dataframes")
parser.add_argument("-p", "--port", help="A port for the debug server", type=int)

app = Dash(
    __name__,
)
app.layout = appshell()
server = app.server


def get_port():
    sock = socket.socket()
    sock.bind(("", 0))
    return sock.getsockname()[1]


if __name__ == "__main__":
    args = parser.parse_args()
    # Vérifier si la variable d'environnement PORTTCP est définie
    port_env = os.getenv("PORTTCP")
    if port_env is not None:
        port = int(port_env)
    elif args.port is None:
        port = get_port()
    else:
        port = args.port

    # Lancer l'application
    app.run(debug=True, port=port, host="0.0.0.0")
