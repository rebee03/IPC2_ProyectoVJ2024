import json
import os
from xml.etree import ElementTree as ET
#import xmltodict
from Controllers.CarritoController import carrito

from Controllers.ProductoController import getProducto
from Controllers.UsuarioController import getUsuario
# from Controllers.ComprarController import Blueprintcompras
from flask import Blueprint, jsonify, request
from Models.Comprar import Comprar
from Models.Carro import Carro

Blueprintcompras = Blueprint('comprar', __name__)

@Blueprintcompras.route('/comprar/agregar', methods=['POST'])
def agregarCompra():
    try:
        compras = precargarCompra()
        #OBTENEMOS EL JSON
        id_user = request.json['id_user']
        id_compra = len(compras)+1
        nuevo = Comprar(id_compra,id_user, carrito)
        compras.append(nuevo)
        if os.path.exists('Proyecto2/Backend/Database/compras.xml'):
            tree = ET.parse('Proyecto2/Backend/Database/compras.xml')
            root = tree.getroot()
            nueva_compra = ET.Element('comprar', numero=str(id_compra))
            usuario = getUsuario(id_user)
            user = ET.SubElement(nueva_compra, 'usuario', id=id_user)   
            user.text = usuario.nombre

            productos = ET.SubElement(nueva_compra, 'productos')
            for car in carrito:

                producto = getProducto(car.idProducto)
                productoxml = ET.SubElement(productos, 'producto', id=producto.id)

                nombre = ET.SubElement(productoxml, 'nombre')
                nombre.text = producto.nombre

                cantidad = ET.SubElement(productoxml, 'cantidad')
                cantidad.text = str(car.cantidad)

            root.append(nueva_compra)
            ET.indent(root, space='\t', level=0)
            tree.write('Proyecto2/Backend/Database/compras.xml', encoding='utf-8', xml_declaration=True)
        else:
            comprasxml = ET.Element('compras')
            nueva_compra = ET.SubElement(comprasxml,'comprar', numero=str(id_compra))
            usuario = getUsuario(id_user)
            user = ET.SubElement(nueva_compra, 'usuario', id=id_user)
            user.text = usuario.nombre
            productos = ET.SubElement(nueva_compra, 'productos')
            for car in carrito:
                producto = getProducto(car.idProducto)
                productoxml = ET.SubElement(productos, 'producto', id=producto.id)
                nombre = ET.SubElement(productoxml, 'nombre')
                nombre.text = producto.nombre
                cantidad = ET.SubElement(productoxml, 'cantidad')
                cantidad.text = str(car.cantidad)
            tree = ET.ElementTree(comprasxml)
            ET.indent(tree, space='\t', level=0)
            tree.write('Proyecto2/Backend/Database/compras.xml', encoding='utf-8', xml_declaration=True)
            print('ya no')
        carrito.clear()
        return jsonify({
            'message': 'Producto agregado al compras',
            'status': 200
        }), 200
    except:
        return jsonify({
            'message': 'Error al agregar al compras',
            'status': 404
        }), 404

@Blueprintcompras.route('/comprar/ver', methods=['GET'])
def verCompra():
    try:
        xml_salida = ''
        with open('Proyecto2/Backend/Database/compras.xml', 'r', encoding='utf-8') as file:
            xml_salida = file.read()
            file.close()
        return jsonify({
            'message': 'Compras',
            'status': 200,
            'contenido': xml_salida
        }), 200
    
    except:
        return jsonify({
            'message': 'Error al ver el compras',
            'status': 404
        }), 404


def precargarCompra():
    compras = []
    if os.path.exists('Proyecto2/Backend/Database/compras.xml'):
        tree = ET.parse('Proyecto2/Backend/Database/compras.xml')
        root = tree.getroot()
        for comprar in root:
            id = comprar.attrib['numero']
            id_user = ''
            productos = []
            for elemento in comprar:
                if elemento.tag == 'usuario':
                    id_user = elemento.attrib['id']
                if elemento.tag == 'productos':
                    for producto in elemento:
                        productos.append(Carro(producto.attrib['id'],producto.text))
            nuevo = Comprar(id, id_user, productos)
            compras.append(nuevo)
    return compras
