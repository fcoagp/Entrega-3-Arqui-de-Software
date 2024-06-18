import socket
import psycopg2
from psycopg2 import sql

def procesar_transaccion(transaccion):
    servicio = transaccion[5:10]
    datos = transaccion[10:]
    print(datos)
    if servicio == "store":
        nombre, valor = datos.split(' ', 1)
        return almacenar_datos(nombre, valor)
    elif servicio == "fetch":
        nombre = datos
        return obtener_datos(nombre)
    elif servicio == "updat":
        nombre, valor = datos.split(' ', 1)
        return actualizar_datos(nombre, valor)
    elif servicio == "delet":
        nombre = datos
        return eliminar_datos(nombre)
    else:
        return "00013" + servicio + "NKService not found"

def almacenar_datos(nombre, valor):
    try:
        conn = psycopg2.connect(
            dbname="Biblioteca", user="postgres", password="postgres", host="localhost", port="5444"
        )
        cur = conn.cursor()
        query = sql.SQL("INSERT INTO datos (nombre, valor) VALUES (%s, %s) RETURNING id")
        cur.execute(query, (nombre, valor))
        conn.commit()
        cur.close()
        conn.close()
        return f"00012storeOK{nombre} stored"
    except Exception as e:
        return f"00013storeNKError: {str(e)}"

def obtener_datos(nombre):
    try:
        conn = psycopg2.connect(
            dbname="servicio_db", user="postgres", password="password", host="localhost", port="5432"
        )
        if(nombre == '*'):
            cur = conn.cursor()
            query = sql.SQL("SELECT nombre, valor FROM datos")
            cur.execute(query)
            results = cur.fetchall()
            cur.close()
            conn.close()
            if results:
                resultados_str = ' '.join([f"{nombre}:{valor}" for nombre, valor in results])
                response_length = len(f"storeOK {resultados_str}")
                return f"{str(response_length).zfill(5)}storeOK {resultados_str}"
            else:
                return "00015storeNKNo data found"
        else:
            cur = conn.cursor()
            query = sql.SQL("SELECT valor FROM datos WHERE nombre = %s")
            cur.execute(query, (nombre,))
            result = cur.fetchone()
            cur.close()
            conn.close()
            if result:
                return f"00013storeOK{result[0]}"
            else:
                return f"00015storeNKNo data found"
    except Exception as e:
        return f"00013storeNKError: {str(e)}"


def eliminar_datos(nombre):
    try:
        conn = psycopg2.connect(
            dbname="servicio_db", user="postgres", password="password", host="localhost", port="5432"
        )
        print("Conexión exitosa a la base de datos PostgreSQL.")
        cur = conn.cursor()
        query = sql.SQL("DELETE FROM datos WHERE nombre = %s")
        cur.execute(query, (nombre,))
        conn.commit()
        cur.close()
        conn.close()
        return f"00014storeOK{nombre} eliminado"
    except psycopg2.Error as e:
        return f"00015storeNKError: {str(e)}"

def actualizar_datos(nombre, nuevo_valor):
    try:
        conn = psycopg2.connect(
            dbname="servicio_db", user="postgres", password="password", host="localhost", port="5432"
        )
        print("Conexión exitosa a la base de datos PostgreSQL.")
        cur = conn.cursor()
        query = sql.SQL("UPDATE datos SET valor = %s WHERE nombre = %s")
        cur.execute(query, (nuevo_valor, nombre))
        conn.commit()
        cur.close()
        conn.close()
        return f"00015storeOK{nombre} actualizado"
    except psycopg2.Error as e:
        return f"00016storeNKError: {str(e)}"


def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    bus_address = ('localhost', 5000)
    print('connecting to {} port {}'.format(*bus_address))
    sock.connect(bus_address)

    try:
        message = b'00010sinitstore'
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
            print('received {!r}'.format(data))
            transaccion = data.decode()
            print(transaccion)
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
