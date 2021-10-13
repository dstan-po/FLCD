class SymbolTable:
	def __init__(self, length):
		self.hash_table = [[] for array in range(length)]

	def insert(self, key, value):
		hash_key = self.hashFunction(key)
		key_exists = False
		key_values = self.hash_table[hash_key]

		for index, kv in enumerate(key_values):
			k, v = kv
			if key == k:
				key_exists = True 
				break

		if key_exists:
			key_values[index] = ((key, value))
		else:
			key_values.append((key, value))

		return (key, value)

	def hashFunction(self, key):
		return hash(key) % len(self.hash_table)

	def search(self, key):
		hash_key = self.hashFunction(key)
		key_values = self.hash_table[hash_key]

		for index, kv in enumerate(key_values):
			k, v = kv
			if key == k:
				return v

	def addSymbol(self, value):
		return self.insert(value, value)

i = SymbolTable(15)
print(i.hash_table)
print(i.addSymbol("a"))
print(i.addSymbol("a"))
print(i.addSymbol("b"))
print(i.hash_table)