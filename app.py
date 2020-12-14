from flask import Flask, request, jsonify, render_template
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from flask_cors import CORS
from models import db, User, Address

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['DEBUG'] = True
app.config['ENV'] = 'development'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
db.init_app(app)
Migrate(app, db)
manager = Manager(app)
manager.add_command("db", MigrateCommand)

@app.route("/")
def root():
    return render_template('index.html')

@app.route("/users/search/", methods=['POST'])
def search(name=None, gender=None, address=None):
    if request.method == 'POST':
        name = request.json.get('name', None)
        gender = request.json.get('gender', None)
        address = request.json.get('address', None)

        if name and gender and address:
            users = User.query.filter(User.name.like('%'+name+'%'), User.gender==gender).join(User.addresses).filter(Address.address.like('%'+address+'%')).all()
            users = list(map(lambda user: user.serialize(), users))
            return jsonify(users), 200
        elif name and address:
            users = User.query.filter(User.name.like('%'+name+'%')).join(User.addresses).filter(Address.address.like('%'+address+'%')).all()
            users = list(map(lambda user: user.serialize(), users))
            return jsonify(users), 200
        elif gender and address:
            users = User.query.filter(User.gender==gender).join(User.addresses).filter(Address.address.like('%'+address+'%')).all()
            users = list(map(lambda user: user.serialize(), users))
            return jsonify(users), 200
        elif name:
            users = User.query.filter(User.name.like('%'+name+'%')).all()
            users = list(map(lambda user: user.serialize(), users))
            return jsonify(users), 200
        elif gender:
            users = User.query.filter(User.gender==gender).all()
            users = list(map(lambda user: user.serialize(), users))
            return jsonify(users), 200
        elif address:
            users = User.query.join(User.addresses).filter(Address.address.like('%'+address+'%')).all()
            users = list(map(lambda user: user.serialize(), users))
            return jsonify(users), 200
        else:
            users = User.query.all()
            users = list(map(lambda user: user.serialize(), users))
            return jsonify(users), 200

if __name__ == "__main__":
    manager.run()