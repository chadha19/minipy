# MiniPy: A Python-like Language Compiler and Virtual Machine

MiniPy is a small Python-like programming language with a complete compiler pipeline: from source code to bytecode execution on a stack-based virtual machine.

## Overview

MiniPy implements a full compiler stack:

```
Source Code → Lexer → Parser → AST → Bytecode Generator → Virtual Machine → Output
```

### Language Features

- **Variables**: `x = 10`
- **Arithmetic**: `+`, `-`, `*`, `/`
- **Comparisons**: `<`, `>`, `==`
- **Print**: `print(expression)`
- **Control Flow**:
  - `if` / `else` statements
  - `while` loops
- **Data Types**: Integers and booleans (0/1)

## Project Structure

```
minipy/
├── README.md           # This file
├── compiler.py         # Main entry point + AST to bytecode compiler
├── lexer.py            # Tokenizer
├── parser.py           # Recursive descent parser
├── ast_nodes.py        # AST node definitions
├── bytecode.py         # Bytecode instruction definitions
├── vm.py               # Stack-based virtual machine
├── interpreter.py      # Optional tree-walk interpreter
├── errors.py           # Error handling
├── examples/           # Example MiniPy programs
│   ├── hello.mp
│   ├── loop.mp
│   └── ifelse.mp
└── tests/              # Test suite
    ├── test_lexer.py
    ├── test_parser.py
    ├── test_vm.py
    └── test_integration.py
```

## Installation

No installation required! Just ensure you have Python 3.6+ installed.

## Usage

### Running a Program

```bash
python compiler.py examples/hello.mp
```

### Debug Mode

To see tokens, AST, and bytecode:

```bash
python compiler.py examples/loop.mp --debug
```

### Running Tests

```bash
# Run all tests
python -m pytest tests/

# Or use unittest
python -m unittest discover tests
```

## Architecture

### 1. Lexer (`lexer.py`)

The lexer tokenizes source code into a stream of tokens:
- Identifiers, numbers, keywords
- Operators (`+`, `-`, `*`, `/`, `<`, `>`, `==`)
- Punctuation (`(`, `)`, `:`, `=`)
- Indentation tokens (`INDENT`, `DEDENT`)

**Example:**
```python
source = "x = 5 + 3"
# Tokens: [IDENT('x'), ASSIGN, NUMBER(5), PLUS, NUMBER(3), EOF]
```

### 2. Parser (`parser.py`)

Recursive descent parser that builds an Abstract Syntax Tree (AST):
- Handles operator precedence
- Validates syntax
- Performs basic semantic checks (undefined variables)

**AST Node Types:**
- `Program` - Root node
- `Assign` - Variable assignment
- `Print` - Print statement
- `If` - Conditional statement
- `While` - Loop statement
- `BinOp` - Binary operation
- `Number` - Integer literal
- `Var` - Variable reference

### 3. Compiler (`compiler.py`)

Converts AST to bytecode instructions:
- Generates instruction sequence
- Manages constant pool
- Manages name table
- Handles control flow with jumps

**Bytecode Opcodes:**
- `LOAD_CONST idx` - Load constant from pool
- `LOAD_NAME idx` - Load variable value
- `STORE_NAME idx` - Store value to variable
- `ADD`, `SUB`, `MUL`, `DIV` - Arithmetic operations
- `CMP_LT`, `CMP_GT`, `CMP_EQ` - Comparisons
- `JUMP target` - Unconditional jump
- `JUMP_IF_FALSE target` - Conditional jump
- `PRINT` - Print top of stack
- `HALT` - End execution

### 4. Virtual Machine (`vm.py`)

Stack-based VM that executes bytecode:
- **Stack**: Operand stack for calculations
- **Globals**: Variable storage
- **Constants**: Constant pool
- **Instruction Pointer**: Current execution position

**Execution Model:**
1. Fetch instruction at `ip`
2. Decode opcode and argument
3. Execute operation
4. Update `ip`
5. Repeat until `HALT`

## Example Programs

### Hello World (`examples/hello.mp`)

```python
print(5)
```

**Output:**
```
5
```

### Loop (`examples/loop.mp`)

```python
x = 0
while x < 3:
    x = x + 1
print(x)
```

**Output:**
```
3
```

### If/Else (`examples/ifelse.mp`)

```python
x = 10
if x > 5:
    print(1)
else:
    print(0)
```

**Output:**
```
1
```

## Language Syntax

### Statements

**Assignment:**
```python
x = 10
y = x + 5
```

**Print:**
```python
print(42)
print(x)
print(x + y)
```

**If/Else:**
```python
if x > 5:
    print(1)
else:
    print(0)
```

**While:**
```python
x = 0
while x < 10:
    x = x + 1
    print(x)
```

### Expressions

**Arithmetic:**
```python
2 + 3
10 - 4
5 * 6
20 / 4
```

**Comparisons:**
```python
x < 10
y > 5
z == 0
```

**Precedence:**
- Parentheses: `(2 + 3) * 4`
- Multiplication/Division before Addition/Subtraction
- Comparisons have lowest precedence

## Development

### Adding New Features

1. **Lexer**: Add new token types in `lexer.py`
2. **Parser**: Add parsing rules in `parser.py`
3. **AST**: Add new node types in `ast_nodes.py`
4. **Compiler**: Add compilation logic in `compiler.py`
5. **VM**: Add execution logic in `vm.py`

### Testing

The test suite includes:
- Unit tests for each component
- Integration tests for the full pipeline

Run tests with:
```bash
python -m unittest discover tests
```

## Implementation Details

### Indentation Handling

MiniPy uses Python-style indentation. The lexer:
1. Tracks indentation levels on newlines
2. Emits `INDENT` tokens when indentation increases
3. Emits `DEDENT` tokens when indentation decreases
4. Validates consistent indentation

### Variable Scoping

Currently, all variables are global. The parser tracks defined variables and raises errors for undefined variable usage.

### Boolean Representation

Booleans are represented as integers:
- `0` = False
- `1` (or any non-zero) = True

### Integer Division

Division uses integer division (`//`), so `7 / 2 = 3`.

## Limitations

- No floating-point numbers
- No strings
- No functions
- No arrays/lists
- Global variables only
- No type checking (all integers)

## Future Enhancements

Potential additions:
- Functions and function calls
- Local variable scoping
- String literals
- Lists/arrays
- More operators (`<=`, `>=`, `!=`)
- Error messages with line numbers
- Optimizations (constant folding, dead code elimination)

## License

This is an educational project. Feel free to use and modify as needed.

## Author

Created as a complete compiler and VM implementation example.

