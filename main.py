from plot5d.cli import parser
from plot5d.app import app
import socket

def get_port():
    sock = socket.socket()
    sock.bind(('', 0))
    return sock.getsockname()[1]


if __name__ == "__main__":
    args = parser.parse_args()
    if args.port is None:
        port = get_port()
    else:
        port = args.port
    app.run(debug=True, port=port)
