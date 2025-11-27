"""Constant folding and AST optimization for MiniPy."""

from typing import Optional
from ast_nodes import (
    ASTNode, Program, Assign, Print, If, While,
    BinOp, Number, Var, Statement, Expression
)


class Optimizer:
    """Performs constant folding and simple optimizations."""
    
    def optimize(self, node: ASTNode) -> ASTNode:
        """Optimize an AST node."""
        if isinstance(node, Program):
            return self.optimize_program(node)
        elif isinstance(node, Assign):
            return self.optimize_assign(node)
        elif isinstance(node, Print):
            return self.optimize_print(node)
        elif isinstance(node, If):
            return self.optimize_if(node)
        elif isinstance(node, While):
            return self.optimize_while(node)
        elif isinstance(node, BinOp):
            return self.optimize_binop(node)
        else:
            return node
    
    def optimize_program(self, node: Program) -> Program:
        """Optimize a program."""
        optimized_statements = [self.optimize(stmt) for stmt in node.statements]
        return Program(optimized_statements)
    
    def optimize_assign(self, node: Assign) -> Assign:
        """Optimize assignment."""
        optimized_expr = self.optimize(node.expr)
        return Assign(node.name, optimized_expr, node.line)
    
    def optimize_print(self, node: Print) -> Print:
        """Optimize print statement."""
        optimized_expr = self.optimize(node.expr)
        return Print(optimized_expr, node.line)
    
    def optimize_if(self, node: If) -> If:
        """Optimize if statement."""
        optimized_cond = self.optimize(node.cond)
        
        # Constant folding: if condition is constant, eliminate branch
        if isinstance(optimized_cond, Number):
            if optimized_cond.value != 0:  # True
                # Always take then branch
                optimized_then = [self.optimize(stmt) for stmt in node.then_body]
                return If(optimized_cond, optimized_then, None, node.line)
            else:  # False
                # Always take else branch
                if node.else_body:
                    optimized_else = [self.optimize(stmt) for stmt in node.else_body]
                    return If(optimized_cond, [], optimized_else, node.line)
                return If(optimized_cond, [], None, node.line)
        
        optimized_then = [self.optimize(stmt) for stmt in node.then_body]
        optimized_else = [self.optimize(stmt) for stmt in node.else_body] if node.else_body else None
        return If(optimized_cond, optimized_then, optimized_else, node.line)
    
    def optimize_while(self, node: While) -> While:
        """Optimize while loop."""
        optimized_cond = self.optimize(node.cond)
        
        # Constant folding: if condition is always false, remove loop
        if isinstance(optimized_cond, Number) and optimized_cond.value == 0:
            return While(optimized_cond, [], node.line)
        
        optimized_body = [self.optimize(stmt) for stmt in node.body]
        return While(optimized_cond, optimized_body, node.line)
    
    def optimize_binop(self, node: BinOp) -> Expression:
        """Optimize binary operation with constant folding."""
        left = self.optimize(node.left)
        right = self.optimize(node.right)
        
        # Constant folding: both operands are numbers
        if isinstance(left, Number) and isinstance(right, Number):
            result = self.evaluate_constants(left.value, node.op, right.value)
            if result is not None:
                return Number(result, node.line)
        
        # Simple optimizations
        if node.op == "+":
            # x + 0 → x
            if isinstance(right, Number) and right.value == 0:
                return left
            # 0 + x → x
            if isinstance(left, Number) and left.value == 0:
                return right
        elif node.op == "*":
            # x * 1 → x
            if isinstance(right, Number) and right.value == 1:
                return left
            # 1 * x → x
            if isinstance(left, Number) and left.value == 1:
                return right
            # x * 0 → 0
            if (isinstance(left, Number) and left.value == 0) or \
               (isinstance(right, Number) and right.value == 0):
                return Number(0, node.line)
        elif node.op == "-":
            # x - 0 → x
            if isinstance(right, Number) and right.value == 0:
                return left
        
        return BinOp(left, node.op, right, node.line)
    
    def evaluate_constants(self, left: int, op: str, right: int) -> Optional[int]:
        """Evaluate constant expression."""
        try:
            if op == "+":
                return left + right
            elif op == "-":
                return left - right
            elif op == "*":
                return left * right
            elif op == "/":
                if right == 0:
                    return None  # Division by zero
                return left // right
            elif op == "<":
                return 1 if left < right else 0
            elif op == ">":
                return 1 if left > right else 0
            elif op == "<=":
                return 1 if left <= right else 0
            elif op == ">=":
                return 1 if left >= right else 0
            elif op == "==":
                return 1 if left == right else 0
            elif op == "!=":
                return 1 if left != right else 0
        except:
            return None
        return None

