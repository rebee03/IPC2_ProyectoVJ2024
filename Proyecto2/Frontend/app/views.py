#para mostrar mensajes en pantalla
from django.contrib import messages
#para las cookies
from django.http import HttpResponse
from django.shortcuts import redirect, render

from .forms import FileForm, LoginForm, SerchForm, CantidadForm

import datetime
import requests
import json

# Create your views here.
endpoint = 'http://localhost:5000/'

contexto = {
    'user':None,
    'contenido_archivo':None,
    'binario_xml':None
}

def index(request):
    return render(request, 'index.html')

def login(request):
    return render(request, 'login.html')

def signin(request):
    try:
        if request.method == 'POST':
            form = LoginForm(request.POST)
            if form.is_valid():
                #obtenemos los datos del formulario
                iduser = form.cleaned_data['iduser']
                password = form.cleaned_data['password']

                #PETICION AL BACKEND
                #ENDPOINT- URL
                url = endpoint + 'usuarios/login'
                #DATA A ENVIAR
                data = {
                    'id': iduser,
                    'password': password
                }

                #convertimos los datos a json
                json_data = json.dumps(data)

                #HEADERS
                headers = {
                    'Content-Type': 'application/json'
                }

                #llamamos a la peticion backend
                response = requests.post(url, data=json_data, headers=headers)
                respuesta = response.json()
                if response.status_code == 200:
                    rol = int(respuesta['role'])
                    contexto['user'] = iduser
                    pagina_redireccion = None
                    #IR A ADMIN
                    if rol == 0:
                        pagina_redireccion = redirect('carga')
                        pagina_redireccion.set_cookie('id_user', iduser)
                        return pagina_redireccion
                    elif rol == 1:
                        pagina_redireccion = redirect('user')
                        pagina_redireccion.set_cookie('id_user', iduser)
                        return pagina_redireccion
    except:
        return render(request, 'login.html')


def admincarga(request):
    ctx = {
        'title':'Carga Masiva'
    }
    return render(request, 'cargaadmin.html', ctx)

def cargarXML(request):
    ctx = {
        'contenido_archivo':None
    }
    try:
        if request.method == 'POST':
            #obtenemos el formulario
            form = FileForm(request.POST, request.FILES)
            print(form.is_valid())
            if form.is_valid():
                #obtenemos el archivo
                archivo = request.FILES['file']
                #guardamos el binario
                xml = archivo.read()
                xml_decodificado = xml.decode('utf-8')
                #guardamos el contenido del archivo
                contexto['binario_xml'] = xml
                contexto['contenido_archivo'] = xml_decodificado
                ctx['contenido_archivo'] = xml_decodificado
                return render(request, 'cargaadmin.html', ctx)
    except:
        return render(request, 'cargaadmin.html')

def enviarProductos(request):
    try:
        if request.method == 'POST':
            xml = contexto['binario_xml']
            if xml is None:
                messages.error(request, 'No se ha cargado ningun archivo')
                return render(request, 'cargaadmin.html')
            
            #PETICION AL BACKEND
            url = endpoint + 'productos/carga'
            respuesta = requests.post(url, data=xml)
            mensaje = respuesta.json()
            messages.success(request, mensaje['message'])
            contexto['binario_xml'] = None
            contexto['contenido_archivo'] = None
            return render(request, 'cargaadmin.html', contexto)
    except:
        return render(request, 'cargaadmin.html')

def enviarUsuarios(request):
    try:
        if request.method == 'POST':
            xml = contexto['binario_xml']
            if xml is None:
                messages.error(request, 'No se ha cargado ningun archivo')
                return render(request, 'cargaadmin.html')
            
            #PETICION AL BACKEND
            url = endpoint + 'usuarios/carga'
            respuesta = requests.post(url, data=xml)
            mensaje = respuesta.json()
            messages.success(request, mensaje['message'])
            contexto['binario_xml'] = None
            contexto['contenido_archivo'] = None
            return render(request, 'cargaadmin.html', contexto)
    except:
        return render(request, 'cargaadmin.html')

def enviarEmpleados(request):
    try:
        if request.method == 'POST':
            xml = contexto['binario_xml']
            if xml is None:
                messages.error(request, 'No se ha cargado ningun archivo')
                return render(request, 'cargaadmin.html')
            
            #PETICION AL BACKEND
            url = endpoint + 'empleados/carga'
            respuesta = requests.post(url, data=xml)
            mensaje = respuesta.json()
            messages.success(request, mensaje['message'])
            contexto['binario_xml'] = None
            contexto['contenido_archivo'] = None
            return render(request, 'cargaadmin.html', contexto)
    except:
        return render(request, 'cargaadmin.html')

