import socket
import psycopg2
from psycopg2 import sql

def registrar_usuario(nombre_usuario, contraseña):
    try:
        conn = psycopg2.connect(
            dbname="Biblioteca", user="postgres", password="postgres", host="localhost", port="5444"
        )
        print("Conexión exitosa a la base de datos PostgreSQL.")
        cur = conn.cursor()
        query = sql.SQL("INSERT INTO usuarios (username, password) VALUES (%s, %s)")
        cur.execute(query, (nombre_usuario, contraseña))
        conn.commit()
        cur.close()
        conn.close()
        return f"00021regisOKUsuario {nombre_usuario} registrado correctamente"
    except psycopg2.Error as e:
        return f"00022regisNKError al registrar usuario: {str(e)}"

def procesar_transaccion(transaccion):
    servicio = transaccion[0:5]
    datos = transaccion[5:]

    if servicio == "regis":
        username, password = datos.split(' ', 1)
        return registrar_usuario(username, password)
    else:
        return f"{transaccion[:5]}{servicio}NKService not found"

def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    bus_address = ('localhost', 5000)
    print('connecting to {} port {}'.format(*bus_address))
    sock.connect(bus_address)

    try:
        message = b'00010sinitregis'
        print('sending {!r}'.format(message))
        sock.sendall(message)
        sinit = 1

        while True:
            print("Waiting for transaction")
            amount_received = 0
            amount_expected = int(sock.recv(5))
            while amount_received < amount_expected:
                data = sock.recv(amount_expected - amount_received)
                amount_received += len(data)
            print("Checking store answer ...")
            transaccion = data.decode()
            if sinit == 1:
                sinit = 0
                print('Received sinit answer')
            else:
                print("Processing transaction...")
                respuesta = procesar_transaccion(transaccion)
                print("Send answer")
                print('sending {!r}'.format(respuesta))
                sock.sendall(respuesta.encode())
    finally:
        print('closing socket')
        sock.close()

if __name__ == "__main__":
    main()
