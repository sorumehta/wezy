import socket
import select
import logging
from typing import List, Dict, Any, Optional

from buffer import Buffer

logger = logging.getLogger(__name__)


def process_ready_socket(ready: socket.socket, server: socket.socket, inputs: List[socket.socket],
                         outputs: List[socket.socket], conns: Dict[socket.socket, Optional[Buffer]]):
    # if s is our 'server' socket, it means a new client is waiting for us to accept connection
    if ready is server:
        connection, client_address = ready.accept()
        print(f"received new connection from {client_address}")
        connection.setblocking(False)
        inputs.append(connection)
        conns[connection] = None
    else:
        buf = conns[ready]
        if buf is None:
            buf = Buffer()
        buf.read_buffer() # does this even make sense?



def start_server(port: int) -> None:
    assert(isinstance(port, int))
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setblocking(False)
    print(f"starting the server on port {port}")
    server.bind(('', port))
    server.listen(5)
    connections = {}
    inputs = [server]
    outputs = []
    while True:
        print("event loop in wait mode, press CTRL-C to exit")
        # pass in server socket as input and exception, and empty output to select()
        readable_sock, writeable_sock, err_sock = select.select(inputs, outputs, inputs)
        for s in readable_sock:
            process_ready_socket(s, server, inputs, outputs)




start_server(10000)