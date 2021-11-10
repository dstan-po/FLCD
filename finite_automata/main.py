class FiniteAutomata:
	INITIAL_STATE = "initial_state"
	TRANSITION_FUNCTION = "transition_function"
	INPUT_SYMBOLS = "input_symbols"
	STATES = "states"
	FINAL_STATES = "final_states"

	VALID_COMMANDS = [0, 1, 2, 3, 4, 5]

	def __init__(self):
		self.elements = {self.STATES: [], self.INPUT_SYMBOLS: [], self.INITIAL_STATE: None, self.FINAL_STATES: [],
						 self.TRANSITION_FUNCTION: {}}

	def read_finite_automata(self, filename: str):
		file = open(filename, "r")
		line = file.readline()
		while line:
			element_name = 0
			elements = 1

			line_elements = line.split(":")
			if line_elements[element_name] == self.INITIAL_STATE:
				self.elements[self.INITIAL_STATE] = line_elements[1].replace("\n", "")
			elif line_elements[element_name] == self.TRANSITION_FUNCTION:
				transitions = line_elements[elements].split(";")
				for transition in transitions:
					destination = transition.split("->")[1]
					starting_point = (transition.split(",")[0][1], transition.split(",")[1][0])
					self.elements[self.TRANSITION_FUNCTION][starting_point] = destination
			else:
				for value in line_elements[elements].split(","):
					self.elements[line_elements[element_name]].append(value.replace("\n", ""))

			line = file.readline()
		file.close()

	def print_menu(self):
		print("Input a number to execute the commands: ")
		print("1. Print set of states")
		print("2. Print alphabet")
		print("3. Print transitions")
		print("4. Print set of final states")
		print("5. Verify sequence")
		print("0. Exit")

	def display_list(self, symbols_list, title: str):
		print(title, end="")
		for state in symbols_list[:-1]:
			print(str(state) + ", ", end="")
		print(symbols_list[-1])

	def display_transitions(self, transitions: dict):
		print("Transitions: ")
		for transition in transitions.keys():
			print(str(transition) + " -> " + str(transitions[transition]))

	def read_and_check_sequence(self):
		print(self.validate_sequence(str(input("Sequence: ").upper())), end="\n\n")

	def validate_sequence(self, sequence: str):
		self.display_list(self.elements[self.FINAL_STATES], "Set of final states: ")
		current_node = self.elements[self.INITIAL_STATE]

		for state in sequence:
			transition_function = (current_node, state)

			if transition_function in self.elements[self.TRANSITION_FUNCTION].keys():
				print(str(transition_function) + " -> ", end="")
				current_node = self.elements[self.TRANSITION_FUNCTION][transition_function][0]
				print(current_node)
			else:
				return "Invalid sequence: Could not find next step"

		if current_node in self.elements[self.FINAL_STATES]:
			return "Valid sequence"
		return "Invalid sequence: Invalid final state"

	def run(self):
		while True:
			self.print_menu()
			try:
				command = int(input("Command: "))
				if command not in self.VALID_COMMANDS:
					raise Exception("COMMAND NOT FOUND IN LIST")

				if command == 1:
					self.display_list(self.elements[self.STATES], "States: ")
				elif command == 2:
					self.display_list(self.elements[self.INPUT_SYMBOLS], "Alphabet: ")
				elif command == 3:
					self.display_transitions(self.elements[self.TRANSITION_FUNCTION])
				elif command == 4:
					self.display_list(self.elements[self.FINAL_STATES], "Set of final states: ")
				elif command == 5:
					self.read_and_check_sequence()
				elif command == 0:
					break
			except Exception as e:
				print(e)
				print("INVALID COMMAND")


if __name__ == '__main__':
	fa = FiniteAutomata()
	fa.read_finite_automata("finite_automata.in")
	fa.run()
