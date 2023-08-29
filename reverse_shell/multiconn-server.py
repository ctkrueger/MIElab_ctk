import sys
import socket
import selectors # .select() to handle multiple connections simultaneously
import types

sel = selectors.DefaultSelector() # selector object

# ...

def accept_wrapper(sock):
    conn, addr = sock.accept() # Should be ready to read
    print(f'Accepted connection from addr: {addr}')
    conn.setblocking(False) # put socket into non-blocking mode
    data = types.SimpleNamespace(addr=addr, inb=b"", outb=b"")
    events = selectors.EVENT_READ | selectors.EVENT_WRITE # bitwise or
    sel.register(conn, events, data=data)

# ...

def service_connection(key, mask):
    sock = key.fileobj
    data = key.data
    if mask & selectors.EVENT_READ: # this is called when the socket is ready for reading
        recv_data = sock.recv(1024) # Should be ready to read 
        if recv_data:
            data.outb += recv_data
        else: # if no data received, client socket assumed to be closed, closing server
            print(f'Closing connection to {data.addr}')
            sel.unregister(sock) # remember to unregister before closing
            sock.close()
    if mask & selectors.EVENT_WRITE: # this is called when the socket is ready for writing
        if data.outb: # wont this just send back exactly what is already being received???
            print(f'Echoing {data.outb!r} to {data.addr}')
            sent = sock.send(data.outb) # should be ready to write
            data.outb = data.outb[sent:] #updates the data.outb to exclude what has already been sent

# ...

host, port = sys.argv[1], int(sys.argv[2])
lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
lsock.bind((host, port))
lsock.listen()
print(f'Listening on host: {host}, port: {port}')
lsock.setblocking(False) # calls made to this socket will no longer block
# can wait for events on >=1 socket and then read + write data when its ready
sel.register(lsock, selectors.EVENT_READ, data=None) # registering the object with lsock, want read events for listening socket

# ...

try:
    while True: #infinite loop
        events = sel.select(timeout=None) # returns list of tuples which contain key and mask
        for key, mask in events:
            if key.data is None:
                accept_wrapper(key.fileobj)
            else:
                service_connection(key, mask)
except KeyboardInterrupt:
    print("Caught keyboard interrupt, exiting")
finally:
    sel.close()



