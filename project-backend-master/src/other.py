"""Clears Global Variables:"""
from src.data_store import data_store
import json

def clear_v1():
	"""Clears all data from store"""
	store = data_store.get()
	store['users'].clear()
	store['channels'].clear()
	store['dm'].clear()
	store['threads'].clear()
	data_store.set(store)
	with open('database.json', 'w') as FILE:
		empty = {}
		json.dump(empty, FILE)
