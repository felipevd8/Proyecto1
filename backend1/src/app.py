
from flask import Flask,request,jsonify                                 ##.\venv\Scripts\activate.bat --- mongod para iniciar la bdd -- mongo para conectarse --python src/app.py para iniciar el servidor de la apg
from flask_pymongo import PyMongo, ObjectId
from flask_cors import CORS

app = Flask(__name__)                                                   ##la variable app(python) es de tipo Flask(__name__)  
app.config['MONGO_URI']='mongodb://localhost/BDDproyecto1'              ##la variable llama a un metodo .config para la url de la bdd o server y crea la carpeta
mongo = PyMongo(app)                                                    ## conexion de la BDD

db = mongo.db.users

@app.route('/')
def index():
        return 'HOLAS'
        
@app.route('/users', methods = ['POST'])
def createUser():
    id = db.insert({
        'name': request.json['name'],
        'email': request.json['email'],
        'password': request.json['password']
    })
    return jsonify(str(ObjectId(id)))                                   ##METODO jsonify para mostrar valores

@app.route('/users', methods = ['GET'])
def getUsers():
        users = []
        for doc in db.find():                                           ##consulta a la BDD
                users.append({                                          ##llenado de lista
                        '_id': str(ObjectId(doc['_id'])),               ##id a ObjectId-> string
                        'name' : doc['name'],
                        'email' : doc['email'],
                        'password' : doc['password']
                })  
        return jsonify(users)

@app.route('/user/<id>', methods = ['GET'])
def getUser(id):
        user = db.find_one({'_id': ObjectId(id)})                        ## compara _id con la id q recibe<id> convertida en ObjectId--USER es una clase
        print (user)
        return jsonify({                                                 ##rellena con los datos de user
                '_id': str(ObjectId(user['_id'])),
                'name' : user['email'],
                'email' : user['email'],
                'password' : user['password']
                
        })

@app.route('/users/<id>', methods = ['DELETE'])
def deleteUser(id):
        db.delete_one({'_id': ObjectId(id)})
        return jsonify('Cliente borrado correctamente')     

@app.route('/users/<id>', methods = ['PUT'])
def updateUser(id):
        db.update_one({'_id': ObjectId(id)}, {'$set': {
                'name': request.json['name'],
                'email': request.json['email'],
                'password': request.json['password']
        }})
        return jsonify ('Usuario actualizado')

if __name__ == "__main__":
    app.run(debug=True)