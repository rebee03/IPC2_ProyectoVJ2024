import os
import datetime
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

#Importar las clases necesarias
from Usuarios.Usuario import Usuario
from Productos.Producto import Producto
from Empleados.Empleado import Empleado
from Actividades.Actividad import Actividad
from Actividades.Matriz_Dispersa import MatrizDispersa

#Libreria para ElementTree
import xml.etree.ElementTree as ET
from tkinter import filedialog, messagebox
#from Compras.Comprador  import Comprador

#Importar las listas
from Usuarios.Lista_Doble import ListaDoble
from Productos.Lista_Doble_Circular import ListaDobleCircular
from Empleados.Lista_Circular import ListaCircular
from Compras.Pila import Pila
from Compras.Cola import Cola
from Compras.ListaSimple import ListaSimple
#from Actividades.Lista_Ortogonal import ListaCabecera

#Creamos las listas globales
lista_usuarios = ListaDoble()
lista_productos = ListaDobleCircular()
lista_empleados = ListaCircular()
lista_aceptados = ListaSimple()
lista_actividades = MatrizDispersa()
ComprasPila = Pila()
ComprasCola = Cola()


#Variable global para la ruta
ruta = ''
nombre_usuario = ''
total = 0
# indice_compra_actual = 0
productos_mismoUsuario = ''

# --------------------------------------------------- Funciones Compartidas ---------------------------------------------------
def Regresar():
    ventanaAdmin.withdraw()
    ventana.deiconify()
    ventanaComprar.withdraw()	
    limpiarCampo()

def Salir():
    os._exit(0)

def limpiarCampo():
    entry_usuario.delete(0, tk.END)
    entry_clave.delete(0, tk.END)
    cuadroCatnidad.delete("1.0", tk.END)
    labelImagen.config(image=None)

def login():
    global nombre_usuario
    actual  = lista_usuarios.cabeza
    usuario = entry_usuario.get()
    clave = entry_clave.get()

    if usuario == "1" and clave == "1":
        ventanaAdmin.deiconify()  
        ventana.withdraw()

    else:
        while actual != None:
            if actual.dato.usuario == usuario and actual.dato.contrasena == clave:
                nombre_usuario = actual.dato.nombre
                ventanaComprar.deiconify()
                ventana.withdraw()
                break
            actual = actual.siguiente
        else:
            print("Usuario no encontrado")
    limpiarCampo()

# --------------------------------------------------- Ventana login ---------------------------------------------------
ventana = tk.Tk()
ventana.title("Login")

label_usuario = tk.Label(ventana, text="Usuario:")
label_usuario.grid(row=0, column=0, padx=10, pady=5, sticky=tk.E)

label_clave = tk.Label(ventana, text="Clave:")
label_clave.grid(row=1, column=0, padx=10, pady=5, sticky=tk.E)

entry_usuario = tk.Entry(ventana)
entry_usuario.grid(row=0, column=1, padx=10, pady=5)

entry_clave = tk.Entry(ventana, show="*")
entry_clave.grid(row=1, column=1, padx=10, pady=5)

boton_login = tk.Button(ventana, text="Login", command=login)
boton_login.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

# ---------------------------------------------- Ventana administrador ----------------------------------------------
ventanaAdmin = tk.Toplevel()
ventanaAdmin.title("Administrador")
ventanaAdmin.withdraw()  

def pestañaCargar(event):
    menu = tk.Menu(ventana, tearoff=0)
    menu.add_command(label="Cargar Usuarios", command=cargar_usuarios_xml)
    menu.add_command(label="Cargar Productos", command=cargar_productos_xml)
    menu.add_command(label="Cargar Empleados", command=cargar_empleados_xml)
    menu.add_command(label="Cargar Actividades", command=cargar_actividades_xml)
    menu.post(event.x_root, event.y_root)

def pestañaReportes(event):
    menu = tk.Menu(ventana, tearoff=0)
    menu.add_command(label="Reporte Usuarios", command=reporte_usuarios)
    menu.add_command(label="Reporte Productos", command=reporte_productos)
