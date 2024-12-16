import re

class Interpreter:
    def __init__(self):
        self.variables = {}
        self.errors = []

    def parse_program(self, program):
        lines = program.strip().split(";")
        for line in lines:
            if line.strip():
                self.parse_assignment(line.strip())

    def parse_assignment(self, line):
        match = re.match(r'^([a-zA-Z_][a-zA-Z0-9_]*)\s*=\s*(.+)$', line)
        if not match:
            self.errors.append("error")
            return
        identifier, expression = match.groups()
        if not self.is_valid_identifier(identifier):
            self.errors.append("error")
            return
        try:
            value = self.evaluate_expression(expression)
            if value is None:
                self.errors.append("error")
            else:
                self.variables[identifier] = value
        except Exception:
            self.errors.append("error")

    def is_valid_identifier(self, identifier):
        return re.match(r'^[a-zA-Z_][a-zA-Z0-9_]*$', identifier) is not None

    def evaluate_expression(self, expression):
        # Replace variable names with their values
        def replace_vars(match):
            var_name = match.group(0)
            if var_name not in self.variables:
                raise ValueError(f"Uninitialized variable: {var_name}")
            return str(self.variables[var_name])

        expression = re.sub(r'[a-zA-Z_][a-zA-Z0-9_]*', replace_vars, expression)

        # Check for leading zeros in literals
        if re.search(r'\b0[0-9]', expression):
            raise ValueError("Leading zeros in literals are not allowed")

        try:
            value = eval(expression, {"__builtins__": None}, {})
            if not isinstance(value, int):
                raise ValueError("Expression must evaluate to an integer")
            return value
        except Exception:
            raise ValueError("Invalid expression")

    def run(self, program):
        self.variables.clear()
        self.errors.clear()
        self.parse_program(program)

        if self.errors:
            print("error")
        else:
            for var, val in self.variables.items():
                print(f"{var} = {val}")


# Test inputs
interpreter = Interpreter()

# Input 1
print("Input 1")
interpreter.run("x = 001;")
print()

# Input 2
print("Input 2")
interpreter.run("x_2 = 0;")
print()

# Input 3
print("Input 3")
interpreter.run("x = 0 y = x; z = ---(x+y);")
print()

# Input 4
print("Input 4")
interpreter.run("x = 1; y = 2; z = ---(x+y)*(x+-y);")