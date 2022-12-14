import socket
import select
import logging
import time
from typing import List, Dict, Optional
from constants import MAX_BUFFER_TRIES, MAX_REQUEST_SIZE, MAX_REQUEST_AGE
from buffer import Buffer
from request import Request
from handler_table import find_handler
from utils import get_status_message
logger = logging.getLogger(__name__)


def return_error(status_code: int, sock: socket.socket, conns: Dict[socket.socket, Buffer]):
    buf = conns[sock]
    buf.write_response(response_code=status_code, body=get_status_message(status_code),response_headers=[])


def handle_request(sock: socket.socket, request: Request, conns: Dict[socket.socket, Buffer]):
    handler, path_params = find_handler(request.http_method, request.resource)
    if handler is None:
        return_error(404, sock, conns)
        return
    else:
        result = handler(request)
    if not result:
        result = {}
    body = result.get("body") or ""
    status = result.get("status") or 200
    headers = result.get("headers") or []
    buf = conns[sock]
    buf.write_response(response_code=status, body=body, response_headers=headers)


def process_ready_socket(ready: socket.socket, server: socket.socket, inputs: List[socket.socket],
                         outputs: List[socket.socket], conns: Dict[socket.socket, Optional[Buffer]]):
    # if our 'server' socket is ready, it means a new client is waiting for us to accept connection
    if ready is server:
        connection, client_address = ready.accept()
        print(f"received new connection from {client_address}")
        connection.setblocking(False)
        inputs.append(connection)
        conns[connection] = None
    else:
        data = ready.recv(2048)
        data = data.decode('utf-8')
        if conns[ready] is None:
            conns[ready] = Buffer()
        buf = conns[ready]
        buf.stream_data = data
        if buf.process_buffer() == "EOF!":
            print(f"connection closed by client")
            if ready in outputs:
                outputs.remove(ready)
            inputs.remove(ready)
            del conns[ready]
            ready.close()
        else:
            no_output = False
            too_big = buf.total_buffered > MAX_REQUEST_SIZE
            too_old = time.time() - buf.start_time > MAX_REQUEST_AGE
            too_needy = buf.n_tries > MAX_BUFFER_TRIES
            if too_big:
                return_error(413, ready, conns)
                inputs.remove(ready)
            elif too_old or too_needy:
                print(f"request too_old: {too_old} or too_needy: {too_needy}, error 400")
                return_error(400, ready, conns)
                inputs.remove(ready)
            elif buf.request:
                try:
                    handle_request(ready, buf.request, conns)
                except Exception as e:
                    logger.exception(e)
                    return_error(500, ready, conns)

            else:
                no_output = True
            # add output channel for response
            if (not no_output) and ready not in outputs:
                outputs.append(ready)


def process_outgoing_socket(out_sock: socket.socket, inputs: List[socket.socket], outputs: List[socket.socket], connections: Dict[socket.socket, Buffer]):
    buf = connections[out_sock]
    if buf.response:
        response = buf.response.build_response_str()
        out_sock.send(response.encode())

    out_sock.close()
    outputs.remove(out_sock)
    if out_sock in inputs:
        inputs.remove(out_sock)


def start_server(port: int) -> None:
    assert(isinstance(port, int))
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.setblocking(False)
    print(f"starting the server on port {port}")
    server.bind(('', port))
    server.listen(5)
    connections = {}
    inputs = [server]
    outputs = []
    while inputs:
        print("event loop in wait mode, press CTRL-C to exit")
        # pass in server socket as input and exception, and empty output to select()
        readable_sock, writeable_sock, err_sock = select.select(inputs, outputs, inputs)
        for s in readable_sock:
            process_ready_socket(s, server, inputs, outputs, connections)
        for s in writeable_sock:
            process_outgoing_socket(s, inputs, outputs, connections)
        for s in err_sock:
            print(f"error in sock: {s}")
            inputs.remove(s)
            if s in outputs:
                outputs.remove(s)
            s.close()
            if s in connections:
                del connections[s]
    print("shutting down web server...")
    for c in connections:
        c.close()
    server.close()


start_server(10000)