# prueba
    menu.add_command(label="Reporte Compras", command=lista_aceptados.graficar)
    menu.add_command(label="Reporte Cola", command=ComprasCola.graficar)
# prueba
    menu.add_command(label="Reporte Empleados", command=reporte_empleados)
    menu.add_command(label="Reporte Actividades", command=reporte_actividades)
    menu.post(event.x_root, event.y_root)

botonCargar = tk.Button(ventanaAdmin, text="Cargar Datos")
botonCargar.grid(row=2, column=0, columnspan=2, padx=5, pady=10)
botonCargar.bind("<Button-1>", pestañaCargar) 

botonReportes = tk.Button(ventanaAdmin, text="Reportes")
botonReportes.grid(row=2, column=3, columnspan=2, padx=5, pady=10)
botonReportes.bind("<Button-1>", pestañaReportes) 

botonVerActividades = tk.Button(ventanaAdmin, text="Ver Actividades")
botonVerActividades.grid(row=2, column=6, columnspan=2, padx=5, pady=10)

labelAutorizar = tk.Label(ventanaAdmin, text="Autorizar Compra")
labelAutorizar.grid(row=3, column=0, padx=10, pady=5, sticky=tk.E)

textArea = tk.Text(ventanaAdmin, width=30, height=10)
textArea.grid(row=4, column=0, columnspan=10, padx=1, pady=0)

botonRegresar = tk.Button(ventanaAdmin, text="Regresar", command=Regresar)
botonRegresar.grid(row=6, column=15, columnspan=2, padx=10, pady=10)

botonSalir = tk.Button(ventanaAdmin, text="Salir", command=Salir)
botonSalir.grid(row=6, column=17, columnspan=2, padx=10, pady=10)

# ---------------------------------------------- Ventana Comprar ----------------------------------------------
imagen_tk = None
ventanaComprar = tk.Toplevel()
ventanaComprar.title("Comprar")
ventanaComprar.withdraw()

def pestanaVerProductoSeleccionado():
    global imagen_tk
    producto_seleccionado = comboProductos.get()
    if producto_seleccionado:
        detalles_producto = lista_productos.obtenerDetallesProducto(producto_seleccionado)
        if detalles_producto:
            nombreProducto.config(text=f"Nombre: {detalles_producto.nombre}")
            labelPrecio.config(text=f"Precio: {detalles_producto.precio}")
            labelDescripcion.config(text=f"Descripcion: {detalles_producto.descripcion}")
            labelCantidad.config(text=f"Cantidad: {detalles_producto.cantidad}")
            rutaImagen = detalles_producto.imagen
            try:
                imagen = Image.open(rutaImagen)
                tamano = (200, 200)  
                imagen = imagen.resize(tamano, Image.BICUBIC)
                imagen_tk = ImageTk.PhotoImage(imagen)
                labelImagen.config(image=imagen_tk)
                labelImagen.image = imagen_tk  
                ventanaComprar.imagen_tk = imagen_tk
            except Exception as e:
                print(f"Error al cargar la imagen: {e}")
        else:
            print("El producto seleccionado no se encontró.")
    else:
        print("Ningún producto seleccionado.")

    nombreProducto.update()
    labelPrecio.update()
    labelDescripcion.update()
    labelCantidad.update()
    labelImagen.update()

def agregarAlCarrito():
    # global productos_mismoUsuario
    producto_seleccionado = comboProductos.get()
    cantidad = cuadroCatnidad.get("1.0", tk.END)
    if producto_seleccionado and cantidad:
        detalles_producto = lista_productos.obtenerDetallesProducto(producto_seleccionado)
        if detalles_producto:
            ComprasPila.push(detalles_producto, int(cantidad))
            messagebox.showinfo("Exito","Agregado Exitosamente")
            return ComprasPila.peek()
        else:
            messagebox.showerror("Error","Producto no encontrado")

