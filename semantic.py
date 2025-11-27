"""Semantic analysis and type checking for MiniPy."""

from typing import Dict, Optional, List, Set
from dataclasses import dataclass
from ast_nodes import (
    ASTNode, Program, Assign, Print, If, While,
    BinOp, Number, Var, Statement, Expression
)
from errors import SemanticError


# Type system
class Type:
    """Base type class."""
    pass


@dataclass(frozen=True)
class IntType(Type):
    """Integer type."""
    pass


@dataclass(frozen=True)
class BoolType(Type):
    """Boolean type."""
    pass


@dataclass(frozen=True)
class ErrorType(Type):
    """Error type for type checking failures."""
    pass


# Type constants
INT = IntType()
BOOL = BoolType()
ERROR = ErrorType()


@dataclass
class VariableInfo:
    """Information about a variable."""
    name: str
    type: Type
    declared: bool
    line: int


class Scope:
    """Represents a variable scope."""
    
    def __init__(self, parent: Optional['Scope'] = None):
        self.parent = parent
        self.variables: Dict[str, VariableInfo] = {}
    
    def declare(self, name: str, var_type: Type, line: int) -> None:
        """Declare a variable in this scope."""
        if name in self.variables:
            raise SemanticError(f"Variable '{name}' already declared in this scope", line)
        self.variables[name] = VariableInfo(name, var_type, True, line)
    
    def lookup(self, name: str) -> Optional[VariableInfo]:
        """Look up a variable, checking parent scopes."""
        if name in self.variables:
            return self.variables[name]
        if self.parent:
            return self.parent.lookup(name)
        return None
    
    def update(self, name: str, var_type: Type, line: int) -> None:
        """Update variable type (for assignment to existing variable)."""
        var_info = self.lookup(name)
        if var_info is None:
            raise SemanticError(f"Variable '{name}' used before declaration", line)
        # Update the variable in the scope where it was declared
        if name in self.variables:
            self.variables[name] = VariableInfo(name, var_type, True, line)
        elif self.parent:
            self.parent.update(name, var_type, line)


class SemanticAnalyzer:
    """Performs semantic analysis and type checking."""
    
    def __init__(self):
        self.current_scope: Scope = Scope()
        self.errors: List[SemanticError] = []
    
    def analyze(self, node: ASTNode) -> Type:
        """Analyze an AST node and return its type."""
        if isinstance(node, Program):
            return self.analyze_program(node)
        elif isinstance(node, Assign):
            return self.analyze_assign(node)
        elif isinstance(node, Print):
            return self.analyze_print(node)
        elif isinstance(node, If):
            return self.analyze_if(node)
        elif isinstance(node, While):
            return self.analyze_while(node)
        elif isinstance(node, BinOp):
            return self.analyze_binop(node)
        elif isinstance(node, Number):
            return self.analyze_number(node)
        elif isinstance(node, Var):
            return self.analyze_var(node)
        else:
            return ERROR
    
    def analyze_program(self, node: Program) -> Type:
        """Analyze a program."""
        for stmt in node.statements:
            self.analyze(stmt)
        return ERROR  # Program has no type
    
    def analyze_assign(self, node: Assign) -> Type:
        """Analyze assignment: check expr type and declare/update variable."""
        expr_type = self.analyze(node.expr)
        
        var_info = self.current_scope.lookup(node.name)
        if var_info is None:
            # New variable declaration
            if expr_type == ERROR:
                return ERROR
            self.current_scope.declare(node.name, expr_type, node.line)
        else:
            # Assignment to existing variable
            if expr_type != var_info.type:
                self.errors.append(SemanticError(
                    f"Type mismatch: cannot assign {expr_type} to {var_info.type} variable '{node.name}'",
                    node.line
                ))
                return ERROR
            self.current_scope.update(node.name, expr_type, node.line)
        
        return expr_type
    
    def analyze_print(self, node: Print) -> Type:
        """Analyze print statement."""
        expr_type = self.analyze(node.expr)
        if expr_type == ERROR:
            return ERROR
        return ERROR  # Print has no return type
    
    def analyze_if(self, node: If) -> Type:
        """Analyze if statement."""
        cond_type = self.analyze(node.cond)
        if cond_type != BOOL:
            self.errors.append(SemanticError(
                f"Condition must be bool, got {cond_type}",
                node.line
            ))
        
        # Analyze then body in new scope
        old_scope = self.current_scope
        self.current_scope = Scope(old_scope)
        for stmt in node.then_body:
            self.analyze(stmt)
        self.current_scope = old_scope
        
        # Analyze else body in new scope
        if node.else_body:
            self.current_scope = Scope(old_scope)
            for stmt in node.else_body:
                self.analyze(stmt)
            self.current_scope = old_scope
        
        return ERROR  # If has no return type
    
    def analyze_while(self, node: While) -> Type:
        """Analyze while loop."""
        cond_type = self.analyze(node.cond)
        if cond_type != BOOL:
            self.errors.append(SemanticError(
                f"Condition must be bool, got {cond_type}",
                node.line
            ))
        
        # Analyze body in new scope
        old_scope = self.current_scope
        self.current_scope = Scope(old_scope)
        for stmt in node.body:
            self.analyze(stmt)
        self.current_scope = old_scope
        
        return ERROR  # While has no return type
    
    def analyze_binop(self, node: BinOp) -> Type:
        """Analyze binary operation."""
        left_type = self.analyze(node.left)
        right_type = self.analyze(node.right)
        
        # Arithmetic operations require int operands
        if node.op in ("+", "-", "*", "/"):
            if left_type != INT or right_type != INT:
                self.errors.append(SemanticError(
                    f"Arithmetic operation '{node.op}' requires int operands, got {left_type} and {right_type}",
                    node.line
                ))
                return ERROR
            return INT
        
        # Comparison operations
        if node.op in ("<", ">", "<=", ">="):
            if left_type != INT or right_type != INT:
                self.errors.append(SemanticError(
                    f"Comparison '{node.op}' requires int operands, got {left_type} and {right_type}",
                    node.line
                ))
                return ERROR
            return BOOL
        
        # Equality operations
        if node.op in ("==", "!="):
            if left_type != right_type:
                self.errors.append(SemanticError(
                    f"Equality '{node.op}' requires compatible types, got {left_type} and {right_type}",
                    node.line
                ))
                return ERROR
            return BOOL
        
        return ERROR
    
    def analyze_number(self, node: Number) -> Type:
        """Analyze number literal."""
        return INT
    
    def analyze_var(self, node: Var) -> Type:
        """Analyze variable reference."""
        var_info = self.current_scope.lookup(node.name)
        if var_info is None:
            self.errors.append(SemanticError(
                f"Undefined variable: {node.name}",
                node.line
            ))
            return ERROR
        return var_info.type
    
    def check(self, node: Program) -> List[SemanticError]:
        """Run semantic analysis and return list of errors."""
        self.errors = []
        self.current_scope = Scope()
        self.analyze(node)
        return self.errors

