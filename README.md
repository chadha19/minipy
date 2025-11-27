# MiniPy: A Production-Quality Python-like Language Compiler and Virtual Machine

MiniPy is a complete, production-ready compiler and virtual machine implementation for a Python-like programming language. It demonstrates advanced compiler techniques including semantic analysis, type checking, constant folding optimization, and dual-language VM implementation (Python + C++).

## Overview

MiniPy implements a full compiler stack with multiple execution backends:

```
Source Code → Lexer → Parser → AST → Semantic Analysis → Optimizer → Bytecode → VM (Python/C++) → Output
```

### Key Features

- **Complete Compiler Pipeline**: Lexical analysis, parsing, semantic analysis, optimization, and code generation
- **Type System**: Static type checking with `int` and `bool` types
- **Semantic Analysis**: Variable scoping, undefined variable detection, type checking
- **Constant Folding**: Compile-time optimization of constant expressions
- **Dual VM Backends**: Python VM (reference) and C++ VM (production)
- **AST Visualization**: Graphviz-based AST visualization
- **Comprehensive Testing**: 40+ unit and integration tests
- **CI/CD Pipeline**: Automated testing across Python 3.10-3.12

## 📁 Project Structure

```
minipy/
├── README.md              # This file
├── compiler.py            # Main compiler + CLI
├── lexer.py               # Hand-written lexer
├── parser.py              # Recursive descent parser
├── ast_nodes.py           # AST node definitions (dataclasses)
├── semantic.py            # Semantic analysis & type checking
├── optimizer.py           # Constant folding optimizer
├── bytecode.py            # Bytecode instruction definitions
├── vm.py                  # Python VM implementation
├── ast_viz.py             # AST visualization (Graphviz)
├── bytecode_serializer.py # Bytecode serialization
├── minipyc.py             # Compiler CLI
├── cpp_vm/                # C++ VM implementation
│   ├── vm.h/cpp           # VM core
│   ├── bytecode_loader.h/cpp
│   ├── main.cpp
│   └── CMakeLists.txt
├── examples/              # Example programs
│   ├── hello.mp
│   ├── loop.mp
│   └── ifelse.mp
└── tests/                  # Test suite
    ├── test_lexer.py
    ├── test_parser.py
    ├── test_vm.py
    ├── test_semantic.py
    ├── test_optimizer.py
    ├── test_bytecode.py
    └── test_integration.py
```

## Quick Start

### Running a Program

```bash
# Run with Python VM
python compiler.py examples/hello.mp

# Debug mode (shows tokens, AST, bytecode)
python compiler.py examples/loop.mp --debug

# Dump AST visualization
python compiler.py examples/loop.mp --dump-ast
dot -Tpng examples/loop.dot -o examples/loop.png

# Compile to bytecode only
python compiler.py examples/loop.mp --compile-only
```

### Compiling to Bytecode

```bash
# Compile MiniPy source to bytecode
python minipyc.py examples/loop.mp
# Generates: examples/loop.mpbc
```

### Running C++ VM

```bash
# Build C++ VM
cd cpp_vm
mkdir build && cd build
cmake ..
make

# Run bytecode
./minipy_vm ../examples/loop.mpbc
```

### Running Tests

```bash
# Run all tests
python -m pytest tests/ -v

# Run specific test suite
python -m pytest tests/test_semantic.py -v
```

## 🏗️ Architecture

### Compiler Pipeline

1. **Lexical Analysis** (`lexer.py`)
   - Tokenizes source code
   - Handles indentation (Python-style)
   - Supports operators: `+`, `-`, `*`, `/`, `<`, `>`, `<=`, `>=`, `==`, `!=`

2. **Syntax Analysis** (`parser.py`)
   - Recursive descent parser
   - Builds Abstract Syntax Tree (AST)
   - Handles operator precedence

3. **Semantic Analysis** (`semantic.py`)
   - Type checking (int, bool)
   - Variable scoping with block-level scopes
   - Undefined variable detection
   - Type mismatch detection

4. **Optimization** (`optimizer.py`)
   - Constant folding: `3 + 5` → `8`
   - Identity optimizations: `x + 0` → `x`, `x * 1` → `x`
   - Dead code elimination in constant conditionals

5. **Code Generation** (`compiler.py`)
   - AST → Bytecode compilation
   - Jump patching for control flow
   - Constant and name table management

6. **Execution** (`vm.py` or `cpp_vm/`)
   - Stack-based virtual machine
   - Instruction dispatch
   - Stack safety checks

### Bytecode Instruction Set