# Cola agregar el usuario logueado, productos mismo usuario y total
def confirmarCompra():
    global nombre_usuario
    # ComprasPila.total = 0
    compras = ComprasPila.retornarpila()
    if compras != '':
        ComprasCola.enqueue(nombre_usuario, compras, ComprasPila.total)        
        textArea.insert(tk.END, f'{ComprasCola.verPrimero()}\n')
        messagebox.showinfo("Exito", "Compra Confirmada")
        ComprasPila.cima = None
        ComprasPila.total = 0
    else:
        messagebox.showerror("Error", "No hay productos en el carrito")

# Lista Simple
def aceptarCompra():
    comprasAceptadas = ComprasCola.dequeue()
    if comprasAceptadas:
        lista_aceptados.insertar(comprasAceptadas.usuario, comprasAceptadas.productos, comprasAceptadas.total)
        textArea.delete("1.0", tk.END)
        textArea.insert(tk.END, f'{ComprasCola.verPrimero()}\n')
        messagebox.showinfo("Exito", "Compra Aceptada")
        # print(lista_aceptados.imprimirLista())
#  Eliminar de la pila y de la cola
def cancelarCompra():
    comprasAceptadas = ComprasCola.dequeue()
    if comprasAceptadas:
        textArea.delete("1.0", tk.END)
        textArea.insert(tk.END, f'{ComprasCola.verPrimero()}\n')
        messagebox.showinfo("Exito", "Compra Rechazada")


botonVer = tk.Button(ventanaComprar, text="Ver", command=pestanaVerProductoSeleccionado)
labelImagen = tk.Label(ventanaComprar)
labelImagen.config(image=imagen_tk)
labelImagen.image = imagen_tk
comboProductos = ttk.Combobox(ventanaComprar, values=[], width=30)
nombreProducto = tk.Label(ventanaComprar, text=[])
labelPrecio = tk.Label(ventanaComprar, text=[])
labelCantidad = tk.Label(ventanaComprar, text=[])
labelDescripcion = tk.Label(ventanaComprar, text=[])
textCantidad = tk.Label(ventanaComprar, text="Cantidad Deseada:")
cuadroCatnidad = tk.Text(ventanaComprar, width=3, height=1)
botonAgregarCarrito = tk.Button(ventanaComprar, text="Agregar al carrito", command=agregarAlCarrito)
botonConfirmarCompra = tk.Button(ventanaComprar, text="Confirmar Compra", command=confirmarCompra)
botonVerCarrito = tk.Button(ventanaComprar, text="Ver Carrito", command=ComprasPila.graficar)
botonRegresar = tk.Button(ventanaComprar, text="Regresar", command=Regresar)
botonSalir = tk.Button(ventanaComprar, text="Salir", command=Salir)

botonVer.grid(row=0, column=4)
comboProductos.grid(row=0, column=0)
labelImagen.grid(row=2, column=0, columnspan=1, rowspan=1, padx=10, pady=5)
nombreProducto.grid(row=1, column=3, padx=10, pady=5, sticky=tk.W)
labelPrecio.grid(row=2, column=3, padx=10, pady=5, sticky=tk.W)
labelCantidad.grid(row=3, column=3, padx=10, pady=5, sticky=tk.W)
labelDescripcion.grid(row=4, column=3, padx=10, pady=5, sticky=tk.W)
textCantidad.grid(row=5, column=3, padx=10, pady=5, sticky=tk.W)
cuadroCatnidad.grid(row=5, column=5, padx=10, pady=5, sticky=tk.W)
botonAgregarCarrito.grid(row=8, column=0, columnspan=1, padx=5, pady=10)
botonConfirmarCompra.grid(row=8, column=3, columnspan=1, padx=5, pady=10)
botonVerCarrito.grid(row=8, column=6, columnspan=1, padx=5, pady=10)
botonRegresar.grid(row=9, column=0, columnspan=1, padx=5, pady=10)
botonSalir.grid(row=9, column=3, columnspan=1, padx=10, pady=10)


# Admin botones prueba
botonAceptar = tk.Button(ventanaAdmin, text="Aceptar", command=aceptarCompra)
botonAceptar.grid(row=3, column=9, columnspan=2, padx=10, pady=0)

