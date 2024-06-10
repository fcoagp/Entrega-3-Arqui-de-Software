import socket
import sys

def registrar():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    registro_address = ('localhost', 5000)  
    print('connecting to {} port {}'.format(*registro_address))
    sock.connect(registro_address)

    try:
        while True:
            username = input("Username: ")
            password = input("Password: ")

            # Crear mensaje de registro
            registro_message = f"{len(username) + len(password) + 2:05}regis{username} {password}"
            print(registro_message)
            sock.sendall(registro_message.encode())
            
            # Recibir respuesta del servicio de registro
            amount_expected = int(sock.recv(5).decode())
            data = b''
            amount_received = 0
            while amount_received < amount_expected:
                chunk = sock.recv(amount_expected - amount_received)
                data += chunk
                amount_received += len(chunk)
            
            response = data.decode()
            print(f"Registro response: {response}")
            if "regisOKOK" in response:
                print("Registro successful!")
                return True
            else:
                print("Registro failed. Please try again.")
    finally:
        sock.close()
    
def login():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    login_address = ('localhost', 5000) 
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


def enviar_transaccion(transaccion):
    bus_address = ('localhost', 5000)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(bus_address)

    try:
        # Enviar transacción
        print(f'Enviando transacción: {transaccion}')
        print(transaccion.encode())
        sock.sendall(transaccion.encode())

        # Recibir respuesta
        amount_received = 0
        amount_expected = int(sock.recv(5).decode())
        respuesta = b''
        while amount_received < amount_expected:
            data = sock.recv(amount_expected - amount_received)
            amount_received += len(data)
            respuesta += data

        print(f'Respuesta recibida: {respuesta.decode()}')
        return respuesta.decode()
    
    finally:
        print('Cerrando socket')
        sock.close()

def almacenar_datos(nombre, valor):
    servicio = "store"
    datos = f"{nombre} {valor}"
    longitud = f"{len(servicio + servicio + datos):05d}"
    transaccion = longitud + servicio + servicio + datos
    return enviar_transaccion(transaccion)

def actualizar_datos(nombre, valor):
    variable = "store"
    servicio = "updat"
    datos = f"{nombre} {valor}"
    longitud = f"{len(variable + servicio + datos):05d}"
    transaccion = longitud + variable + servicio + datos
    return enviar_transaccion(transaccion)

def obtener_datos(nombre):
    variable = "store"
    servicio = "fetch"
    datos = nombre
    longitud = f"{len(variable + servicio + datos):05d}"
    transaccion = longitud + variable + servicio + datos
    return enviar_transaccion(transaccion)

def eliminar_datos(nombre):
    variable = "store"
    servicio = "delet"
    datos = nombre
    longitud = f"{len(variable + servicio + datos):05d}"
    transaccion = longitud + variable + servicio + datos
    return enviar_transaccion(transaccion)

def main():

    print("Bienvenido!")
    print("1. Login")
    print("2. Registrar")

    opcion = input("Selecciona una opción: ")

    if opcion == '1':
        if not login():
            print("Failed to login. Exiting...")
            return
    elif opcion == '2':
        if not registrar():
            print("Failed to register. Exiting...")
            return
    else:
        print("Opción no válida. Saliendo...")
        return

    while True:
        print("\nOpciones:")
        print("1. Almacenar datos")
        print("2. Obtener datos")
        print("3. Actualizar datos")
        print("4. Eliminar datos")
        print("5. Salir")
        opcion = input("Selecciona una opción: ")

        if opcion == '1':
            nombre = input("Introduce el nombre: ")
            valor = input("Introduce el valor: ")
            respuesta = almacenar_datos(nombre, valor)
            print(f"Respuesta del servidor: {respuesta}")
        elif opcion == '2':
            nombre = input("Introduce el nombre: ")
            respuesta = obtener_datos(nombre)
            print(f"Respuesta del servidor: {respuesta}")
        elif opcion == '3':
                nombre = input("Ingrese nombre a actualizar: ")
                nuevo_valor = input("Ingrese valor nuevo: ")
                respuesta = actualizar_datos(nombre, nuevo_valor)
                print(f"Respuesta del servidor: {respuesta}")
        elif opcion == '4':
            nombre = input("Introduce el nombre: ")
            respuesta = eliminar_datos(nombre)
            print(f"Respuesta del servidor: {respuesta}")
        elif opcion == '5':
            break
        else:
            print("Opción no válida. Inténtalo de nuevo.")


if __name__ == "__main__":
    main()

