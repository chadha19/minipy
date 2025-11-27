"""Lexer (tokenizer) for MiniPy."""

from errors import LexerError


class Token:
    """Represents a token."""
    def __init__(self, type, value, line=1, col=1):
        self.type = type
        self.value = value
        self.line = line
        self.col = col
    
    def __repr__(self):
        return f"Token({self.type}, {repr(self.value)}, line={self.line}, col={self.col})"
    
    def __eq__(self, other):
        if not isinstance(other, Token):
            return False
        return self.type == other.type and self.value == other.value


# Token types
IDENT = "IDENT"
NUMBER = "NUMBER"
KEYWORD = "KEYWORD"
PLUS = "PLUS"
MINUS = "MINUS"
MUL = "MUL"
DIV = "DIV"
LT = "LT"
GT = "GT"
LE = "LE"
GE = "GE"
EQEQ = "EQEQ"
NEQ = "NEQ"
ASSIGN = "ASSIGN"
LPAREN = "LPAREN"
RPAREN = "RPAREN"
COLON = "COLON"
NEWLINE = "NEWLINE"
INDENT = "INDENT"
DEDENT = "DEDENT"
EOF = "EOF"

# Keywords
KEYWORDS = {
    "if": "if",
    "else": "else",
    "while": "while",
    "print": "print",
}


