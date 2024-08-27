import os
from xml.etree import ElementTree as ET

from Controllers.Estructuras import lista_empleados
from flask import Blueprint, jsonify, request
from Models.Empleado import Empleado


BlueprintEmpleado = Blueprint('empleado', __name__)

@BlueprintEmpleado.route('/empleados/carga', methods=['POST'])
def cargaEmpleados():
    try:
        #OBTENEMOS EL XML
        xml_entrada = request.data.decode('utf-8')
        if xml_entrada == '':
            return jsonify({
                'message': 'Error al cargar los empleados: EL XML está vacio',
                'status': 404
            }), 404
        
        xml_entrada = xml_entrada.replace('\n', '')
        #LEER EL XML
        root = ET.fromstring(xml_entrada)
        for empleado in root:
            codigo = empleado.attrib['codigo']
            nombre = ''
            puesto = ''
            for elemento in empleado:
                if elemento.tag == 'nombre':
                    nombre = elemento.text
                if elemento.tag == 'puesto':
                    puesto = elemento.text
            nuevo = Empleado(codigo, nombre, puesto)
            lista_empleados.append(nuevo)

            #AGREGAMOS EL EMPLEADO AL XML QUE YA EXISTE
            if os.path.exists('Proyecto2/Backend/Database/empleados.xml'):
                tree2 = ET.parse('Proyecto2/Backend/Database/empleados.xml')
                root2 = tree2.getroot()
                nuevo_empleado = ET.Element('empleado', codigo=nuevo.codigo)
                nombre = ET.SubElement(nuevo_empleado, 'nombre')
                nombre.text = nuevo.nombre
                puesto = ET.SubElement(nuevo_empleado, 'puesto')
                puesto.text = nuevo.puesto
                root2.append(nuevo_empleado)
                ET.indent(root2, space='\t', level=0)
                tree2.write('Proyecto2/Backend/Database/empleados.xml', encoding='utf-8', xml_declaration=True)

        #SI EN DADO CASO NO EXISTE EL XML, LO CREAMOS
        if not os.path.exists('Proyecto2/Backend/Database/empleados.xml'):
            with open('Proyecto2/Backend/Database/empleados.xml', 'w', encoding='utf-8') as file:
                file.write(xml_entrada)
                file.close()
        
        return jsonify({
            'message': 'Empleados cargados correctamente',
            'status': 200
        }), 200
 
    except:
        return jsonify({
            'message': 'Error al cargar los empleados',
            'status': 404
        }), 404


@BlueprintEmpleado.route('/empleados/verEmpleados', methods=['GET'])
def obtenerEmpleados():
    empleados = precargaEmpleados()
    diccionario_salida = {
        'message': 'Empleados cargados correctamente',
        'status': 200,
        'empleados': []
    }
    for empleado in empleados:
        diccionario_salida['empleados'].append({
            'codigo': empleado.codigo,
            'nombre': empleado.nombre,
            'puesto': empleado.puesto
        })
    return jsonify(diccionario_salida)

#METODO DE PRECARGAR EMPLEADOS
def precargaEmpleados():
    emple = []
    if os.path.exists('Proyecto2/Backend/Database/empleados.xml'):
        tree = ET.parse('Proyecto2/Backend/Database/empleados.xml')
        root = tree.getroot()
        for empleado in root:
            codigo = empleado.attrib['codigo']
            nombre = ''
            puesto = ''
            for elemento in empleado:
                if elemento.tag == 'nombre':
                    nombre = elemento.text
                if elemento.tag == 'puesto':
                    puesto = elemento.text
            nuevo = Empleado(codigo, nombre, puesto)
            emple.append(nuevo)
    return emple