from flask import Blueprint, request, jsonify, render_template
from helpers import token_required
from models import db, User, Wine, wine_schema, wines_schema

api = Blueprint('api',__name__, url_prefix='/api')


@api.route('/wine', methods = ['POST'])
@token_required
def add_wine(current_user_token):
    name = request.json['name']
    country = request.json['country']
    region = request.json['region']
    vintage = request.json['vintage']
    taste = request.json['taste']
    nose = request.json['nose']
    price = request.json['price']
    img = request.json['img']
    user_token = current_user_token.token

    print(f'BIG TESTER: {current_user_token.token}')

    wine = Wine(name, country, region, vintage, taste, nose, price, img, user_token = user_token )

    db.session.add(wine)
    db.session.commit()

    response = wine_schema.dump(wine)
    return jsonify(response)

# GET ALL WINES ENDPOINT
@api.route('/wine', methods = ['GET'])
@token_required
def get_wine(current_user_token):
    owner = current_user_token.token
    wines = Wine.query.filter_by(user_token = owner).all()
    response = wines_schema.dump(wines)
    return jsonify(response)

# GET A SINGLE WINE ENDPOINT
@api.route('/wine/<id>', methods = ['GET'])
@token_required
def get_single_wine(current_user_token, id):
    owner = current_user_token.token
    if owner == current_user_token.token:
        wine = Wine.query.get(id)
        response = wine_schema.dump(wine)
        return jsonify(response)
    else:
        return jsonify({"message": "Valid Token Required"}),401

# UPDATE WINE ENDPOINT
@api.route('/wine/<id>', methods = ['POST','PUT'])
@token_required
def update_contact(current_user_token,id):
    wine = Wine.query.get(id)
    wine.name = request.json['name']
    wine.country = request.json['country']
    wine.region = request.json['region']
    wine.vintage = request.json['vintage']
    wine.taste = request.json['taste']
    wine.nose = request.json['nose']
    wine.price = request.json['price']
    wine.img = request.json['img']
    wine.user_token = current_user_token.token

    db.session.commit()
    response = wine_schema.dump(wine)
    return jsonify(response)


# DELETE wine ENDPOINT
@api.route('/wine/<id>', methods = ['DELETE'])
@token_required
def delete_wine(current_user_token, id):
    wine = Wine.query.get(id)
    db.session.delete(wine)
    db.session.commit()
    response = wine_schema.dump(wine)
    return jsonify(response)
