import re


def contains(list, filter):
	for x in list:
		if filter(x):
			return x
	return None


class SymbolTable:
	def __init__(self, length=30):
		self.length = length
		self.hash_table = [[] for array in range(length)]

	def hashFunction(self, key):
		stringed_key = str(key)
		char_sum = 0
		for char in enumerate(stringed_key):
			char_sum += ord(char[1])
		return char_sum % self.length

	def search(self, key):
		hash_key = self.hashFunction(key)
		try:
			return hash_key, self.hash_table[hash_key].index(key)
		except Exception:
			return None

	def addSymbol(self, value):
		hash_key = self.hashFunction(value)
		search_result = self.search(value)

		if search_result is None:
			self.hash_table[hash_key].append(value)
			return hash_key, self.hash_table[hash_key].index(value)
		else:
			return search_result


'''
PIF generation:
	The pif is generated using the tokens obtained from the scanning function.
	The symbols/keywords will always have the position -1 in the ST.
	The position in the symbol table is denoted as a tuple with the location.
	Constants will have the value "const" and the position in the symbol table.  
	The identifiers will have the value "id" and the position in the symbol table.
	
	If the token is not recognized then an exception with the following text will be thrown:
		ERROR ON LINE NR: {line_number} - TOKEN: {token} IS NOT VALID

Scanning:
	The source code is scanned line by line and the lines are separated in tokens

Tokenization:
	The text is taken character by character and builds a lexeme checking at every iteration if the current lexeme
	is part of the keywords/tokens
'''


class Scanner:
	symbols = ["\n", "+", "-", "*", "%", "/", "<", ">",
			   "<=", ">=", "=", "==", "!=", "!", ";", "#", "(", ")",
			   "&&", "||", "[", "]", "{", "}"]
	keywords = ["int", "string", "bool", "while", "for",
				"if", "else", "print", "read", "_START_COMPUTING_",
				"_STOP_COMPUTING_", "_STOP_DEC_"]
	white_space = " "
	KEYWORDS = symbols + keywords

	DEFAULT_ID = -1
	CONSTANT_NAME = "const"
	IDENTIFIER_NAME = "id"

	def __init__(self):
		self.symbol_table = SymbolTable()

	def get_tokens(self, code: str):
		tokens = []
		lexeme = ""
		i = 0
		while i < len(code):
			char = code[i]
			if char == "<" and code[i + 1] == "=":
				lexeme += "<="
				i += 1
			elif char == ">" and code[i + 1] == "=":
				lexeme += ">="
				i += 1
			elif char == "=" and code[i + 1] == "=":
				lexeme += "=="
				i += 1
			elif char == "!" and code[i + 1] == "=":
				lexeme += "!="
				i += 1
			elif char == "-" and code[i + 1] != " ":
				lexeme += char + code[i + 1]
				i += 1
			elif char != self.white_space:
				lexeme += char

			if i + 1 < len(code):
				if code[i + 1] == self.white_space or code[i + 1] in self.KEYWORDS or lexeme in self.KEYWORDS:
					if lexeme in self.keywords and code[i + 1] not in (" ", "(", "\n"):
						pass
					elif lexeme != '':
						lexeme = lexeme.replace("\t", "")
						if lexeme != '':
							tokens.append(lexeme)
						lexeme = ""
			i += 1

		return tokens

	def solve_pif(self, tokens: list, pif: list, line_number: int):
		numeric_regex = "^(0|[-]?[1-9][0-9]*)$"
		string_regex = "\"[a-zA-Z0-9]*\""
		variable_regex = "[a-zA-Z]+[0-9]*"

		for token in tokens:
			if token in self.KEYWORDS:
				pif.append((token, self.DEFAULT_ID))
			else:
				search_result = contains(pif, lambda item: item[0] == token)
				if search_result is not None:
					pif.append((token, search_result[1]))
				else:
					if bool(re.match(numeric_regex, token)):
						pif.append((self.CONSTANT_NAME, self.symbol_table.addSymbol(token)))
					elif bool(re.match(string_regex, token)):
						pif.append((self.CONSTANT_NAME, self.symbol_table.addSymbol(token)))
					elif bool(re.match(variable_regex, token)):
						pif.append((self.IDENTIFIER_NAME, self.symbol_table.addSymbol(token)))
					else:
						raise Exception(f"ERROR ON LINE NR: {line_number} - TOKEN: {token} IS NOT VALID")
		return pif

	def scan_file(self, file_name: str):
		program_file = open(file_name + ".txt", "r")
		line = program_file.readline()
		pif = []
		line_number = 0
		while line:
			pif = self.solve_pif(self.get_tokens(line), pif, line_number)
			line = program_file.readline()
			line_number += 1

		program_file.close()
		pif_file = open(file_name + "PIF.out", "w")
		for item in pif:
			pif_file.write(str(item[0]) + " " + str(item[1]) + "\n")
		pif_file.close()

		st_file = open(file_name + "ST.out", "w")
		i = 0
		while i < len(self.symbol_table.hash_table):
			current_element = self.symbol_table.hash_table[i]
			if len(current_element) != 0:
				j = 0
				while j < len(current_element):
					st_file.write(str((i, j)) + " " + str(current_element[j]) + "\n")
					j += 1
			i += 1
		st_file.close()

scanner = Scanner()
scanner.scan_file("p1")

scanner = Scanner()
scanner.scan_file("p2")

scanner = Scanner()
scanner.scan_file("p3")
