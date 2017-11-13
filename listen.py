import socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((socket.gethostname(), 8080))
sock.listen(10)
conn, addr = sock.accept()

while True:
    data = b''
    while True:
        more = conn.recv(1)
        if not more or more == b'\0':
            break
        print(more)
        data += more

    print("RECEIVED:", data)
    print(type(data))

    import forwardparser as fp
    import parser as p
    from simplify import simplify
    from reverseparse import toString, encode
    
    transformed = fp.parse(data)
    print(transformed)
    
    parsed = p.parse(transformed)
    print(parsed)
    
    evaluated = simplify(parsed)
    print(evaluated)
    
    transformed = toString(evaluated)
    print(transformed)
    
    conn.send(encode(transformed)+b'\0')
    sock.close()
