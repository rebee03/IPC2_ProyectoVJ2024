import os

from Empleados.Nodo import Nodo

class ListaCircular:
    def __init__(self):
        self.primero = None
        self.ultimo = None
        self.tamanio = 0

    def __len__(self):
        return self.tamanio
    
    def agregarEmpleado(self, dato):
        nuevo = Nodo(dato)
        #Si la lista esta vacia
        if self.primero == None and self.ultimo == None:
            #1. Asigna el nuevo nodo al primer nodo de la lista
            self.primero = nuevo
            #2. Asigna el nuevo nodo al ultimo nodo de la lista
            self.ultimo = nuevo
            #3. El ultimo nodo apunta al primer nodo
            self.ultimo.siguiente = self.primero
        #Si la lista tiene mas de 1 elemento
        else:
            #1. El siguiente del ultimo nodo apunta al nuevo nodo
            self.ultimo.siguiente = nuevo
            #2. El ultimo nodo va a ser ahora el nuevo nodo
            self.ultimo = nuevo
            #3. El siguiente del ultimo nodo apunta al primer nodo
            self.ultimo.siguiente = self.primero
        self.tamanio += 1

    def mostrarEmpleados(self):
        contador = 0
        actual = self.primero
        while contador < self.tamanio:
            print(str(actual.dato.codigo) + ' - ' + str(actual.dato.nombre) + ' - ' + str(actual.dato.puesto))
            actual = actual.siguiente
            contador += 1

    #WARNING: NO APLICAR ESTO EN UNA LISTA SIMPLEMENTE CIRCULAR
    def mostrar_sin_cuidado(self):
        actual = self.primero 
        while actual != None:
            print(actual.dato)
            actual = actual.siguiente

    #OBTENER EL DATO DE UN NODO
    def obtenerDato(self, dato):
        actual = self.primero
        contador = 0
        while contador < self.tamanio:
            if actual.dato == dato:
                return actual.dato
            actual = actual.siguiente
            contador += 1
        return None
    
    def buscarEmpleado(self, codigo):
        if self.primero is None:
            return None
        else:
            actual = self.primero
            contador = 0
            while contador < self.tamanio:
                if actual.dato.codigo == codigo:
                    return actual.dato
                actual = actual.siguiente
                contador += 1
            return None
    
    def mostrar(self):
        if self.primero is None:
            print("La lista está vacía")
        else:
            actual = self.primero
            contador = 0
            while contador < self.tamanio:
                print(actual.dato)
                actual = actual.siguiente
                contador += 1


    def buscarEmpleado(self, codigo):
        if self.primero is None:
            return None
        else:
            actual = self.primero
            contador = 0
            while contador < self.tamanio:
                if actual.dato.codigo == codigo:
                    return actual.dato
                actual = actual.siguiente
                contador += 1
            return None

#     def graficarEmpleados(self):
#         codigo_dot = ''
#         archivo = open('Reportedot/lista_circular.dot', 'w')
#         codigo_dot += '''digraph G {
#   rankdir=LR;
#   node [shape = record, height = .1]\n'''
#         #PRIMERO CREAMOS LOS NODOS
#         contador_nodos = 0
#         actual = self.primero
#         while contador_nodos < self.tamanio:
#             codigo_dot += 'node'+str(contador_nodos)+' [label = "{'+str(actual.dato)+'|<f1>}"];\n'
#             actual = actual.siguiente
#             contador_nodos += 1

#         #CREAR LAS RELACIONES O APUNTADORES
#         actual = self.primero
#         contador_nodos = 0
#         while contador_nodos < self.tamanio-1:
#             codigo_dot += 'node'+str(contador_nodos)+' -> node'+str(contador_nodos+1)+';\n'
#             actual = actual.siguiente
#             contador_nodos += 1
        
#         #AGREGAMOS LA RELACIÓN DEL NODO FINAL CON EL NODO INICIAL
#         codigo_dot += 'node'+str(self.tamanio-1)+' -> node0 [constraint=false];\n'

#         codigo_dot += '}'

#         #ESCRIBIR EL ARCHIVO .DOT
#         archivo.write(codigo_dot)
#         archivo.close()

#         #Generar la imagen
#         ruta_dot = 'Reportedot/lista_circular.dot'
#         ruta_imagen = 'Reportes/lista_circular.png'
#         comando = 'dot -Tpng '+ruta_dot+' -o '+ruta_imagen
#         os.system(comando)

#         #Abrimos la imagen
#         #convierte la ruta de la imagen que es relativa a una ruta absoluta
#         ruta_reporte2 = os.path.abspath(ruta_imagen)
#         os.startfile(ruta_reporte2)
    def graficarEmpleados(self):
        codigo_dot = ''
        archivo = open('Reportedot/lista_circular.dot', 'w')
        codigo_dot += '''digraph G {
    rankdir=LR;
    node [shape = record, height = .1]\n'''

        #PRIMERO CREAMOS LOS NODOS
        contador_nodos = 0
        actual = self.primero
        while contador_nodos < self.tamanio:
            # Ajustamos aquí para incluir más detalles del empleado
            codigo_dot += f'node{contador_nodos} [label = "{{Código: {actual.dato.codigo} | Nombre: {actual.dato.nombre} | Puesto: {actual.dato.puesto}}}"];\n'
            actual = actual.siguiente
            contador_nodos += 1

        #CREAR LAS RELACIONES O APUNTADORES
        actual = self.primero
        contador_nodos = 0
        while contador_nodos < self.tamanio-1:
            codigo_dot += f'node{contador_nodos} -> node{contador_nodos+1};\n'
            actual = actual.siguiente
            contador_nodos += 1
        
        #AGREGAMOS LA RELACIÓN DEL NODO FINAL CON EL NODO INICIAL
        codigo_dot += f'node{self.tamanio-1} -> node0 [constraint=false];\n'

        codigo_dot += '}'

        #ESCRIBIR EL ARCHIVO .DOT
        archivo.write(codigo_dot)
        archivo.close()

        #Generar la imagen
        ruta_dot = 'Reportedot/lista_circular.dot'
        ruta_imagen = 'Reportes/lista_circular.png'
        comando = f'dot -Tpng {ruta_dot} -o {ruta_imagen}'
        os.system(comando)

        #Abrimos la imagen
        #convierte la ruta de la imagen que es relativa a una ruta absoluta
        ruta_reporte2 = os.path.abspath(ruta_imagen)
        os.startfile(ruta_reporte2)
