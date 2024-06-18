import socket
import psycopg2
from psycopg2 import sql

def historial_transacciones(user_id):
    try:
        conn = psycopg2.connect(
            dbname="Biblioteca", user="postgres", password="postgres", host="localhost", port="5444"
        )
        print("Conexión exitosa a la base de datos PostgreSQL.")
        cur = conn.cursor()
        query = """
            SELECT * FROM prestamos
            WHERE usuario_prestador_id = %s OR usuario_solicitante_id = %s
        """
        cur.execute(query, (user_id, user_id))
        transactions = cur.fetchall()
        cur.close()
        conn.close()
        return f"00015histOK{transactions}"
    except psycopg2.Error as e:
        return f"00015histNKError: {str(e)}"

def procesar_transaccion(transaccion):
    servicio = transaccion[5:10]
    datos = transaccion[10:]
    
    if servicio == "hist":
        user_id = datos
        return historial_transacciones(user_id)
    else:
        return f"{transaccion[:5]}{servicio}NKService not found"

def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    bus_address = ('localhost', 5000)
    print('connecting to {} port {}'.format(*bus_address))
    sock.connect(bus_address)

    try:
        # Inicializar la conexión al servicio de historial de transacciones
        message = '00010sinithist'.encode()
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
