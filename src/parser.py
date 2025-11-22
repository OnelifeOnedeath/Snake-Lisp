#!/usr/bin/env python3
"""
Snake-Lisp Parser 🐍
Парсер - превращает токены в AST (Abstract Syntax Tree)
"""

class ASTNode:
    """Базовый класс для узлов AST"""
    def __repr__(self):
        return f"{self.__class__.__name__}({self.__dict__})"

class NumberNode(ASTNode):
    def __init__(self, value):
        self.value = float(value) if '.' in str(value) else int(value)

class SymbolNode(ASTNode):
    def __init__(self, name):
        self.name = name

class StringNode(ASTNode):
    def __init__(self, value):
        self.value = value[1:-1]  # Убираем кавычки

class ListNode(ASTNode):
    def __init__(self, elements):
        self.elements = elements
    
    def __repr__(self):
        return f"List({self.elements})"

class Parser:
    """Парсер Snake-Lisp - превращает токены в AST"""
    
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
    
    def current_token(self):
        """Текущий токен"""
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return None
    
    def eat(self, token_type=None):
        """Съедаем текущий токен и двигаемся дальше"""
        token = self.current_token()
        if not token:
            raise SyntaxError("Неожиданный конец файла")
        
        if token_type and token.type != token_type:
            raise SyntaxError(f"Ожидался {token_type}, но получен {token.type} at {token.line}:{token.column}")
        
        self.pos += 1
        return token
    
    def parse(self):
        """Основной метод парсинга"""
        return self.parse_expression()
    
    def parse_expression(self):
        """Парсим выражение"""
        token = self.current_token()
        
        if not token:
            return None
        
        if token.type == 'LPAREN':
            return self.parse_list()
        elif token.type == 'NUMBER':
            return NumberNode(self.eat('NUMBER').value)
        elif token.type == 'STRING':
            return StringNode(self.eat('STRING').value)
        elif token.type == 'SYMBOL':
            return SymbolNode(self.eat('SYMBOL').value)
        else:
            raise SyntaxError(f"Неожиданный токен: {token.type} at {token.line}:{token.column}")
    
    def parse_list(self):
        """Парсим список (S-Expression)"""
        self.eat('LPAREN')  # Съедаем открывающую скобку
        
        elements = []
        while self.current_token() and self.current_token().type != 'RPAREN':
            elements.append(self.parse_expression())
        
        self.eat('RPAREN')  # Съедаем закрывающую скобку
        return ListNode(elements)

# Тестируем парсер
if __name__ == "__main__":
    from lexer import Lexer
    
    code = """
    (+ 1 2 3)
    (define pi 3.14159)
    "hello world"
    """
    
    # Лексический анализ
    lexer = Lexer(code)
    tokens = lexer.tokenize()
    
    print("=== ТОКЕНЫ ===")
    for token in tokens:
        print(token)
    
    # Синтаксический анализ
    parser = Parser(tokens)
    ast = parser.parse()
    
    print("\n=== AST ===")
    print(ast)
