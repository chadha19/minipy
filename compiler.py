"""Compiler: converts AST to bytecode."""

from ast_nodes import Program, Assign, Print, If, While, BinOp, Number, Var
from bytecode import Instruction, LOAD_CONST, LOAD_NAME, STORE_NAME, ADD, SUB, MUL, DIV
from bytecode import CMP_LT, CMP_GT, CMP_EQ, JUMP, JUMP_IF_FALSE, PRINT, HALT


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
        self.code[else_label_pos].arg = else_label
        
        # Compile else body (if exists)
        if node.else_body:
            for stmt in node.else_body:
                self.compile(stmt)
        
        # Patch end jump
        end_label = len(self.code)
        self.code[end_label_pos].arg = end_label
    
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
        self.code[end_label_pos].arg = end_label
    
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
        elif node.op == "==":
            self.emit(CMP_EQ)
        else:
            raise ValueError(f"Unknown operator: {node.op}")
    
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
    from lexer import Lexer
    from parser import Parser
    from vm import VM
    from bytecode import format_bytecode
    
    if len(sys.argv) < 2:
        print("Usage: python compiler.py <file.mp> [--debug]")
        sys.exit(1)
    
    filename = sys.argv[1]
    debug = "--debug" in sys.argv
    
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
        
        # Compile
        code, consts, names = compile_ast(ast)
        if debug:
            print("=== BYTECODE ===")
            print(format_bytecode(code))
            print(f"\nConstants: {consts}")
            print(f"Names: {names}")
            print()
        
        # Execute
        vm = VM(code, consts, names)
        vm.run()
        
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

