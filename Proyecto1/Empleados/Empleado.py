class Empleado:
    def __init__(self, codigo, nombre, puesto):
        self.codigo = codigo
        self.nombre = nombre
        self.puesto = puesto

    def __str__(self):
        return f'Codigo: {self.codigo}\\n' \
               f'Nombre: {self.nombre}\\n' \
               f'Puesto: {self.puesto}'
       