| Opcode | Description | Stack Effect |
|--------|-------------|--------------|
| `LOAD_CONST idx` | Load constant | `[] → [value]` |
| `LOAD_NAME idx` | Load variable | `[] → [value]` |
| `STORE_NAME idx` | Store variable | `[value] → []` |
| `ADD` | Addition | `[a, b] → [a+b]` |
| `SUB` | Subtraction | `[a, b] → [a-b]` |
| `MUL` | Multiplication | `[a, b] → [a*b]` |
| `DIV` | Division | `[a, b] → [a/b]` |
| `CMP_LT` | Less than | `[a, b] → [a<b]` |
| `CMP_GT` | Greater than | `[a, b] → [a>b]` |
| `CMP_LE` | Less or equal | `[a, b] → [a<=b]` |
| `CMP_GE` | Greater or equal | `[a, b] → [a>=b]` |
| `CMP_EQ` | Equality | `[a, b] → [a==b]` |
| `CMP_NEQ` | Not equal | `[a, b] → [a!=b]` |
| `JUMP target` | Unconditional jump | `[] → []` |
| `JUMP_IF_FALSE target` | Jump if false | `[value] → []` |
| `JUMP_IF_TRUE target` | Jump if true | `[value] → []` |
| `POP` | Pop stack | `[value] → []` |
| `PRINT` | Print value | `[value] → []` |
| `HALT` | End execution | `[] → []` |

### Type System

MiniPy supports two types:

- **`int`**: Integer literals and arithmetic operations
- **`bool`**: Result of comparisons (`<`, `>`, `==`, etc.), used in conditions

Type checking rules:
- Arithmetic operations (`+`, `-`, `*`, `/`) require `int` operands
- Comparisons (`<`, `>`, `<=`, `>=`) require `int` operands, return `bool`
- Equality (`==`, `!=`) requires compatible types, return `bool`
- `if` and `while` conditions must be `bool`

### Variable Scoping

- Block-scoped variables (each `if`/`while` creates a new scope)
- Variable shadowing allowed
- Variables must be declared before use
- Global scope for top-level variables

## Language Syntax

### Grammar

```
program     : statement*
statement   : assignment | print | if | while
assignment  : IDENT "=" expression
print       : "print" "(" expression ")"
if          : "if" expression ":" block ("else" ":" block)?
while       : "while" expression ":" block
block       : INDENT statement+ DEDENT
expression  : comparison
comparison  : additive (("<" | ">" | "<=" | ">=" | "==" | "!=") additive)?
additive    : multiplicative (("+" | "-") multiplicative)*
multiplicative : factor (("*" | "/") factor)*
factor      : NUMBER | IDENT | "(" expression ")"
```

### Example Programs

**Hello World** (`examples/hello.mp`):
```python
print(5)
```

**Loop** (`examples/loop.mp`):
```python
x = 0
while x < 3:
    x = x + 1
print(x)
```

**Conditional** (`examples/ifelse.mp`):
```python
x = 10
if x > 5:
    print(1)
else:
    print(0)
```

## 🔧 Development

### Building C++ VM

```bash
cd cpp_vm
mkdir build
cd build
cmake ..
make
```

### Adding New Features

1. **New AST Node**: Add to `ast_nodes.py` as dataclass
2. **Parser Support**: Add parsing rule in `parser.py`
3. **Semantic Check**: Add type checking in `semantic.py`
4. **Optimization**: Add optimization rule in `optimizer.py`
5. **Code Generation**: Add compilation in `compiler.py`
6. **VM Support**: Add instruction handling in `vm.py` and `cpp_vm/`

### Code Style

- Python: Type hints required, dataclasses for AST nodes
- C++: C++17, RAII, no raw pointers
- Tests: pytest for Python, comprehensive coverage

## Testing

The test suite includes:

- **Lexer Tests**: Tokenization, indentation, operators
- **Parser Tests**: AST construction, operator precedence
- **Semantic Tests**: Type checking, scoping, error detection
- **Optimizer Tests**: Constant folding, dead code elimination
- **Bytecode Tests**: Instruction generation
- **VM Tests**: Instruction execution, stack operations
- **Integration Tests**: End-to-end pipeline

Run tests:
```bash
python -m pytest tests/ -v
```

## CI/CD

GitHub Actions workflow tests:
- Python 3.10, 3.11, 3.12 on Ubuntu, Windows, macOS
- Linting with `ruff`
- Type checking with `mypy`
- C++ VM build (Linux)

## AST Visualization

Generate AST visualization:

```bash
python compiler.py examples/loop.mp --dump-ast
dot -Tpng examples/loop.dot -o examples/loop.png
```

## Educational Value

This project demonstrates:

- **Compiler Design**: Complete compiler pipeline from scratch
- **Type Systems**: Static type checking implementation
- **Optimization**: Constant folding and dead code elimination
- **Virtual Machines**: Stack-based VM design
- **Multi-language Systems**: Python compiler + C++ runtime
- **Software Engineering**: Testing, CI/CD, documentation

## License

Educational project - use freely for learning.

