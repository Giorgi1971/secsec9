import sqlite3
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel

class Item(Resource):
	parser = reqparse.RequestParser() # პარსეწრი არის RequestParser-ის ობიექტი
	parser.add_argument('price', # Parser ობიექტს ვამატებთ მხოლოდ 'price'-ს
			type = float,
			required = True,
			help = 'This field cannot be left blank'
		)
	parser.add_argument('store_id', # Parser ობიექტს ვამატებთ მხოლოდ 'price'-ს
			type = int,
			required = True,
			help = 'Every Item need store_id'
		)

	@jwt_required()
	def get(self, name):
		item = ItemModel.find_by_name(name)
		if item:
			return item.json()
		return {'message:':'item not found.'}


	def post(self, name):
		if ItemModel.find_by_name(name):  #  is not None
			return {'message': 'An item with name {} already exists'.format(name)}, 400

		data = Item.parser.parse_args()

		item = ItemModel(name, data['price'], data['store_id'])
		try:
			item.save_to_db()
		except:
			return {'message:':'An error occurred inserting the item'}, 500 #internal server error
		return item.json(), 201


	def delete(self, name):
		item = ItemModel.find_by_name(name)
		if item:
			item.delete_from_db()
			return {'message': 'item deleted, Yesss QSLAchemy'}
		return {'message': 'item not found'}, 404

	def put(self, name):
		data = Item.parser.parse_args()

		item = ItemModel.find_by_name(name)

		if item:
			item.price = data['price']
		else:
			item = ItemModel(name, data['price'], data['store_id'])
		item.save_to_db()

		return item.json()


class ItemList(Resource):
	def get(self):
		return {'Items:': [item.json() for item in ItemModel.query.all()]}