"""Compiler: converts AST to bytecode."""

from ast_nodes import Program, Assign, Print, If, While, BinOp, Number, Var
from bytecode import (
    Instruction, LOAD_CONST, LOAD_NAME, STORE_NAME, ADD, SUB, MUL, DIV,
    CMP_LT, CMP_GT, CMP_LE, CMP_GE, CMP_EQ, CMP_NEQ,
    JUMP, JUMP_IF_FALSE, JUMP_IF_TRUE, POP, PRINT, HALT
)
from semantic import SemanticAnalyzer
from optimizer import Optimizer


class Compiler:
    """Compiles AST to bytecode."""
    
    def __init__(self):
        self.code = []
        self.consts = []
        self.names = []
        self.const_map = {}  # Map values to indices
        self.name_map = {}  # Map names to indices
    
    def const_index(self, value):
        """Get or create constant index."""
        if value not in self.const_map:
            idx = len(self.consts)
            self.consts.append(value)
            self.const_map[value] = idx
        return self.const_map[value]
    
    def name_index(self, name):
        """Get or create name index."""
        if name not in self.name_map:
            idx = len(self.names)
            self.names.append(name)
            self.name_map[name] = idx
        return self.name_map[name]
    
    def emit(self, opcode, arg=None):
        """Emit an instruction."""
        self.code.append(Instruction(opcode, arg))
        return len(self.code) - 1
    
    def compile(self, node):
        """Compile an AST node."""
        if isinstance(node, Program):
            return self.compile_program(node)
        elif isinstance(node, Assign):
            return self.compile_assign(node)
        elif isinstance(node, Print):
            return self.compile_print(node)
        elif isinstance(node, If):
            return self.compile_if(node)
        elif isinstance(node, While):
            return self.compile_while(node)
        elif isinstance(node, BinOp):
            return self.compile_binop(node)
        elif isinstance(node, Number):
            return self.compile_number(node)
        elif isinstance(node, Var):
            return self.compile_var(node)
        else:
            raise ValueError(f"Unknown node type: {type(node)}")
    
    def compile_program(self, node):
        """Compile a program."""
        for stmt in node.statements:
            self.compile(stmt)
        self.emit(HALT)
        return self.code, self.consts, self.names
    
    def compile_assign(self, node):
        """Compile assignment: compile expr, then STORE_NAME"""
        self.compile(node.expr)
        name_idx = self.name_index(node.name)
        self.emit(STORE_NAME, name_idx)
    
    def compile_print(self, node):
        """Compile print: compile expr, then PRINT"""
        self.compile(node.expr)
        self.emit(PRINT)
    
    def compile_if(self, node):
        """Compile if: condition, JUMP_IF_FALSE else_label, then_body, JUMP end_label, else_body"""
        # Compile condition
        self.compile(node.cond)
        
        # Emit jump if false (to else or end)
        else_label_pos = self.emit(JUMP_IF_FALSE, None)  # Will patch later
        
        # Compile then body
        for stmt in node.then_body:
            self.compile(stmt)
        
        # Jump to end (skip else)
        end_label_pos = self.emit(JUMP, None)  # Will patch later
        
        # Patch else jump
        else_label = len(self.code)
        self.patch_jump(else_label_pos, else_label)
        
        # Compile else body (if exists)
        if node.else_body:
            for stmt in node.else_body:
                self.compile(stmt)
        
        # Patch end jump
        end_label = len(self.code)
        self.patch_jump(end_label_pos, end_label)
    
    def compile_while(self, node):
        """Compile while: loop_start, condition, JUMP_IF_FALSE end, body, JUMP start"""
        loop_start = len(self.code)
        
        # Compile condition
        self.compile(node.cond)
        
        # Emit jump if false (to end)
        end_label_pos = self.emit(JUMP_IF_FALSE, None)  # Will patch later
        
        # Compile body
        for stmt in node.body:
            self.compile(stmt)
        
        # Jump back to start
        self.emit(JUMP, loop_start)
        
        # Patch end jump
        end_label = len(self.code)
        self.patch_jump(end_label_pos, end_label)
    
    def compile_binop(self, node):
        """Compile binary operation: compile left, compile right, emit op"""
        self.compile(node.left)
        self.compile(node.right)
        
        if node.op == "+":
            self.emit(ADD)
        elif node.op == "-":
            self.emit(SUB)
        elif node.op == "*":
            self.emit(MUL)
        elif node.op == "/":
            self.emit(DIV)
        elif node.op == "<":
            self.emit(CMP_LT)
        elif node.op == ">":
            self.emit(CMP_GT)
        elif node.op == "<=":
            self.emit(CMP_LE)
        elif node.op == ">=":
            self.emit(CMP_GE)
        elif node.op == "==":
            self.emit(CMP_EQ)
        elif node.op == "!=":
            self.emit(CMP_NEQ)
        else:
            raise ValueError(f"Unknown operator: {node.op}")
    
    def patch_jump(self, pos: int, target: int) -> None:
        """Patch a jump instruction at position pos to jump to target."""
        if pos < len(self.code):
            self.code[pos].arg = target
    
    def compile_number(self, node):
        """Compile number: LOAD_CONST"""
        const_idx = self.const_index(node.value)
        self.emit(LOAD_CONST, const_idx)
    
    def compile_var(self, node):
        """Compile variable: LOAD_NAME"""
        name_idx = self.name_index(node.name)
        self.emit(LOAD_NAME, name_idx)


