from flask import Flask, request
from flask.wrappers import Request
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os

dir_path = os.path.dirname(__file__)
dotenv_path = os.path.join(dir_path, '.env')

load_dotenv(dotenv_path)
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'

db = SQLAlchemy(app)

class Drink(db.Model):
    id = db.Column(db.Integer, primary_key= True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    description  = db.Column(db.String(120))

    def __repr__(self):
        return f'{ self.name} - {self.description}'

@app.route('/')
def index():
    return {'hello': 'world'}

@app.route('/drinks')
def get_drinks():
    drinks = Drink.query.all()
    output = []
    for drink in drinks:
        drinks_data = {'name': drink.name, 'description': drink.description}
        output.append(drinks_data)
    return {'drinks': output}

@app.route('/drinks/<id>')
def get_drink(id):
    drink = Drink.query.get_or_404(id)
    return {'name': drink.name, 'description': drink.description}

@app.route('/delete/<id>', methods = ['DELETE'])
def delete_drink(id):
        drink = Drink.query.get(id)
        if drink is None:
            return {'message': 'Item not found'}
        else:
            db.session.delete(drink)
            db.session.commit()
            return {'message' : 'item deleted successfully'}

@app.route('/delete_all', methods = ['DELETE'])
def delete_all():
    db.session.query(Drink).delete()
    db.session.commit()
    return {'message': 'All the drinks in the DB deleted Successfully'}

@app.route('/drinks', methods = ['POST'])
def add_drink():
    new_drink = Drink(name=request.json['name'], description=request.json['description'])
    db.session.add(new_drink)
    db.session.commit()
    return {'message': f'{new_drink.name} added successfully'}

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)