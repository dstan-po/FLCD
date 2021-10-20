'''
Git: https://github.com/dstan-po/FLCD/tree/master/lab_2

The symbol table implements a hash map with chaining.

Hashing:
	The formula for hashing is:
		hash(value) % size_of_hash_table
	hash() being the python hash function

Searching a symbol:
	The name of the symbol is given as a parameter.

	Calculate the hash value of the symbol.

	The hash value is used find the position in the hash map,
	then the symbol is searched in the obtained list:
		If the symbol is found:
			return the tuple (hash value, position in list)
		If the symbol is not found:
			return None

Adding a symbol:
	If name of the symbol is given as a parameter.

	Calculate the hash value of the symbol.

	The symbol is searched in the table:
		If the symbol is not found:
			Append to the list on the hash value position and return (hash value, position in list)
		If the symbol is found:
			return the result of the search (hash value, position in list)
'''

class SymbolTable:
	def __init__(self, length):
		self.length = length
		self.hash_table = [[] for array in range(length)]

	def hashFunction(self, key):
		return hash(key) % self.length

	def search(self, key):
		hash_key = self.hashFunction(key)
		try:
			return (hash_key, self.hash_table[hash_key].index(key))
		except Exception:
			return None

	def addSymbol(self, value):
		hash_key = self.hashFunction(value)
		search_result = self.search(value)

		if search_result == None:
			self.hash_table[hash_key].append(value)
			return (hash_key, self.hash_table[hash_key].index(value))
		else:
			return search_result
