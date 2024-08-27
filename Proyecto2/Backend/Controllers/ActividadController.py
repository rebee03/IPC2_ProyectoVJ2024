import os
import datetime
from xml.etree import ElementTree as ET

from Controllers.Estructuras import lista_actividades
from flask import Blueprint, jsonify, request
from Models.Actividad import Actividad


BlueprintActividad = Blueprint('actividad', __name__)

@BlueprintActividad.route('/actividades/carga', methods=['POST'])
def cargaActividades():
    try:
        #OBTENEMOS EL XML
        xml_entrada = request.data.decode('utf-8')
        if xml_entrada == '':
            return jsonify({
                'message': 'Error al cargar las actividades: EL XML está vacio',
                'status': 404
            }), 404
    
        xml_entrada = xml_entrada.replace('\n', '')
        #LEER EL XML
        root = ET.fromstring(xml_entrada)
        for actividad in root:
            id = actividad.attrib['id']
            nombre = ''
            descripcion = ''
            empleado = ''
            dia = ''
            hora = ''
            for elemento in actividad:
                if elemento.tag == 'nombre':
                    nombre = elemento.text
                if elemento.tag == 'descripcion':
                    descripcion = elemento.text
                if elemento.tag == 'empleado':
                    empleado = elemento.text
                if elemento.tag == 'dia':
                    dia = elemento.text
                if elemento.tag == 'hora':
                    hora = elemento.text
            nuevo = Actividad(id, nombre, descripcion, empleado, dia, hora)
            lista_actividades.append(nuevo)

            #AGREGAMOS EL ACTIVIDAD AL XML QUE YA EXISTE
            if os.path.exists('Proyecto2/Backend/Database/actividades.xml'):
                tree2 = ET.parse('Proyecto2/Backend/Database/actividades.xml')
                root2 = tree2.getroot()
                nueva_actividad = ET.Element('actividad', id=nuevo.id)
                nombre = ET.SubElement(nueva_actividad, 'nombre')
                nombre.text = nuevo.nombre
                descripcion = ET.SubElement(nueva_actividad, 'descripcion')
                descripcion.text = nuevo.descripcion
                empleado = ET.SubElement(nueva_actividad, 'empleado')
                empleado.text = nuevo.empleado
                dia = ET.SubElement(nueva_actividad, 'dia')
                dia.text = nuevo.dia
                hora = ET.SubElement(nueva_actividad, 'hora')
                hora.text = nuevo.hora
                root2.append(nueva_actividad)
                ET.indent(root2, space='\t', level=0)
                tree2.write('Proyecto2/Backend/Database/actividades.xml', encoding='utf-8', xml_declaration=True)

        #SI EN DADO CASO NO EXISTE EL XML, LO CREAMOS
        if not os.path.exists('Proyecto2/Backend/Database/actividades.xml'):
            with open('Proyecto2/Backend/Database/actividades.xml', 'w', encoding='utf-8') as file:
                file.write(xml_entrada)
                file.close()
        
        return jsonify({
            'message': 'Actividades cargados correctamente',
            'status': 200
        }), 200
 
    except:
        return jsonify({
            'message': 'Error al cargar las actividades',
            'status': 404
        }), 404

@BlueprintActividad.route('/actividades/verActividades', methods=['GET'])
def obtenerActividades():
    try:
        hoy_numero = datetime.datetime.today().strftime('%u')  # Obtiene el número del día de la semana actual (1 es lunes, 7 es domingo)
        
        actividades_hoy = []
        if os.path.exists('Proyecto2/Backend/Database/actividades.xml'):
            tree = ET.parse('Proyecto2/Backend/Database/actividades.xml')
            root = tree.getroot()

            for actividad in root.findall('actividad'):
                dia = actividad.find('dia').text
                if dia == hoy_numero:
                    actividades_hoy.append(actividad)

        # Generar la salida XML
        actividades_element = ET.Element('actividades')
        if actividades_hoy:
            for actividad in actividades_hoy:
                actividad_element = ET.Element('actividad', id=actividad.attrib['id'])
                nombre_element = ET.SubElement(actividad_element, 'nombre')
                nombre_element.text = actividad.find('nombre').text

                descripcion_element = ET.SubElement(actividad_element, 'descripcion')
                descripcion_element.text = actividad.find('descripcion').text

                empleado_element = ET.SubElement(actividad_element, 'empleado')
                empleado_element.text = actividad.find('empleado').text

                dia_element = ET.SubElement(actividad_element, 'dia', hora=actividad.find('dia').attrib['hora'])
                dia_element.text = actividad.find('dia').text

                actividades_element.append(actividad_element)
            ET.indent(actividades_element, space='\t', level=0)
        
        xml_salida = ET.tostring(actividades_element, encoding='unicode')

        return jsonify({
            'message': 'Actividades cargados correctamente',
            'status': 200,
            'contenido': xml_salida
        }), 200
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({
            'message': 'Error al cargar las actividades',
            'status': 404,
            'contenido': ''
        }), 404

#METODO DE PRECARGAR ACTIVIDADES
def precargaActividades():
    activ = []
    if os.path.exists('Proyecto2/Backend/Database/actividades.xml'):
        tree = ET.parse('Proyecto2/Backend/Database/actividades.xml')
        root = tree.getroot()
        for actividad in root:
            id = actividad.attrib['id']
            nombre = ''
            descripcion = ''
            empleado = ''
            dia = ''
            hora = ''
            for elemento in actividad:
                if elemento.tag == 'nombre':
                    nombre = elemento.text
                if elemento.tag == 'descripcion':
                    descripcion = elemento.text
                if elemento.tag == 'empleado':
                    empleado = elemento.text
                if elemento.tag == 'dia':
                    dia = elemento.text
                if elemento.tag == 'hora':
                    hora = elemento.text
                
            nuevo = Actividad(id, nombre, descripcion, empleado, dia, hora)
            activ.append(nuevo)
    return activ