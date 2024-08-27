from Controllers.ComprarController import Blueprintcompras
from Controllers.CarritoController import BlueprintCarro

from Controllers.Estructuras import lista_productos
from Controllers.Estructuras import lista_usuarios
from Controllers.Estructuras import lista_empleados
from Controllers.Estructuras import lista_actividades


from Controllers.ProductoController import BlueprintProducto, precargaProductos
from Controllers.UsuarioController import BlueprintUser, precargarUsuarios
from Controllers.EmpleadoController import BlueprintEmpleado, precargaEmpleados
from Controllers.ActividadController import BlueprintActividad, precargaActividades


from flask import Flask
#from flask.json import jsonify
from flask_cors import CORS


app = Flask(__name__)
#cors = CORS(app, origins=True, allow_headers=['Content-Type', 'Authorization'], supports_credentials=True)
cors = CORS(app)

#PARA PRECARGAR LA DATA
lista_productos = precargaProductos()
lista_usuarios = precargarUsuarios()
lista_empleados = precargaEmpleados()
lista_actividades = precargaActividades()

#IMPRIMIMOS LA LONGITUD DE LAS LISTAS
print('Hay '+str(len(lista_productos)) + ' productos cargados')
print('Hay '+str(len(lista_usuarios)) + ' usuarios cargados')
print('Hay '+str(len(lista_empleados)) + ' empleados cargados')
print('Hay '+str(len(lista_actividades)) + ' actividades cargadas')

#REGISTRAMOS LOS BLUEPRINTS
app.register_blueprint(BlueprintProducto)
app.register_blueprint(BlueprintUser)
app.register_blueprint(BlueprintEmpleado)
app.register_blueprint(BlueprintActividad)
app.register_blueprint(Blueprintcompras)
app.register_blueprint(BlueprintCarro)


if __name__ == '__main__':
    app.run(host='localhost', port=5000, debug=True)