botonCancelar  = tk.Button(ventanaAdmin, text="Cancelar", command=cancelarCompra)
botonCancelar.grid(row=4, column=9, columnspan=2, padx=10, pady=10)

# ---------------------------------------------- Usuarios ----------------------------------------------

def cargar_usuarios_xml():
    ruta_tinter = filedialog.askopenfilename(title='Cargar Archivo XML', filetypes= (('Text files', '.xml'), ('All files', '.')))
    leer_xml_usuarios(ruta_tinter)
    
def leer_xml_usuarios(ruta):
    global lista_usuarios
    tree = ET.parse(ruta)
    root = tree.getroot()
    for usuario in root:
        id = usuario.attrib['id']
        password = usuario.attrib['password']
        nombre = ''
        edad = ''
        email = ''
        telefono = ''
        for subusuario in usuario:
            match subusuario.tag:
                case 'nombre':
                    nombre = subusuario.text
                case 'edad':
                    edad = subusuario.text
                case 'email':
                    email = subusuario.text
                case 'telefono':
                    telefono = subusuario.text
        #CREAMOS UN OBJETO USUARIO
        user = Usuario(id, password, nombre, edad, email, telefono)
        #INSERTAMOS EL USUARIO EN LA LISTA
        lista_usuarios.insertar(user)
    # lista_usuarios.imprimirUsuarios()

def reporte_usuarios():
    lista_usuarios.imprimirlista_desdeinicio()
    lista_usuarios.imprimirlista_alreves()
    lista_usuarios.graficar()
    messagebox.showinfo("Reporte", "Reporte de usuarios generado")

# ---------------------------------------------- Productos ----------------------------------------------
nombres_productos = []

def llenar_combobox_productos():
    if lista_productos.tamanio > 0: 
        actual = lista_productos.primero  
        while True:
            nombre_actual = actual.dato.nombre 
            nombres_productos.append(nombre_actual)
            actual = actual.siguiente
            if actual == lista_productos.primero:
                break

    comboProductos['values'] = nombres_productos

    if nombres_productos:
        comboProductos.current(0)

    return nombres_productos

def cargar_productos_xml():
    ruta_tinter = filedialog.askopenfilename(title='Cargar Archivo XML', filetypes= (('Text files', '.xml'), ('All files', '.')))
    leer_xml_productos(ruta_tinter)

def leer_xml_productos(ruta):
    global lista_productos
    tree = ET.parse(ruta)
    root = tree.getroot()
    for producto in root:
        #Para obtener los atributos de una etiqueta
        id = producto.attrib['id']
        nombre = ''
        precio = ''
        descripcion = ''
        categoria = ''
        cantidad = ''
        imagen = ''
        #para recorrer las etiquetas dentro de producto
        for subproducto in producto:
            match subproducto.tag:
                case 'nombre':
                    nombre = subproducto.text
                case 'precio':
                    precio = subproducto.text
                case 'descripcion':
                    descripcion = subproducto.text
                case 'categoria':
                    categoria = subproducto.text
                case 'cantidad':
                    cantidad = subproducto.text
                case 'imagen':
                    imagen = subproducto.text
        #CREAMOS UN OBJETO PRODUCTO
        product = Producto(id, nombre, precio, descripcion, categoria, cantidad, imagen)
        #INSERTAMOS EL PRODUCTO EN LA LISTA
        lista_productos.agregarProducto(product)
    # lista_productos.imprimirProductos()
    llenar_combobox_productos()

def reporte_productos():
    lista_productos.mostrarProducto()
    lista_productos.graficarProductos()
    messagebox.showinfo("Reporte", "Reporte de productos generado")

# ---------------------------------------------- Empleados ----------------------------------------------
def cargar_empleados_xml():
    ruta_tinter = filedialog.askopenfilename(title='Cargar Archivo XML', filetypes= (('Text files', '.xml'), ('All files', '.')))
    leer_xml_empleados(ruta_tinter)

