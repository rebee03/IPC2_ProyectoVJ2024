import os
from Compras.NodoPila import Nodo

class Pila:
    def __init__(self):
        self.cima = None
        self.tamanio = 0
        self.total = 0

    #1. Agregar
    def push(self, producto, cantidad):
        nuevo = Nodo( producto, cantidad)
        nuevo.abajo = self.cima
        self.cima = nuevo
        self.tamanio += 1
        self.total += float(producto.precio) * int(cantidad)
        print(self.total)
    
    def isEmpty(self):
        return self.cima == None
    
    def __len__(self):
        return self.tamanio
    
    # 2. Eliminar
    def pop(self):
        if self.cima == None:
            print('Pila vacia')
            return None
        nodo_a_eliminar = self.cima
        self.cima = self.cima.abajo
        self.tamanio -= 1
        return nodo_a_eliminar.nodo_a_eliminar.producto, nodo_a_eliminar.total
    
    # 3. Cima Pila
    def peek(self):
        if self.cima == None:
            print('Pila vacia')
            return None
        # print(self.cima.producto, self.total)
        return self.cima.producto, self.total
        

    def retornarpila(self):
        cadena = ''
        actual = self.cima
        while actual is not None:
            cadena += f'{actual.producto.nombre}'
            actual = actual.abajo
        return cadena

    def mostrar(self):
        if self.isEmpty():
            print('Pila vacia')
            return
        actual = self.cima
        while actual is not None:
            print(actual.producto, actual.cantidad)
            actual = actual.abajo

    def retornarproducto (self):
        cadena = ''
        actual = self.cima
        while actual is not None:
            cadena += f'{actual.producto.nombre},'
            actual = actual.abajo
        return cadena
    

    # 7. METODO PARA GRAFICAR LA PILA
    def graficar(self):
        codigodot = ''
        archivo = open('Reportedot/pila.dot', 'w')
        codigodot += '''digraph G {
    rankdir=LR;
    node[shape=Mrecord];\n'''
        nodos = 'Nodo[xlabel = Pila label = "'
        #GRAFICAMOS LOS NODOS
        actual = self.cima
        while actual != None:
            if actual.abajo != None:
                nodos+= 'Nombre: ' + str(actual.producto.nombre) + '\\nCantidad: ' + str(actual.cantidad) + '|'
            else:
                nodos+= 'Nombre: ' + str(actual.producto.nombre) + '\\nCantidad: ' + str(actual.cantidad)
            actual = actual.abajo
        nodos+= '"];\n'
        codigodot+= nodos+"}"

        #GENERAMOS EL DOT
        archivo.write(codigodot)
        archivo.close()

        #GENERAMOS LA IMAGEN
        ruta_dot = 'Reportedot/pila.dot'
        ruta_salida = 'Reportes/pila.svg'
        comando = 'dot -Tsvg '+ruta_dot+' -o '+ruta_salida
        os.system(comando)
        #ABRIMOS LA IMAGEN
        #convierte la ruta relativa en absoluta
        ruta_salida2 = os.path.abspath(ruta_salida)
        #COMANDO PARA ABRIR LA IMAGEN
        os.startfile(ruta_salida2)