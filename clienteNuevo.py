import socket
import sys

def login():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    login_address = ('localhost', 5000)  # Conectar al servicio de login en el puerto 5001
    print('connecting to {} port {}'.format(*login_address))
    sock.connect(login_address)

    try:
        while True:
            username = input("Username: ")
            password = input("Password: ")
            login_message = f"{len(username) + len(password) + 1:05}login{username} {password}"
            print(login_message)
            sock.sendall(login_message.encode())
            amount_expected = int(sock.recv(5).decode())
            data = b''
            amount_received = 0
            while amount_received < amount_expected:
                chunk = sock.recv(amount_expected - amount_received)
                data += chunk
                amount_received += len(chunk)
            response = data.decode()
            print(f"Login response: {response}")
            if "loginOKOK" in response:
                print("Login successful!")
                return True
            else:
                print("Login failed. Please try again.")
    finally:
        sock.close()

def main():
    if not login():
        print("Failed to login. Exiting...")
        return

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    bus_address = ('localhost', 5000)
    print('connecting to {} port {}'.format(*bus_address))
    sock.connect(bus_address)

    try:
        while True:
            if input('Send Hello world to servi ? y/n: ') != 'y':
                break
            message = b'00016serviHello world'
            print('sending {!r}'.format(message))
            sock.sendall(message)
            print("Waiting for transaction")
            amount_received = 0
            amount_expected = int(sock.recv(5).decode())
            data = b''
            while amount_received < amount_expected:
                chunk = sock.recv(amount_expected - amount_received)
                data += chunk
                amount_received += len(chunk)
            print("Checking servi answer ...")
            print(f"received {data}")
    finally:
        print('closing socket')
        sock.close()

if __name__ == "__main__":
    main()
