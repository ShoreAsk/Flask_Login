# project/__init__.py

from flask import Flask
from flask.ext.bcrypt import Bcrypt
from flask.ext.sqlalchemy import SQLAlchemy
from project.config import BaseConfig


# config

app = Flask(__name__)
app.config.from_object(BaseConfig)

bcrypt = Bcrypt(app)
db = SQLAlchemy(app)


from flask import request, jsonify, session
from project.models import User


# routes

@app.route('/register', methods=['POST'])
def register():
    json_data = request.json
    user = User(first_name=json_data['first_name'],
                last_name=json_data['last_name'],
                email=json_data['email'],
                password=json_data['password'],
                team=json_data['team'],
                position=json_data['position']
                )
    try:
        db.session.add(user)
        db.session.commit()
        status = 'success'
    except:
        status = 'this user is already registered'
    db.session.close()
    return jsonify({'result': status})


@app.route('/login', methods=['POST'])
def login():
    json_data = request.json
    user = User.query.filter_by(email=json_data['email']).first()
    password = json_data['password']
    if user and bcrypt.check_password_hash(user.password, password):
        session['logged_in'] = True
        status = True
    else:
        status = False
    return jsonify({'result': status})



@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return jsonify({'result': 'success'})



@app.route('/status')
def status():
    if session.get('logged_in'):
        if session['logged_in']:
            return jsonify({'status': True})
    else:
        return jsonify({'status': False})
