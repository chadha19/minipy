"""AST node classes for MiniPy."""


class ASTNode:
    """Base class for all AST nodes."""
    pass


class Program(ASTNode):
    """Root node representing a complete program."""
    def __init__(self, statements):
        self.statements = statements
    
    def __repr__(self):
        return f"Program({len(self.statements)} statements)"


class Assign(ASTNode):
    """Assignment statement: name = expression"""
    def __init__(self, name, expr):
        self.name = name
        self.expr = expr
    
    def __repr__(self):
        return f"Assign({self.name}, {self.expr})"


class Print(ASTNode):
    """Print statement: print(expression)"""
    def __init__(self, expr):
        self.expr = expr
    
    def __repr__(self):
        return f"Print({self.expr})"


class If(ASTNode):
    """If statement: if cond: then_body else: else_body"""
    def __init__(self, cond, then_body, else_body=None):
        self.cond = cond
        self.then_body = then_body
        self.else_body = else_body
    
    def __repr__(self):
        return f"If({self.cond}, {len(self.then_body)} stmts, else: {len(self.else_body) if self.else_body else 0} stmts)"


class While(ASTNode):
    """While loop: while cond: body"""
    def __init__(self, cond, body):
        self.cond = cond
        self.body = body
    
    def __repr__(self):
        return f"While({self.cond}, {len(self.body)} stmts)"


class BinOp(ASTNode):
    """Binary operation: left op right"""
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right
    
    def __repr__(self):
        return f"BinOp({self.left}, {self.op}, {self.right})"


class Number(ASTNode):
    """Number literal."""
    def __init__(self, value):
        self.value = value
    
    def __repr__(self):
        return f"Number({self.value})"


class Var(ASTNode):
    """Variable reference."""
    def __init__(self, name):
        self.name = name
    
    def __repr__(self):
        return f"Var({self.name})"

