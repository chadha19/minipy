"""AST node classes for MiniPy."""

from dataclasses import dataclass
from typing import List, Optional, Union


class ASTNode:
    """Base class for all AST nodes."""
    pass


@dataclass
class Program(ASTNode):
    """Root node representing a complete program."""
    statements: List['Statement']
    
    def __repr__(self):
        return f"Program({len(self.statements)} statements)"


@dataclass
class Assign(ASTNode):
    """Assignment statement: name = expression"""
    name: str
    expr: 'Expression'
    line: int = 0
    
    def __repr__(self):
        return f"Assign({self.name}, {self.expr})"


@dataclass
class Print(ASTNode):
    """Print statement: print(expression)"""
    expr: 'Expression'
    line: int = 0
    
    def __repr__(self):
        return f"Print({self.expr})"


@dataclass
class If(ASTNode):
    """If statement: if cond: then_body else: else_body"""
    cond: 'Expression'
    then_body: List['Statement']
    else_body: Optional[List['Statement']] = None
    line: int = 0
    
    def __repr__(self):
        return f"If({self.cond}, {len(self.then_body)} stmts, else: {len(self.else_body) if self.else_body else 0} stmts)"


@dataclass
class While(ASTNode):
    """While loop: while cond: body"""
    cond: 'Expression'
    body: List['Statement']
    line: int = 0
    
    def __repr__(self):
        return f"While({self.cond}, {len(self.body)} stmts)"


@dataclass
class BinOp(ASTNode):
    """Binary operation: left op right"""
    left: 'Expression'
    op: str
    right: 'Expression'
    line: int = 0
    
    def __repr__(self):
        return f"BinOp({self.left}, {self.op}, {self.right})"


@dataclass
class Number(ASTNode):
    """Number literal."""
    value: int
    line: int = 0
    
    def __repr__(self):
        return f"Number({self.value})"


@dataclass
class Var(ASTNode):
    """Variable reference."""
    name: str
    line: int = 0
    
    def __repr__(self):
        return f"Var({self.name})"


# Type aliases for type hints
Statement = Union[Assign, Print, If, While]
Expression = Union[BinOp, Number, Var]

