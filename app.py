from flask import Flask
from flask_restful import Api
from flask_jwt import JWT
from Resources.User import UserResgister
from Resources.Item import Item, ItemList
from Resources.Store import Store, StoreList

from Auth.Security import authenticate, identity

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.secret_key = 'efrain'
api = Api(app)


# si queremos cambiar la ruta por defecto del token osea '/auth'
# usamos la linea de codigo debajo y la igualamos a la ruta que deseamos

# app.config['JWT_AUTH_URL_RULE'] = '/login'

# Con esto se configura el tiempo de vida del token 1800 es media hora
# por defecto es solamente 5 minutos
# app.config['JWT_EXPIRATION_DELTA'] = timedelta(seconds=1800)

# configuramos al JWT que en vez de que el key sea 'username' lo cambiamos al que deseamos
# en este casp del ejemplo de abajo es 'email'
# por defecto el nombre es 'username'
# app.config['JWT_AUTH_USERNAME_KEY'] = 'email'

# ----------------------------------------------------

# cuando llamamos a /auth mandamos la clave y el usuario y se la manda al authenticate
# luego devuelve un token si lo encuentra, y lo mandamos al siguiente request
jwt = JWT(app, authenticate, identity)  # /auth


# SI deseamos utilizar el identity para mostrar datos en el response del login
# utilizamos este metodo para cambiar el cuerpo del response con el token
# con el identity solo muestras la data del usuario definida en el modelo
# y el access token con este metodo le puede cambiar el nombre
# @jwt.auth_response_handler
# def customized_response_handler(access_token, identity):
#     return jsonify({
#                         'token': access_token.decode('utf-8'),
#                         'user_id': identity.id
#                    })


@app.before_first_request
def create_tables():
    db.create_all()

api.add_resource(Item, '/item/<string:name>')
api.add_resource(StoreList, '/stores')
api.add_resource(Store, '/store/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(UserResgister, '/register')

if __name__ == '__main__':
    from db import db
    db.init_app(app)
    app.run(debug=True)