def enviarActividades(request):
    try:
        if request.method == 'POST':
            xml = contexto['binario_xml']
            if xml is None:
                messages.error(request, 'No se ha cargado ningun archivo')
                return render(request, 'cargaadmin.html')
            
            #PETICION AL BACKEND
            url = endpoint + 'actividades/carga'
            respuesta = requests.post(url, data=xml)
            mensaje = respuesta.json()
            messages.success(request, mensaje['message'])
            contexto['binario_xml'] = None
            contexto['contenido_archivo'] = None
            return render(request, 'cargaadmin.html', contexto)
    except:
        return render(request, 'cargaadmin.html')


def verProductos(request):
    ctx = {
        'lista_productos':None,
        'title':'Productos'
    }
    url = endpoint + 'productos/verProductos'
    response = requests.get(url)
    data = response.json()
    ctx['productos'] = data['productos']
    return render(request, 'verProductosAdmin.html', ctx)

def verEstadisticas(request):
    ctx = {
        'title':'Estadisticas'
    }
    return render(request, 'estadisticas.html', ctx)

def verPDF(request):
    ctx = {
        'title':'PDF'
    }
    return render(request, 'verpdf.html', ctx)

def logout(request):
    response = redirect('login')
    response.delete_cookie('id_user')
    return response

def userview(request):
    ctx = {
        'productos':None,
        'title':'Productos'
    }
    url = endpoint + 'productos/verProductos'
    response = requests.get(url)
    data = response.json()
    ctx['productos'] = data['productos']
    return render(request, 'user.html', ctx)

def comprarPage(request):
    return render(request, 'comprar.html')

ctx_Producto = {
    'id_ producto':None,
}

def buscarProducto (request):
    try:
        ctx = {
            'producto_encontrado':None
        }
        if request.method == 'POST':
            form = SerchForm(request.POST)
            if form.is_valid():
                idProducto = form.cleaned_data['idProducto']
                ctx_Producto['id_producto'] = idProducto
                url = endpoint + 'productos/ver/'+idProducto
                response = requests.get(url)
                data = response.json()
                producto = data.get('producto')
                ctx['producto_encontrado'] = producto

                return render(request, 'comprar.html', ctx)
    except:
        return render(request, 'comprar.html')
    
def agregarCarrito(request):
    try:
        if request.method == 'POST':
            form = CantidadForm(request.POST)
            if form.is_valid():
                cantidad = form.cleaned_data['cantidad']
                idProducto = ctx_Producto['id_producto']
                data = {
                    'idProducto':idProducto,
                    'cantidad':cantidad
                }
                url = endpoint + 'carro/agregar'
                headers = {
                    'Content-Type': 'application/json'
                }
                response = requests.post(url, json=data, headers=headers)
                mensaje = response.json()
                return render(request, 'comprar.html')
    except:
        return render(request, 'comprar.html')

def verCarrito(request):
    ctx = {
        'contenido_carrito':None
    }
    url = endpoint + 'carro/ver'
    response = requests.get(url)
    data = response.json()
    ctx['contenido_carrito'] = data['contenido']
    return render(request, 'verCarrito.html', ctx)

def comprar(request):
    try:
        if request.method == 'POST':
            id_user = request.COOKIES.get('id_user')
            url = endpoint + 'comprar/agregar'
            data = {
                'id_user':id_user
            }
            headers = {'Content-type':'application/json'}
            response = requests.post(url, json=data, headers=headers)
            print(response.json())
            return render(request, 'comprar.html')
    except:
        return render(request, 'comprar.html')

def verCompras(request):
    ctx = {
        'contenido_comprado':None
    }
    url = endpoint + 'comprar/ver'
    response = requests.get(url)
    data = response.json()
    ctx['contenido_comprado'] = data['contenido']
    return render(request, 'reporteCompras.html', ctx)

def informacionEstudiantes(request):
    return render(request, 'informacionEstudiantes.html')

def verActividades(request):
    ctx = {
        'contenido_actividad': None
    }
    url = endpoint + 'actividades/verActividades'
    response = requests.get(url)
    data = response.json()
    ctx['contenido_actividad'] = data['contenido']
    return render(request, 'reporteActividad.html', ctx) 

