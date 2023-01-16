from flask import Flask,request,jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] ='mysql+pymysql://root:@localhost:3306/bdudemy'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.app_context().push()
db = SQLAlchemy(app)
ma = Marshmallow(app)

#Creacion de tabla - categoria
class Categoria(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    nombre = db.Column(db.String(100))
    desp = db.Column(db.String(100))

    def __init__(self,nombre,desp):
        self.nombre = nombre
        self.desp = desp


db.create_all()

#Esquema categoria
class CategoriaSchema(ma.Schema):
    class Meta:
        fields=('id','nombre','desp')
#Una sola respuesta
categoria_schema = CategoriaSchema()
#Este para muchas respuestas
categorias_schema = CategoriaSchema(many=True)

#GET#######################################
@app.route('/categorias', methods=['GET'])
def get_categorias():
    all_categorias = Categoria.query.all()
    result = categorias_schema.dump(all_categorias)
    return jsonify(result)

# GET x ID ###
@app.route('/categoria/<id>', methods=['GET'])
def get_categoria_x_id(id):
    una_categoria = Categoria.query.get(id)
    return categoria_schema.jsonify(una_categoria)

#POST#######
@app.route('/categoria', methods=['POST'])
def insert_categoria():
    nombre = request.json['nombre']
    desp = request.json['desp']
    nuevo_registro = Categoria(nombre,desp)
    db.session.add(nuevo_registro)
    db.session.commit()
    return categoria_schema.jsonify(nuevo_registro)

#PUT######
@app.route('/categoria/<id>', methods=['PUT'])
def update_categoria(id):
    actualizar_categoria = Categoria.query.get(id)
    nombre = request.json['nombre']
    desp = request.json['desp']

    actualizar_categoria.nombre = nombre
    actualizar_categoria.desp = desp

    db.session.commit()
    return categoria_schema.jsonify(actualizar_categoria)

#DELETE ####
@app.route('/categoria/<id>', methods=['DELETE'])
def delete_categoria(id):
    eliminar_categoria = Categoria.query.get(id)
    db.session.delete(eliminar_categoria)
    db.session.commit()
    return categoria_schema.jsonify(eliminar_categoria)
    

#Mensaje de ingreso
@app.route('/',methods=['GET'])
def index():
    return jsonify({'Mensaje probando mensaje':'Bienvenido al proyecto de API REST Python'})

if __name__=='__main__':
    app.run(debug=True)


#Lineas de referencias:
#Linea 6 - Luego del //root: debería ir la contraseña(En el caso de usarse)