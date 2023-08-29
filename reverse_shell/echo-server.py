import socket

HOST = "127.0.0.1" # loopback ip address (localhost)
PORT = 65432 # non priveleged port (> 1023)

#i have literally never seen a with loop lol
#args used to specify address family and socket type
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    #sock_stream is the socket type for TCP
    #AF_INET expects a two-tuple: (host, port)
    s.bind((HOST, PORT)) # socket -> bind -> listen -> accept
    s.listen()
    conn, addr = s.accept()
    with conn:
        print(f'Connected by {addr}')
        while True:
            data = conn.recv(1024)
            if not data:
                break
            conn.sendall(data)
#instead of using s.close(), end of loop = end of condition

