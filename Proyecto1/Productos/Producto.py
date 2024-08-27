class Producto:
    def __init__(self, id, nombre, precio, descripcion, categoria, cantidad, imagen):
        self.id = id
        self.nombre = nombre
        self.precio = precio
        self.descripcion = descripcion
        self.categoria = categoria
        self.cantidad = cantidad
        self.imagen = imagen

    def __str__(self):
        return f'ID: {self.id}\\n' \
                f'Nombre: {self.nombre}\\n' \
                f'Precio: {self.precio}\\n' \
                f'Descripcion: {self.descripcion}\\n' \
                f'Categoria: {self.categoria}\\n' \
                f'Cantidad: {self.cantidad}\\n' \
                f'Imagen: {self.imagen}'