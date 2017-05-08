# project/__init__.py

from flask import Flask
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user
from project.config import BaseConfig
from flask_cors import CORS, cross_origin
import json

# config

app = Flask(__name__)
app.config.from_object(BaseConfig)
CORS(app)

bcrypt = Bcrypt(app)
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)

from flask import request, jsonify, session
from project.models import User


# routes

@app.route('/register', methods=['POST'])
def register():
    string_json = request.data.decode("utf-8")
    json_data = json.loads(string_json)
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
    string_json = request.data.decode("utf-8")
    json_data = json.loads(string_json)
    user = User.query.filter_by(email=json_data['email']).first()
    password = json_data['password']
    if user and bcrypt.check_password_hash(user.password, password):
        login_user(user)
        result = {
            'id': user.id,
            'firstName': user.first_name,
            'lastName': user.last_name,
            'email': user.email,
            'token': session['_id']
        }
    else:
        result = {'error': 'Login failed'}
    return jsonify(result)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return jsonify({'result': 'success'})


@app.route('/status')
def check_status():
    # if 'username' in session:
    #     result = 'Logged in as ' + session['username']
    # else:
    #     result = 'You are not logged in'
    # return jsonify({'result': result})
    login_manager._load_user()
    if login_manager.current_user.is_authenticated():
        return True
    else:
        return False


# handle login failed
@app.errorhandler(401)
def page_not_found(e):
    return jsonify({'error': str(e)})


# callback to reload the user object
@login_manager.user_loader
def load_user(userid):
    return User(userid)


@app.route("/users")
@login_required
def getAllUsers():
    result = User.query.All()
    return jsonify({'json': result})
