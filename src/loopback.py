import socket, threading, time

HOST = '127.0.0.1' # Standard loopback (localhost)
PORT = 65432

class Server():

    '''
    Starts up the Server, polls on listen for any received data.
    Times out if no data is received for X seconds
    '''
    def start(socket, timeout):
        socket.bind((HOST, PORT))
        socket.listen()
        conn, addr = socket.accept()
        print(f"Server started with address {addr}")
        with conn:
            conn.settimeout(timeout)
            while True:
                try:
                    data = conn.recv(1024)
                    if not data:
                        break
                    conn.sendall(data)
                except Exception as e:
                    print(f"An error occurred: {e}")
                    break

        print("Server shutting down")

class Client:
        
    '''
    Connects to socket, sends data, then prints out the received data
    '''
    def send_and_receive(socket):
        socket.connect((HOST, PORT))
        send_bytes = b"Hello, world"
        for _ in range(3):
            socket.sendall(send_bytes)
            print(f"Client: Sent {send_bytes.decode()}")
            data = socket.recv(1024)
            print(f"Client: Received {data.decode()}")
            time.sleep(2)


if __name__ == "__main__":
    # Create separate sockets for server and client
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server_timeout = 3
    server_thread = threading.Thread(target=Server.start, args=[server_socket, server_timeout])
    client_thread = threading.Thread(target=Client.send_and_receive, args=[client_socket])
    
    server_thread.start()
    client_thread.start()
    
    #import pdb;pdb.set_trace()
    client_thread.join()
    server_thread.join()