def leer_xml_empleados(ruta):
    global lista_empleados
    tree = ET.parse(ruta)
    root = tree.getroot()
    for empleado in root:
        codigo = empleado.attrib['codigo']
        nombre = ''
        puesto = ''
        # Para recorrer las etiquetas dentro de empleado
        for subempleado in empleado:
            if subempleado.tag == 'nombre':
                nombre = subempleado.text
            elif subempleado.tag == 'puesto':
                puesto = subempleado.text
        # Creamos un objeto Empleado
        employee = Empleado(codigo, nombre, puesto)
        # Insertamos el empleado en la lista
        lista_empleados.agregarEmpleado(employee)


def reporte_empleados():    
    # lista_empleados.mostrarEmpleados()
    lista_empleados.graficarEmpleados()
    messagebox.showinfo("Reporte", "Reporte de empleados generado")

# ---------------------------------------------- Actividades --------------------------------------------------------
ventanaActividad = tk.Toplevel()
ventanaActividad.withdraw()
ventanaActividad.title("Actividades")
ventanaActividad.geometry("250x200")

text_area = tk.Text(ventanaActividad, width=30, height=10)
text_area.grid(row=4, column=2, columnspan=10, padx=1, pady=0)

numeros = [str(i) for i in range(1, 8)]


def ver_actividades():
    ventanaActividad.deiconify()
    global dia_seleccionado
    #lista_actividades.recorridoColumnas(dia_seleccionado)
    text_area.insert(tk.END, lista_actividades.recorridoColumnas(obtener_dia_hoy()))    
    #text_area.insert(tk.END, f'{lista_actividades.recorridoColumnas(int(dia_seleccionado))}\n')
    text_area.config(state=tk.DISABLED)  

botonVerActividades = tk.Button(ventanaAdmin, text="Ver Actividades", command=ver_actividades)
botonVerActividades.grid(row=2, column=6, columnspan=2, padx=5, pady=10)

def cargar_actividades_xml():
    ruta_tinter = filedialog.askopenfilename(title='Cargar Archivo XML', filetypes= (('Text files', '.xml'), ('All files', '.')))
    leer_xml_actividades(ruta_tinter)

def leer_xml_actividades(ruta):
    global lista_actividades
    if lista_empleados.tamanio == 0:
        print('Primero debe cargar los empleados')
        messagebox.showinfo("Error", "Primero debe cargar los empleados")
        return
    tree = ET.parse(ruta)
    root = tree.getroot()

    for actividad in root:
        id_actividad = actividad.attrib['id']
        nombre = ''
        descripcion = ''
        empleado = ''
        dia = 0
        hora = 0
        for subactividad in actividad:
            match subactividad.tag:
                case 'nombre':
                    nombre = subactividad.text
                case 'descripcion':
                    descripcion = subactividad.text
                case 'empleado':
                    empleado = subactividad.text
                case 'dia':
                    dia = int(subactividad.text)
                    hora = int(subactividad.attrib['hora'])
        
        #OBTENEMOS EL NOMBRE DEL LIBRO Y DEL USUARIO
        nombre_empleado= lista_empleados.buscarEmpleado(empleado).nombre
        #CREAMOS UN OBJETO RESERVACIÓN
        activity = Actividad(id_actividad, nombre, descripcion, nombre_empleado, dia, hora)
        #INSERTAMOS LA RESERVACIÓN EN LA MATRIZ
        # X = FILAS = HORAS, Y = COLUMNAS = DIAS
        lista_actividades.insertar(hora, dia, activity)

def obtener_dia_hoy():
    hoy = datetime.datetime.today()
    dia_hoy = hoy.weekday()+1
    # print(f'Hoy es el dia {str(dia_hoy)} de la semana')
    return dia_hoy

def reporte_actividades():
    lista_actividades.graficarActividades()
    messagebox.showinfo("Reporte", "Reporte de actividades generado")

if __name__ == '__main__':
    # ventana.mainloop()
    ventanaComprar.mainloop()