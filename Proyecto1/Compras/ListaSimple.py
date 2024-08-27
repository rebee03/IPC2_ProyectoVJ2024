import os
from Compras.NodoListaSimple import Nodo

class ListaSimple:
    def __init__(self):
        self.header = None
        self.size = 0
    
    def __len__(self):
        return self.size

    def insertar (self, usuario, productos, total):
    # Insertar al final
        # Crear un nuevo nodo
        new = Nodo(usuario, productos, total)
        # Se verifica si la lista está vacía
        if self.header == None:
            self.header = new 
        else: 
            current = self.header
            while current != None:
                if current.siguiente == None:
                    current.siguiente = new
                    break
                current = current.siguiente
            self.size += 1

    def eliminar (self, usuario):
        # se señaliza la cabeza de la lista
        current = self.header
        # se señaliza el nodo anterior
        previous = None
        while current != None:
            if current.usuario == usuario:
                if previous == None:
                    self.header = current.siguiente
                else:
                    previous.siguiente = current.siguiente
                self.size -= 1
                return True
            previous = current
            current = current.siguiente
        return False
    
    def imprimirLista(self):
        current = self.header
        while current != None:
            # print('---------------------------------------------------')
            # print('usuario:', current.usuario, '\nproductos:',  current.productos, '\nTotal:', current.total)
            current = current.siguiente
    
    def graficar(self):
        codigodot = ''
        archivo = open('Reportedot/lista_simple.dot', 'w')
        codigodot += '''digraph G {
  rankdir=LR;
  node [shape = record, height = .1]'''
        contador_nodos = 0
        #PRIMERO CREAMOS LOS NODOS
        current = self.header
        while current != None:
            codigodot += 'node' + str(contador_nodos) + '[label = \"{Usuario: ' + str(current.usuario) + '\\nProductos: ' + str(current.productos) + '\\nProductos: ' + str(current.total) + '|<f1>}\"];\n'

            contador_nodos += 1
            current = current.siguiente

        #AHORA CREAMOS LAS RELACIONES
        current = self.header
        contador_nodos = 0
        while current.siguiente != None:
            codigodot += 'node'+str(contador_nodos)+'-> node'+str(contador_nodos+1)+';\n'
            contador_nodos += 1
            current = current.siguiente

        codigodot += '}'

        #Lo escribimos en el archivo dot
        archivo.write(codigodot)
        archivo.close()

        #Generamos la imagen
        ruta_dot = 'Reportedot/lista_simple.dot'
        ruta_reporte = 'Reportes/lista_simple.png'
        comando = 'dot -Tpng '+ruta_dot+' -o '+ruta_reporte
        os.system(comando)
        #Abrir la imagen
        #CONVERTIR DE RUTA RELATIVA A RUTA ABSOLUTA
        ruta_abrir_reporte = os.path.abspath(ruta_reporte)
        os.startfile(ruta_abrir_reporte)
        print('Reporte generado con éxito')