class Lexer:
    """Tokenizes MiniPy source code."""
    
    def __init__(self, source):
        self.source = source
        self.pos = 0
        self.line = 1
        self.col = 1
        self.indent_stack = [0]  # Track indentation levels
        self.tokens = []
        self.pending_indents = []  # Track pending indents/dedents
    
    def current_char(self):
        """Get current character or None if EOF."""
        if self.pos >= len(self.source):
            return None
        return self.source[self.pos]
    
    def peek_char(self, offset=1):
        """Peek ahead by offset characters."""
        pos = self.pos + offset
        if pos >= len(self.source):
            return None
        return self.source[pos]
    
    def advance(self):
        """Move to next character."""
        if self.pos < len(self.source):
            if self.source[self.pos] == '\n':
                self.line += 1
                self.col = 1
            else:
                self.col += 1
            self.pos += 1
    
    def skip_whitespace(self):
        """Skip whitespace (but not newlines)."""
        while self.current_char() and self.current_char() in ' \t\r':
            self.advance()
    
    def skip_comment(self):
        """Skip comment until newline."""
        while self.current_char() and self.current_char() != '\n':
            self.advance()
    
    def read_number(self):
        """Read a number token."""
        start_col = self.col
        num_str = ""
        while self.current_char() and self.current_char().isdigit():
            num_str += self.current_char()
            self.advance()
        return Token(NUMBER, int(num_str), self.line, start_col)
    
    def read_identifier(self):
        """Read an identifier or keyword."""
        start_col = self.col
        ident = ""
        while self.current_char() and (self.current_char().isalnum() or self.current_char() == '_'):
            ident += self.current_char()
            self.advance()
        
        # Check if it's a keyword
        if ident in KEYWORDS:
            return Token(KEYWORD, ident, self.line, start_col)
        return Token(IDENT, ident, self.line, start_col)
    
    def handle_indentation(self, indent_level):
        """Handle indentation for a new line."""
        if indent_level > self.indent_stack[-1]:
            # Indent
            self.indent_stack.append(indent_level)
            self.pending_indents.append((INDENT, indent_level))
        elif indent_level < self.indent_stack[-1]:
            # Dedent
            while len(self.indent_stack) > 1 and indent_level < self.indent_stack[-1]:
                self.indent_stack.pop()
                self.pending_indents.append((DEDENT, self.indent_stack[-1]))
            if indent_level != self.indent_stack[-1]:
                raise LexerError(
                    f"Inconsistent indentation: expected {self.indent_stack[-1]}, got {indent_level}",
                    self.line, self.col
                )
    
    def tokenize(self):
        """Tokenize the entire source."""
        self.tokens = []
        self.pos = 0
        self.line = 1
        self.col = 1
        self.indent_stack = [0]
        self.pending_indents = []
        
        in_newline = True
        line_start_col = 1
        
        while self.pos < len(self.source):
            # Skip whitespace (but track for indentation)
            if in_newline:
                spaces = 0
                while self.current_char() and self.current_char() in ' \t':
                    if self.current_char() == ' ':
                        spaces += 1
                    elif self.current_char() == '\t':
                        spaces += 4  # Treat tab as 4 spaces
                    self.advance()
                
                # Handle indentation if not empty line
                if self.current_char() and self.current_char() != '\n':
                    if self.current_char() != '#':  # Not a comment
                        self.handle_indentation(spaces)
                        # Emit pending indents/dedents immediately
                        for token_type, level in self.pending_indents:
                            self.tokens.append(Token(token_type, level, self.line, 1))
                        self.pending_indents = []
                    in_newline = False
                else:
                    # Empty line or comment, skip
                    if self.current_char() == '\n':
                        self.advance()
                    continue
            
            # Skip remaining whitespace
            self.skip_whitespace()
            
            if not self.current_char():
                break
            
            char = self.current_char()
            
            # Newline
            if char == '\n':
                self.tokens.append(Token(NEWLINE, '\n', self.line, self.col))
                self.advance()
                in_newline = True
                continue
            
            # Comment
            if char == '#':
                self.skip_comment()
                continue
            
            # Two-character operators
            if char == '=':
                self.advance()
                if self.current_char() == '=':
                    self.advance()
                    self.tokens.append(Token(EQEQ, '==', self.line, self.col - 1))
                else:
                    self.tokens.append(Token(ASSIGN, '=', self.line, self.col - 1))
                continue
            
            # Single-character operators
            if char == '+':
                self.tokens.append(Token(PLUS, '+', self.line, self.col))
                self.advance()
                continue
            if char == '-':
                self.tokens.append(Token(MINUS, '-', self.line, self.col))
                self.advance()
                continue
            if char == '*':
                self.tokens.append(Token(MUL, '*', self.line, self.col))
                self.advance()
                continue
            if char == '/':
                self.tokens.append(Token(DIV, '/', self.line, self.col))
                self.advance()
                continue
            if char == '<':
                self.advance()
                if self.current_char() == '=':
                    self.advance()
                    self.tokens.append(Token(LE, '<=', self.line, self.col - 1))
                else:
                    self.tokens.append(Token(LT, '<', self.line, self.col - 1))
                continue
            if char == '>':
                self.advance()
                if self.current_char() == '=':
                    self.advance()
                    self.tokens.append(Token(GE, '>=', self.line, self.col - 1))
                else:
                    self.tokens.append(Token(GT, '>', self.line, self.col - 1))
                continue
            if char == '!':
                self.advance()
                if self.current_char() == '=':
                    self.advance()
                    self.tokens.append(Token(NEQ, '!=', self.line, self.col - 1))
                else:
                    raise LexerError(f"Unexpected character after '!': {repr(self.current_char())}", self.line, self.col)
                continue
            if char == '(':
                self.tokens.append(Token(LPAREN, '(', self.line, self.col))
                self.advance()
                continue
            if char == ')':
                self.tokens.append(Token(RPAREN, ')', self.line, self.col))
                self.advance()
                continue
            if char == ':':
                self.tokens.append(Token(COLON, ':', self.line, self.col))
                self.advance()
                continue
            
            # Numbers
            if char.isdigit():
                self.tokens.append(self.read_number())
                continue
            
            # Identifiers and keywords
            if char.isalpha() or char == '_':
                self.tokens.append(self.read_identifier())
                continue
            
            # Unknown character
            raise LexerError(f"Unexpected character: {repr(char)}", self.line, self.col)
        
        # Add any pending dedents at end of file
        while len(self.indent_stack) > 1:
            self.indent_stack.pop()
            self.tokens.append(Token(DEDENT, self.indent_stack[-1], self.line, self.col))
        
        # Add EOF token
        self.tokens.append(Token(EOF, None, self.line, self.col))
        
        return self.tokens

