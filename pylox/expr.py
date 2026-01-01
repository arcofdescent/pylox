"""
expression     → literal
               | unary
               | binary
               | grouping ;

literal        → NUMBER | STRING | "true" | "false" | "nil" ;
grouping       → "(" expression ")" ;
unary          → ( "-" | "!" ) expression ;
binary         → expression operator expression ;
operator       → "==" | "!=" | "<" | "<=" | ">" | ">="
               | "+"  | "-"  | "*" | "/" ;
"""

from abc import ABC, abstractmethod
from pylox.token import Token

class Expr(ABC):
    def __init__(self):
        pass

class Binary(Expr):
    def __init__(self, left: Expr, operator: Token, right: Expr):
        super().__init__()
        self.left = left
        self.operator = operator
        self.right = right
