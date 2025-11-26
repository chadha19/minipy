"""Error handling for MiniPy compiler."""


class MiniPyError(Exception):
    """Base exception for MiniPy errors."""
    pass


class LexerError(MiniPyError):
    """Error during tokenization."""
    def __init__(self, message, line, col):
        super().__init__(f"LexerError at line {line}, col {col}: {message}")
        self.line = line
        self.col = col


class ParserError(MiniPyError):
    """Error during parsing."""
    def __init__(self, message, line=None, col=None):
        if line is not None:
            super().__init__(f"ParserError at line {line}, col {col}: {message}")
        else:
            super().__init__(f"ParserError: {message}")
        self.line = line
        self.col = col


class SemanticError(MiniPyError):
    """Error during semantic analysis."""
    def __init__(self, message, line=None):
        if line is not None:
            super().__init__(f"SemanticError at line {line}: {message}")
        else:
            super().__init__(f"SemanticError: {message}")
        self.line = line


class VMError(MiniPyError):
    """Error during VM execution."""
    def __init__(self, message, ip=None):
        if ip is not None:
            super().__init__(f"VMError at instruction {ip}: {message}")
        else:
            super().__init__(f"VMError: {message}")
        self.ip = ip

