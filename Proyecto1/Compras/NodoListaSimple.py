class Nodo:
    def __init__(self, usuario, productos, total):
        self.usuario = usuario
        self.productos = productos
        self.total = total  
        self.siguiente = None
    
    def getUsuario(self):
        return self.usuario  
    
    def getproductos(self):
        return self.productos
    
    def gettotal(self):
        return self.total
    
    def setusuario(self, usuario):
        self.usuario = usuario    
    
    def setproductos(self, productos):
        self.productos = productos    
    
    def settotal(self, total):
        self.total = total
    