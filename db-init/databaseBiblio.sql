
-- Conectarse a la base de datos
\c Biblioteca;

-- Crear la tabla de administradores
CREATE TABLE UsuarioAdministrador (
    usuario_id SERIAL PRIMARY KEY,
    primer_nombre VARCHAR(20) NOT NULL,
    apellido VARCHAR(20) NOT NULL,
    email VARCHAR(50) NOT NULL UNIQUE,
    password VARCHAR(50) NOT NULL,
    rol VARCHAR(20) DEFAULT 'Administrador' NOT NULL
);

-- Crear la tabla de usuarios clientes
CREATE TABLE usuario (
    usuario_id SERIAL PRIMARY KEY,
    primer_nombre VARCHAR(20) NOT NULL,
    apellido VARCHAR(20) NOT NULL,
    email VARCHAR(50) NOT NULL UNIQUE,
    direccion VARCHAR(50),
    password VARCHAR(50) NOT NULL,
    celular VARCHAR(20)
);

-- Crear la tabla de libros
CREATE TABLE Libros (
    ISBN NUMERIC(13) PRIMARY KEY,
    titulo VARCHAR(100) NOT NULL,
    autor VARCHAR(50) NOT NULL,
    genero VARCHAR(30),
    descripcion TEXT
);

-- Crear la tabla de detalle de biblioteca
CREATE TABLE BibliotecaDetalle (
    biblioteca_id SERIAL PRIMARY KEY,
    usuario_id INT,
    ISBN NUMERIC(13),
    cantidad INT DEFAULT 1,
    FOREIGN KEY (usuario_id) REFERENCES UsuarioCliente(usuario_id),
    FOREIGN KEY (ISBN) REFERENCES Libros(ISBN)
);

-- Crear la tabla de préstamos
CREATE TABLE Prestamos (
    prestamo_id SERIAL PRIMARY KEY,
    usuario_prestador_id INT,
    usuario_solicitante_id INT,
    ISBN NUMERIC(13),
    fecha_prestamo TIMESTAMP NOT NULL,
    fecha_devolucion TIMESTAMP,
    FOREIGN KEY (usuario_prestador_id) REFERENCES UsuarioCliente(usuario_id),
    FOREIGN KEY (usuario_solicitante_id) REFERENCES UsuarioCliente(usuario_id),
    FOREIGN KEY (ISBN) REFERENCES Libros(ISBN)
);

-- Crear algunos índices para optimizar las consultas
CREATE INDEX idx_usuario_cliente_email ON UsuarioCliente(email);
CREATE INDEX idx_libros_titulo ON Libros(titulo);
CREATE INDEX idx_prestamos_fecha_prestamo ON Prestamos(fecha_prestamo);
