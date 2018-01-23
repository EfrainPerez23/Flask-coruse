from werkzeug.security import safe_str_cmp
from Models.User import UserModel

def authenticate(username, password):
    user = UserModel.findByUserName(username)
    if user and safe_str_cmp(user.password, password):
        return user


# SE UTILIZA PARA RETORNAR LOS DATOS DEL USUARIO EN FUNCION A SU MODELO
# POR EJEMPLO payload['identity'] TOMA EL ID QUE ESTA EN EL JWTOKEN Y LUEGO
# LO BUSCAMOS EN LA BASE DATOS PARA OBTENER SUS DATOS
# Y PODEMOS CONFIGURAR QUE EN EL CUERPO DEL RESPONSE DE INIICAR SESION PODEMOS
# SOLICITAR CUALQUIER DATO DE LA TABLA QUE ESTA DEFINIDO EN EL MODELO
# POR EJEMPLO USER TIENE id, username, password. Nosotros en el response
# podemos pedir el id o el username o el password porque lo definimos en el modelo
# listo

def identity(payload):
    user_id = payload['identity']
    return UserModel.findById(user_id)