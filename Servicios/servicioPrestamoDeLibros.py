import socket
import psycopg2
from psycopg2 import sql
from datetime import datetime

def prestar_libro(usuario_prestador_id, usuario_solicitante_id, ISBN, fecha_devolucion):
    try:
        conn = psycopg2.connect(
            dbname="Biblioteca", user="postgres", password="postgres", host="localhost", port="5444"
        )
        print("Conexión exitosa a la base de datos PostgreSQL.")
        cur = conn.cursor()
        fecha_prestamo = datetime.now()
        query = """
            INSERT INTO prestamos (usuario_prestador_id, usuario_solicitante_id, ISBN, fecha_prestamo, fecha_devolucion)
            VALUES (%s, %s, %s, %s, %s) RETURNING prestamo_id
        """
        cur.execute(query, (usuario_prestador_id, usuario_solicitante_id, ISBN, fecha_prestamo, fecha_devolucion))
        prestamo_id = cur.fetchone()[0]
        conn.commit()
        cur.close()
        conn.close()
        return f"00015loanOK{prestamo_id}"
    except psycopg2.Error as e:
        return f"00015loanNKError: {str(e)}"

def procesar_transaccion(transaccion):
    servicio = transaccion[5:10]
    datos = transaccion[10:].split(' ')
    
    if servicio == "loan":
        usuario_prestador_id, usuario_solicitante_id, ISBN, fecha_devolucion = datos
        return prestar_libro(usuario_prestador_id, usuario_solicitante_id, ISBN, fecha_devolucion)
    else:
        return f"{transaccion[:5]}{servicio}NKService not found"

def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    bus_address = ('localhost', 5000)
    print('connecting to {} port {}'.format(*bus_address))
    sock.connect(bus_address)

    try:
        # Inicializar la conexión al servicio de préstamos
        message = '00010sinitloan'.encode()
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
