"""Tree-walk interpreter for MiniPy (baseline for comparison with VM)."""

from ast_nodes import Program, Assign, Print, If, While, BinOp, Number, Var
from errors import SemanticError


class Interpreter:
    """Tree-walk interpreter that directly executes AST."""
    
    def __init__(self):
        self.globals = {}
    
    def interpret(self, node):
        """Interpret an AST node."""
        if isinstance(node, Program):
            return self.interpret_program(node)
        elif isinstance(node, Assign):
            return self.interpret_assign(node)
        elif isinstance(node, Print):
            return self.interpret_print(node)
        elif isinstance(node, If):
            return self.interpret_if(node)
        elif isinstance(node, While):
            return self.interpret_while(node)
        elif isinstance(node, BinOp):
            return self.interpret_binop(node)
        elif isinstance(node, Number):
            return self.interpret_number(node)
        elif isinstance(node, Var):
            return self.interpret_var(node)
        else:
            raise ValueError(f"Unknown node type: {type(node)}")
    
    def interpret_program(self, node):
        """Interpret a program."""
        for stmt in node.statements:
            self.interpret(stmt)
        return self.globals
    
    def interpret_assign(self, node):
        """Interpret assignment."""
        value = self.interpret(node.expr)
        self.globals[node.name] = value
        return value
    
    def interpret_print(self, node):
        """Interpret print statement."""
        value = self.interpret(node.expr)
        print(value)
        return value
    
    def interpret_if(self, node):
        """Interpret if statement."""
        cond = self.interpret(node.cond)
        if cond != 0:  # True
            for stmt in node.then_body:
                self.interpret(stmt)
        else:
            if node.else_body:
                for stmt in node.else_body:
                    self.interpret(stmt)
        return None
    
    def interpret_while(self, node):
        """Interpret while loop."""
        while True:
            cond = self.interpret(node.cond)
            if cond == 0:  # False
                break
            for stmt in node.body:
                self.interpret(stmt)
        return None
    
    def interpret_binop(self, node):
        """Interpret binary operation."""
        left = self.interpret(node.left)
        right = self.interpret(node.right)
        
        if node.op == "+":
            return left + right
        elif node.op == "-":
            return left - right
        elif node.op == "*":
            return left * right
        elif node.op == "/":
            if right == 0:
                raise ValueError("Division by zero")
            return left // right  # Integer division
        elif node.op == "<":
            return 1 if left < right else 0
        elif node.op == ">":
            return 1 if left > right else 0
        elif node.op == "==":
            return 1 if left == right else 0
        else:
            raise ValueError(f"Unknown operator: {node.op}")
    
    def interpret_number(self, node):
        """Interpret number literal."""
        return node.value
    
    def interpret_var(self, node):
        """Interpret variable reference."""
        if node.name not in self.globals:
            raise SemanticError(f"Undefined variable: {node.name}")
        return self.globals[node.name]


def interpret_ast(ast):
    """Convenience function to interpret an AST."""
    interpreter = Interpreter()
    return interpreter.interpret(ast)

