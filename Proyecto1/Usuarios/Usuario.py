class Usuario:
    def __init__ (self, usuario, contrasena, nombre, edad, email, telefono):
        self.usuario = usuario
        self.contrasena = contrasena
        self.nombre = nombre
        self.edad = edad
        self.email = email
        self.telefono = telefono

    def __str__(self):
        return f'Usuario: {self.usuario}\\n' \
               f'Contraseña: {self.contrasena}\\n' \
               f'Nombre: {self.nombre}\\n' \
               f'Edad: {self.edad}\\n' \
               f'Email: {self.email}\\n' \
               f'Telefono: {self.telefono}' 
