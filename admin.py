
import socket
import sys

def conectar_servidor():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = ('localhost', 5000)
    print(f'Conectando a {server_address[0]} puerto {server_address[1]}')
    sock.connect(server_address)
    return sock

def enviar_transaccion(transaccion):
    sock = conectar_servidor()
    try:
        print(f'Enviando transacción: {transaccion}')
        sock.sendall(transaccion.encode())

        # Recibir respuesta
        amount_expected = int(sock.recv(5).decode())
        data = b''
        while len(data) < amount_expected:
            chunk = sock.recv(amount_expected - len(data))
            data += chunk

        respuesta = data.decode()
        print(f'Respuesta recibida: {respuesta}')
        return respuesta
    finally:
        sock.close()

def crear_usuario(username, password, email, role='Cliente'):
    servicio = "adm01"
    datos = f"{username} {password} {email} {role}"
    longitud = f"{len(servicio + datos):05d}"
    transaccion = longitud + servicio + datos
    return enviar_transaccion(transaccion)

def actualizar_usuario(username, password=None, email=None, role=None):
    servicio = "adm02"
    datos = f"{username}"
    if password:
        datos += f" {password}"
    if email:
        datos += f" {email}"
    if role:
        datos += f" {role}"
    longitud = f"{len(servicio + datos):05d}"
    transaccion = longitud + servicio + datos
    return enviar_transaccion(transaccion)

def eliminar_usuario(username):
    servicio = "adm03"
    datos = f"{username}"
    longitud = f"{len(servicio + datos):05d}"
    transaccion = longitud + servicio + datos
    return enviar_transaccion(transaccion)

def restablecer_contrasena(username):
    servicio = "adm04"
    datos = f"{username}"
    longitud = f"{len(servicio + datos):05d}"
    transaccion = longitud + servicio + datos
    return enviar_transaccion(transaccion)

def main():
    print("Bienvenido, Administrador!")
    while True:
        print("\nOpciones:")
        print("1. Crear usuario")
        print("2. Actualizar usuario")
        print("3. Eliminar usuario")
        print("4. Restablecer contraseña")
        print("5. Salir")
        opcion = input("Selecciona una opción: ")

        if opcion == '1':
            username = input("Introduce el nombre de usuario: ")
            password = input("Introduce la contraseña: ")
            email = input("Introduce el email: ")
            role = input("Introduce el rol (Cliente/Administrador): ")
            respuesta = crear_usuario(username, password, email, role)
            print(f"Respuesta del servidor: {respuesta}")
        elif opcion == '2':
            username = input("Introduce el nombre de usuario: ")
            password = input("Introduce la nueva contraseña (deja en blanco para no cambiar): ")
            email = input("Introduce el nuevo email (deja en blanco para no cambiar): ")
            role = input("Introduce el nuevo rol (deja en blanco para no cambiar): ")
            respuesta = actualizar_usuario(username, password or None, email or None, role or None)
            print(f"Respuesta del servidor: {respuesta}")
        elif opcion == '3':
            username = input("Introduce el nombre de usuario: ")
            respuesta = eliminar_usuario(username)
            print(f"Respuesta del servidor: {respuesta}")
        elif opcion == '4':
            username = input("Introduce el nombre de usuario: ")
            respuesta = restablecer_contrasena(username)
            print(f"Respuesta del servidor: {respuesta}")
        elif opcion == '5':
            break
        else:
            print("Opción no válida. Inténtalo de nuevo.")

if __name__ == "__main__":
    main()
