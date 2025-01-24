from plot5d.app import app
import socket
import argparse as ap

parser = ap.ArgumentParser(prog="Plot5D", description="A plotting tool for your favorite dataframes")
parser.add_argument("-p", "--port", help="A port for the debug server", type=int)


def get_port():
    sock = socket.socket()
    sock.bind(("", 0))
    return sock.getsockname()[1]


def main():
    args = parser.parse_args()
    if args.port is None:
        port = get_port()
    else:
        port = args.port
    app.run(debug=True, port=port)
