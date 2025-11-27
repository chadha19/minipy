#!/usr/bin/env python3
"""MiniPy compiler CLI - compiles .mpy files to bytecode."""

import sys
from compiler import (
    Lexer, Parser, SemanticAnalyzer, Optimizer,
    compile_ast, serialize_bytecode
)

def main():
    if len(sys.argv) < 2:
        print("Usage: minipyc <file.mpy>")
        sys.exit(1)
    
    filename = sys.argv[1]
    
    try:
        with open(filename, 'r') as f:
            source = f.read()
        
        # Full pipeline
        lexer = Lexer(source)
        tokens = lexer.tokenize()
        
        parser = Parser(tokens)
        ast = parser.parse_program()
        
        semantic = SemanticAnalyzer()
        errors = semantic.check(ast)
        if errors:
            for error in errors:
                print(f"Error: {error}", file=sys.stderr)
            sys.exit(1)
        
        optimizer = Optimizer()
        ast = optimizer.optimize(ast)
        
        code, consts, names = compile_ast(ast)
        
        # Output bytecode
        bytecode_file = filename.replace('.mpy', '.mpbc')
        serialize_bytecode(code, consts, names, bytecode_file)
        print(f"Compiled to {bytecode_file}")
        
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()

