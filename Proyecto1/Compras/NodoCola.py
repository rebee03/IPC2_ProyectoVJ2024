class Nodo:
    def __init__(self, usuario, productos, total):
        self.usuario = usuario
        self.productos = productos
        self.total = total
        self.siguiente = None