def compile_ast(ast):
    """Convenience function to compile an AST."""
    compiler = Compiler()
    code, consts, names = compiler.compile(ast)
    return code, consts, names


if __name__ == "__main__":
    import sys
    import os
    from lexer import Lexer
    from parser import Parser
    from vm import VM
    from bytecode import format_bytecode
    from ast_viz import ast_to_dot
    from bytecode_serializer import serialize_bytecode
    
    if len(sys.argv) < 2:
        print("Usage: python compiler.py <file.mp> [--debug] [--dump-ast] [--compile-only]")
        sys.exit(1)
    
    filename = sys.argv[1]
    debug = "--debug" in sys.argv
    dump_ast = "--dump-ast" in sys.argv
    compile_only = "--compile-only" in sys.argv
    
    try:
        # Read source file
        with open(filename, 'r') as f:
            source = f.read()
        
        # Lex
        lexer = Lexer(source)
        tokens = lexer.tokenize()
        if debug:
            print("=== TOKENS ===")
            for token in tokens:
                print(token)
            print()
        
        # Parse
        parser = Parser(tokens)
        ast = parser.parse_program()
        if debug:
            print("=== AST ===")
            print(ast)
            print()
        
        # Semantic analysis
        semantic = SemanticAnalyzer()
        errors = semantic.check(ast)
        if errors:
            print("=== SEMANTIC ERRORS ===")
            for error in errors:
                print(error)
            print()
            if not debug:
                sys.exit(1)
        
        # Optimize
        optimizer = Optimizer()
        ast = optimizer.optimize(ast)
        if debug:
            print("=== OPTIMIZED AST ===")
            print(ast)
            print()
        
        # Dump AST if requested
        if dump_ast:
            dot_file = filename.replace('.mp', '.dot').replace('.mpy', '.dot')
            ast_to_dot(ast, dot_file)
            print(f"AST dumped to {dot_file}")
            print(f"Generate visualization with: dot -Tpng {dot_file} -o {dot_file.replace('.dot', '.png')}")
        
        # Compile
        code, consts, names = compile_ast(ast)
        if debug:
            print("=== BYTECODE ===")
            print(format_bytecode(code))
            print(f"\nConstants: {consts}")
            print(f"Names: {names}")
            print()
        
        # Serialize bytecode for C++ VM
        bytecode_file = filename.replace('.mp', '.mpbc').replace('.mpy', '.mpbc')
        serialize_bytecode(code, consts, names, bytecode_file)
        if debug:
            print(f"Bytecode serialized to {bytecode_file}")
        
        # Execute (unless compile-only)
        if not compile_only:
            vm = VM(code, consts, names)
            vm.run()
        
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

