"""
This script runs the application using a development server.
It contains the definition of routes and views for the application.
"""

from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_sqlalchemy  import Column, Integer, String, Float

app = Flask(__name__)

#SQLite path
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'planets.db')

#Initialize db
db = SQLAlchemy


#create database
@app.cli.command('db_create')
def db_create():
    db.create_all()
    print('Database created')

#delete database
@app.cli.command('db-drop')
def db_drop():
    db.drop_all()
    print('Database dropped')

@app.cli.command
def db_seed():
    mercury = Planet(planet_name='Mercury', planet_type='Class D',
                     home_star='Sol', mass=3.238e223, radius = 1516,
                     distance = 35.98e5
                     )

    venus = Planet(planet_name='Venus', planet_type='Class K',
                     home_star='Sol', mass=4.867e24, radius = 3760,
                     distance = 67.24e6
                     )

    earth = Planet(planet_name='Earth', planet_type='Class M',
                     home_star='Sol', mass=5.9e24, radius = 3959,
                     distance = 92.96e6
                     )

#Add planets to db
db.session.add(mercury)
db.session.add(venus)
db.session.add(earth)

# Make the WSGI interface available at the top level so wfastcgi can get it.
wsgi_app = app.wsgi_app

# default hello world route
@app.route('/')
def hello():
    """Renders a sample page."""
    return "Hello World!"

# Custom hello world route
@app.route('/super_simple')
def super_simple():
    return jsonify(message="Hello From Planetary API"), 200

#Not found route
@app.route('/not_found')
def not_found():
    return jsonify(message="That resource is not found"), 404

# How to use parameters route
@app.route('/parameters')
def parameters():
    name = request.args.get('name')
    age = int(request.args.get('age'))
    if age < 18:
        return jsonify(message="Sorry " + name + ", you are not old enough"), 401
    else:
        return jsonify(message="Welcome " + name + ", you are old enough")

## How to use variables route
@app.route('/url_variables/<string:name>/<int:age>')
def url_variables(name:str, age:int):
      if age < 18:
        return jsonify(message="Sorry " + name + ", you are not old enough"), 401
      else:
        return jsonify(message="Welcome " + name + ", you are old enough")


# database models
class User(db.Model):
    __tablename__ = "users"
    id: Column(Integer, primary_key=True);
    first_name: Column(String)
    last_name: Column(String)
    email: Column(String, unique=True)
    password: Column(String)


#database planets
class Planet(db.Model):
    __tablename__ = "planets"
    planet_id: Column(Integer, primary_key=True)
    planet_name:Column(String)
    planet_type: Column(String)
    home_star: Column(String)
    mass: Column(Float)
    radius: Column(Float)
    distance: Column(Float)


if __name__ == '__main__':
    import os
    HOST = os.environ.get('SERVER_HOST', 'localhost')
    try:
        PORT = int(os.environ.get('SERVER_PORT', '5555'))
    except ValueError:
        PORT = 5555
    app.run(HOST, PORT)
