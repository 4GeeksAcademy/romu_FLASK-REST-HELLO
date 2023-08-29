"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/users', methods=['GET', 'POST'])
def handle_users():
    if request.method == 'GET':
        users = db.session.execute(db.select(User).orde_by(User.name)).scalars()
        results = [item.serialize() for item in users]
        response_body = {"message": "Devuelve le GET del endpoint /users",
                         "result": results,
                         "status": "ok"
                         }
        return response_body, 200
    if request.method == 'POST':
        request_body = request.get_json()
        user = User(email = request_body["email"],
                    password = request_body["password"],
                    name = request_body["name"],
                    phone = request_body["phone"])
        db.session.add(user)
        db.session.commit()
        print(request_body)
        response_body = {"message": "Adding new user",
                        "status": "ok",
                        "new_user": request_body}
        return response_body, 200

@app.route('/users/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def handle_user(id):
    if request.method == 'GET':
        user = db.get_or_404(User, id)
        print(user)
        response_body = {"status": "ok",
                         "results": user.serialize()}
        return response_body, 200
    if request.method == 'PUT':
        request_body = request.get_json()
        user = db.get_or_404(User, id)
        user.email = request_body["email"]
        user.password = request_body["password"]
        user.name = request_body["name"]
        user.phone = request_body["phone"]
        db.session.commit()
        response_body = {"message": "Update new user",
                        "status": "ok",
                        "new_user": request_body}
        return response_body, 200
    if request.method == 'DELETE':
        user = db.get_or_404(User, id)
        db.session.delete(user)
        db.session.commit()
        response_body = { "messega": "Deleting user",
                         "status": "ok",
                         "user delete": id}

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
