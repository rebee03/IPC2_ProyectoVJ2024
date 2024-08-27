from xml.etree import ElementTree as ET

from Controllers.Estructuras import lista_productos
from flask import Blueprint, jsonify, request
from Models.Producto import Producto

import os
from collections import Counter

BlueprintProducto = Blueprint('producto', __name__)

@BlueprintProducto.route('/productos/carga', methods=['POST'])
def cargaProductos():
    try:
        #OBTENEMOS EL XML
        xml_entrada = request.data.decode('utf-8')
        if xml_entrada == '':
            return jsonify({
                'message': 'Error al cargar los productos: EL XML está vacio',
                'status': 404
            }), 404
        #QUITARLE LOS SALTOS DE LINEA INNECESARIOS
        xml_entrada = xml_entrada.replace('\n', '')
        #LEER EL XML
        root = ET.fromstring(xml_entrada)
        for producto in root:
            id = producto.attrib['id']
            nombre = ''
            precio = ''
            descripcion = ''
            categoria = ''
            cantidad = ''
            imagen = ''
            for elemento in producto:
                if elemento.tag == 'nombre':
                    nombre = elemento.text
                if elemento.tag == 'precio':
                    precio = elemento.text
                if elemento.tag == 'descripcion':
                    descripcion = elemento.text
                if elemento.tag == 'categoria':
                    categoria = elemento.text
                if elemento.tag == 'cantidad':
                    cantidad = elemento.text
                if elemento.tag == 'imagen':
                    imagen = elemento.text
            nuevo = Producto(id, nombre, precio, descripcion, categoria, cantidad, imagen)
            lista_productos.append(nuevo)

            #AGREGAMOS EL PRODUCTO AL XML QUE YA EXISTE
            if os.path.exists('Proyecto2/Backend/Database/productos.xml'):
                tree2 = ET.parse('Proyecto2/Backend/Database/productos.xml')
                root2 = tree2.getroot()
                nuevo_producto = ET.Element('producto', id=nuevo.id)
                nombre = ET.SubElement(nuevo_producto, 'nombre')
                nombre.text = nuevo.nombre
                precio = ET.SubElement(nuevo_producto, 'precio')
                precio.text = nuevo.precio
                descripcion = ET.SubElement(nuevo_producto, 'descripcion')
                descripcion.text = nuevo.descripcion
                categoria = ET.SubElement(nuevo_producto, 'categoria')
                categoria.text = nuevo.categoria
                cantidad = ET.SubElement(nuevo_producto, 'cantidad')
                cantidad.text = nuevo.cantidad
                imagen = ET.SubElement(nuevo_producto, 'imagen')
                imagen.text = nuevo.imagen
                root2.append(nuevo_producto)
                ET.indent(root2, space='\t', level=0)
                tree2.write('Proyecto2/Backend/Database/productos.xml', encoding='utf-8', xml_declaration=True)

        #SI EN DADO CASO NO EXISTE EL XML, LO CREAMOS
        if not os.path.exists('Proyecto2/Backend/Database/productos.xml'):
            with open('Proyecto2/Backend/Database/productos.xml', 'w', encoding='utf-8') as file:
                file.write(xml_entrada)
                file.close()
        
        return jsonify({
            'message': 'Productos cargados correctamente',
            'status': 200
        }), 200
 
    except:
        return jsonify({
            'message': 'Error al cargar los productos',
            'status': 404
        }), 404


@BlueprintProducto.route('/productos/verProductos', methods=['GET'])
def obtenerProductos():
    productos = precargaProductos()
    diccionario_salida = {
        'mensaje': 'Productos obtenidos correctamente',
        'status': 200,
        'productos': []
    }
    for producto in productos:
        diccionario_salida['productos'].append({
            'id': producto.id,
            'nombre': producto.nombre,
            'precio': producto.precio,
            'descripcion': producto.descripcion,
            'categoria': producto.categoria,
            'cantidad': producto.cantidad,
            'imagen': producto.imagen
        })
    return jsonify(diccionario_salida),200

@BlueprintProducto.route('/productos/ver/<string:id>', methods=['GET'])
def obtenerProducto(id):
    productos = precargaProductos()
    for producto in productos:
        if producto.id == id:
            return jsonify({
                'message': 'producto encontrado',
                'status': 200,
                'producto': {
                    'id': producto.id,
                    'nombre': producto.nombre,
                    'descripcion': producto.descripcion,
                    'categoria': producto.categoria,
                    'precio': producto.precio,
                    'cantidad': producto.cantidad,
                    'imagen': producto.imagen,

                }
            }), 200
    return jsonify({
        'message': 'Libro no encontrado',
        'status': 404
    }), 404


@BlueprintProducto.route('/productos/topCategorias', methods=['GET'])
def obtenerTopCategorias():
    productos = precargaProductos()
    categorias = [producto.categoria for producto in productos]
    contador_categorias = Counter(categorias)
    top_categorias = contador_categorias.most_common(3)
    
    diccionario_salida = {
        'mensaje': 'Top 3 categorías obtenidas correctamente',
        'status': 200,
        'categorias': []
    }
    for categoria, cantidad in top_categorias:
        diccionario_salida['categorias'].append({
            'categoria': categoria,
            'cantidad': int(cantidad)
        })
    
    return jsonify(diccionario_salida), 200



@BlueprintProducto.route('/productos/topCantidad', methods=['GET'])
def obtenerTopProductos():
    productos = precargaProductos()
    
    # Ordenar productos por cantidad de forma descendente
    productos_sorted = sorted(productos, key=lambda x: int(x.cantidad), reverse=True)
    
    # Tomar los primeros 3 productos (o menos si hay menos de 3)
    top_productos = productos_sorted[:3]
    
    diccionario_salida = {
        'mensaje': 'Top 3 productos obtenidos correctamente',
        'status': 200,
        'productos': []
    }
    
    for producto in top_productos:
        diccionario_salida['productos'].append({
            'id': producto.id,
            'nombre': producto.nombre,
            'precio': producto.precio,
            'descripcion': producto.descripcion,
            'categoria': producto.categoria,
            'cantidad': int(producto.cantidad),
            'imagen': producto.imagen
        })
    
    return jsonify(diccionario_salida), 200



#METODO DE PRECARGAR PRODUCTOS
def precargaProductos():
    produ = []
    if os.path.exists('Proyecto2/Backend/Database/productos.xml'):
        tree = ET.parse('Proyecto2/Backend/Database/productos.xml')
        root = tree.getroot()
        for producto in root:
            id = producto.attrib['id']
            nombre = ''
            precio = ''
            descripcion = ''
            categoria = ''
            cantidad = ''
            imagen = ''
            for elemento in producto:
                if elemento.tag == 'nombre':
                    nombre = elemento.text
                if elemento.tag == 'precio':
                    precio = elemento.text
                if elemento.tag == 'descripcion':
                    descripcion = elemento.text
                if elemento.tag == 'categoria':
                    categoria = elemento.text
                if elemento.tag == 'cantidad':
                    cantidad = elemento.text
                if elemento.tag == 'imagen':
                    imagen = elemento.text
            nuevo = Producto(id, nombre, precio, descripcion, categoria, cantidad, imagen)
            produ.append(nuevo)
    return produ

def getProducto(id):
    productos = precargaProductos()
    for producto in productos:
        if producto.id == id:
            return producto
    return None