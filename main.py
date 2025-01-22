from plot5d.cli import parser
import os
from plot5d.app import app
import socket


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
