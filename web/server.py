from flask import Flask,render_template, request, session, Response, redirect
from database import connector
from model import entities
import json

db = connector.Manager()
engine = db.createEngine()

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/users')
def users():
    db_session = db.getSession(engine)
    user = db_session.query(entities.User)
    data = user[:]
    #Esta repsuesta va al cliente en Json con MINETYPE, y puede ver el formato del contenido y mostrarlo
    return Response(json.dumps(data, cls=connector.AlchemyEncoder), mimetype = 'application/json')

@app.route('/users/<id>',methods = ['GET'])
def get_user(id):
    db_session = db.getSession(engine)
    users = db_session.query(entities.User).filter(entities.User.id==id)
    for user in users:
        js = json.dumps(user,cls=connector.AlchemyEncoder)
        return Response(js, status=200, mimetype='application/json')
    message = {"status":404, "message":"Not Found"}
    return Response(message, status=404, mimetype='application/json')


@app.route('/create_user', methods = ['GET'])
def create_test_books():
    db_session = db.getSession(engine)
    userdavid = entities.User(codigo=201810015, nombre="Nuevo Alumno" , apellido="Nuevo Apelldio", password="123")
    db_session.add(userdavid)
    db_session.commit()
    return "User Create DAVLP!"

@app.route('/create_mensaje', methods = ['GET'])
def create_test_mensaje():
    db_session = db.getSession(engine)
    userdavid = entities.Mensaje(texto="Holi wiii", datetime="2019-05-22" , estado="leido", user_enula=1,user_recibe=2)
    db_session.add(userdavid)
    db_session.commit()
    return "Mensaje Create DAVLP!"


if __name__ == '__main__':
    app.secret_key = ".."
    app.run(debug=True,)

