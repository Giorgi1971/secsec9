from flask_restful import Resource
from models.store import StoreModel

class Store(Resource):
	def get(self, name):
		store = StoreModel.find_by_name(name)
		print(store)
		if store:
			return store.json()
		return {'message': 'store {} cannot be found'.format(name)}, 404 
		# ბოლო return აბრუნებს tuple-ს, და ხვდება რომ პიველი ნაწილი უნდა დაბრუნდეს body-ში 
		# და მეორე (404) არის სტატუს კოდი.

	def post(self, name):
		if StoreModel.find_by_name(name):
			return {'message': 'store {} already exists'.format(name)}, 400
		store = StoreModel(name)
		try:
			store.save_to_db()
		except:
			return {'message':'somthing went wrong'}, 500  # როცა არ ვიცით რა უნდა

		return store.json(), 201

	def delete(self, name):
		store = StoreModel.find_by_name(name)
		if store:
			store.delete_from_db()
			return {'message':"'{}' store was deleted".format(name)}
		else:
			return {'message': "Store '{}' not be found".format(name)}


class StoreList(Resource):
	def get(self):
		return {'Stores':[store.json() for store in StoreModel.query.all()]}
		# ან 