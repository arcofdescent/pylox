
from typing import List, Optional, Callable
from pylox.token import Token
from pylox.token_type import TokenType

class Scanner():
    def __init__(self, source: str, report_error: Optional[Callable[[int, str, str], None]] = None):
        self.source : str = source
        self.tokens : List[Token] = []
        self.start : int = 0
        self.current : int = 0
        self.line : int = 1
        self.report_error = report_error

    def scan_tokens(self) -> List[Token]:
        print("Scanning tokens...")

        while not self.is_at_end():
            self.start = self.current
            self.scan_token()

        self.tokens.append(Token(TokenType.EOF, "", None, self.line))
        return self.tokens

    def is_at_end(self) -> bool:
        return self.current >= len(self.source)

    def scan_token(self):
        c = self.advance()
        # print(f"Scanning token: {c}")

        match c:
            case '(': self.add_token(TokenType.LEFT_PAREN)
            case ')': self.add_token(TokenType.RIGHT_PAREN)
            case '{': self.add_token(TokenType.LEFT_BRACE)
            case '}': self.add_token(TokenType.RIGHT_BRACE)
            case ',': self.add_token(TokenType.COMMA)
            case '.': self.add_token(TokenType.DOT)
            case '-': self.add_token(TokenType.MINUS)
            case '+': self.add_token(TokenType.PLUS)
            case ';': self.add_token(TokenType.SEMICOLON)
            case '*': self.add_token(TokenType.STAR)

            # single or double character tokens
            case '!':
                if self.match('='):
                    self.add_token(TokenType.BANG_EQUAL)
                else:
                    self.add_token(TokenType.BANG)
            case '=':
                if self.match('='):
                    self.add_token(TokenType.EQUAL_EQUAL)
                else:
                    self.add_token(TokenType.EQUAL)
            case '>':
                if self.match('='):
                    self.add_token(TokenType.GREATER_EQUAL)
                else:
                    self.add_token(TokenType.GREATER)
            case '<':
                if self.match('='):
                    self.add_token(TokenType.LESS_EQUAL)
                else:
                    self.add_token(TokenType.LESS)
                    
            # slash or comment
            case '/':
                if self.match('/'):
                    # A comment goes until the end of the line.
                    while self.peek() != '\n' and not self.is_at_end():
                        self.advance()
                else:
                    self.add_token(TokenType.SLASH)
                    
            # whitespace
            case ' ' | '\r' | '\t':
                pass

            # newline
            case '\n':
                self.line += 1

            # string
            case '"':
                while self.peek() != '"' and not self.is_at_end():
                    if self.peek() == '\n':
                        self.line += 1
                    self.advance()

                if self.is_at_end():
                    self.report_error(self.line, "", "Unterminated string.")
                    return

                # The closing ".
                self.advance()

                # Trim the surrounding quotes.
                value = self.source[self.start + 1:self.current - 1]
                self.add_token(TokenType.STRING, value)
            
            # numbers
            case _ if c.isdigit():
                while self.peek().isdigit():
                    self.advance()

                # Look for a fractional part.
                if self.peek() == '.' and self.peek_next().isdigit():
                    # Consume the "."
                    self.advance()

                    while self.peek().isdigit():
                        self.advance()

                value = float(self.source[self.start:self.current])
                self.add_token(TokenType.NUMBER, value)
                
            case _:
                self.report_error(self.line, "", f"Unexpected character: {c}")
            
    def advance(self) -> str:
        ret = self.source[self.current]
        self.current += 1
        return ret
    
    def add_token(self, token_type: TokenType, literal: object = None):
        text = self.source[self.start:self.current]
        self.tokens.append(Token(token_type, text, literal, self.line))

    def match(self, expected: str) -> bool:
        if self.is_at_end():
            return False
        if self.source[self.current] != expected:
            return False

        self.current += 1
        return True

    def peek(self) -> str:
        if self.is_at_end():
            return '\0'
        return self.source[self.current]
    
    def peek_next(self) -> str:
        if self.current + 1 >= len(self.source):
            return '\0'
        return self.source[self.current + 1]

