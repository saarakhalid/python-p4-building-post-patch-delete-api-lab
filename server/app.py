from flask import Flask, request, jsonify
from flask_migrate import Migrate
from models import db, Bakery, BakedGood

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)
db.init_app(app)

@app.route('/baked_goods', methods=['POST'])
def create_baked_good():
    data = request.form
    name = data.get('name')
    price = data.get('price')
    bakery_id = data.get('bakery_id')

    if not name or not price or not bakery_id:
        return jsonify({'error': 'Missing data. Please provide name, price, and bakery_id'}), 400

    try:
        baked_good = BakedGood(name=name, price=price, bakery_id=bakery_id)
        db.session.add(baked_good)
        db.session.commit()
        return jsonify(baked_good.to_dict()), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/bakeries/<int:id>', methods=['PATCH'])
def update_bakery(id):
    data = request.form
    bakery = Bakery.query.get(id)

    if not bakery:
        return jsonify({'error': 'Bakery not found'}), 404

    name = data.get('name')
    if name:
        bakery.name = name

    try:
        db.session.commit()
        return jsonify(bakery.to_dict()), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/baked_goods/<int:id>', methods=['DELETE'])
def delete_baked_good(id):
    baked_good = BakedGood.query.get(id)

    if not baked_good:
        return jsonify({'error': 'Baked good not found'}), 404

    try:
        db.session.delete(baked_good)
        db.session.commit()
        return jsonify({'message': 'Baked good deleted successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(port=5555, debug=True)