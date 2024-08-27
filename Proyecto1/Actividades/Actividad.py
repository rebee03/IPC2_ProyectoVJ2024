class Actividad:
    def __init__(self, id, nombre, descripcion, empleado, dia, hora):
        self.id = id
        self.nombre = nombre
        self.descripcion = descripcion
        self.empleado = empleado
        self.dia = dia
        self.hora = hora

    def __str__(self):
        return f'ID: {self.id}\\n' \
                f'Nombre: {self.nombre}\\n' \
                f'Descripción: {self.descripcion}\\n' \
                f'Empleado: {self.empleado}\\n' \
                f'Día: {str(self.dia)}\n' \
                f'Hora: {str(self.hora)}:00'