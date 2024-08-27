import os
from Compras.NodoCola import Nodo

class Cola:
    def __init__(self):
        self.primero = None
        self.tamanio = 0
    
    #METODOS DE COLA
    #1. METODO PARA INSERTAR UN ELEMENTO A LA COLA (ENQUEUE)
    def enqueue(self, usuario, productos, total):
        nuevo = Nodo(usuario, productos, total)
        if self.primero == None:
            self.primero = nuevo
        else:
            actual = self.primero
            while actual != None:
                if actual.siguiente == None:
                    actual.siguiente = nuevo
                    break
                actual = actual.siguiente
        self.tamanio += 1

    #2. METODO PARA ELIMINAR UN ELEMENTO DE LA COLA (DEQUEUE)
    def dequeue(self):
        if self.primero == None:
            print('Cola vacia')
            return None
        else:
            nodo_a_eliminar = self.primero
            self.primero = self.primero.siguiente
            self.tamanio -= 1
            return nodo_a_eliminar       
        
    #3. METODO PARA MOSTRAR EL PRIMERO DE LA COLA
    def verPrimero(self):
        if self.primero == None:
            print('Cola vacia')
            return None
        else:
        # return 'Nombre: ' + self.primero.usuario, '\nProductos:' + self.primero.productos, '\nTotal:' + str(self.primero.total)
            return 'Nombre: {}, \nProducto: {}, \nTotal: {}'.format(self.primero.usuario, self.primero.productos, self.primero.total)

    #4. OBTENER EL TAMAÑO DE LA COLA
    def size(self):
        return self.tamanio
    
    #5. METODO PARA MOSTRAR LA COLA EN CONSOLA
    def mostrar(self):
        if self.primero == None:
            print('Cola vacia')
            return
        actual = self.primero
        while actual != None:
            print(actual.usuario, actual.productos, actual.total)
            actual = actual.siguiente

    #6. METODO PARA SABER SI LA COLA ESTA VACIA
    def isEmpty(self):
        return self.primero == None
    
    # #7. METODO PARA GRAFICAR LA COLA
    def graficar(self):
        codigodot = ''
        archivo = open('Reportedot/cola.dot', 'w')
        codigodot += '''digraph G {
    rankdir="RL";
    label="Cola";
    node[shape=box];\n'''

        contador = 0
        actual = self.primero
        conexiones = ''
        nodos = ''
        while actual != None:
            nodos += 'Nodo'+str(contador)+'[style="filled", label="'+ str(actual.usuario)+ '\\n' +str(actual.productos)+'\\n'+str(actual.total)+'", fillcolor="green"];\n'
            if actual.siguiente != None:
                conexiones += 'Nodo'+str(contador+1) + ' -> Nodo'+str(contador)+';\n'
            contador += 1
            actual = actual.siguiente
        
        codigodot += nodos +"\n"+ conexiones + '\n}'

        #ESCRIBIMOS EN EL ARCHIVO
        archivo.write(codigodot)
        archivo.close()

        #GENERAMOS LA IMAGEN
        ruta_dot = 'Reportedot/cola.dot'
        ruta_salida = 'Reportes/cola.png'
        comando = 'dot -Tpng '+ruta_dot+' -o '+ruta_salida
        os.system(comando)
        #ABRIMOS LA IMAGEN
        #CONVIERTE LA RUTA RELATIVA EN ABSOLUTA
        ruta_salida2 = os.path.abspath(ruta_salida)
        os.startfile(ruta_salida2)