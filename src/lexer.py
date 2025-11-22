#!/usr/bin/env python3
"""
Snake-Lisp Lexer 🐍
Токенизатор - превращает код в поток токенов
"""

import re

class Token:
    """Токен Lisp кода"""
    def __init__(self, type, value, line, column):
        self.type = type
        self.value = value
        self.line = line
        self.column = column
    
    def __repr__(self):
        return f"Token({self.type}, {repr(self.value)}, {self.line}:{self.column})"

class Lexer:
    """Лексический анализатор Snake-Lisp"""
    
    # Регулярки для токенов
    TOKEN_SPEC = [
        ('COMMENT', r';[^\n]*'),           # Комментарии
        ('LPAREN', r'\('),                 # Открывающая скобка
        ('RPAREN', r'\)'),                 # Закрывающая скобка  
        ('NUMBER', r'-?\d+\.?\d*'),        # Числа
        ('STRING', r'"[^"]*"'),            # Строки
        ('SYMBOL', r'[^\s()";]+'),         # Символы
        ('WHITESPACE', r'\s+'),            # Пробелы (пропускаем)
    ]
    
    def __init__(self, code):
        self.code = code
        self.tokens = []
        self.line = 1
        self.column = 1
        self.pos = 0
        self.compile_regex()
    
    def compile_regex(self):
        """Компилируем регулярки в один паттерн"""
        patterns = []
        for name, pattern in self.TOKEN_SPEC:
            patterns.append(f'(?P<{name}>{pattern})')
        self.pattern = re.compile('|'.join(patterns))
    
    def tokenize(self):
        """Основной метод токенизации"""
        while self.pos < len(self.code):
            match = self.pattern.match(self.code, self.pos)
            if not match:
                raise SyntaxError(f"Неизвестный символ: {self.code[self.pos]} at {self.line}:{self.column}")
            
            kind = match.lastgroup
            value = match.group()
            
            if kind == 'WHITESPACE':
                # Пропускаем пробелы, но обновляем позицию
                lines = value.count('\n')
                if lines > 0:
                    self.line += lines
                    self.column = len(value) - value.rfind('\n')
                else:
                    self.column += len(value)
            elif kind == 'COMMENT':
                # Пропускаем комментарии
                pass  
            else:
                # Создаём токен
                token = Token(kind, value, self.line, self.column)
                self.tokens.append(token)
                
                # Обновляем позицию
                self.column += len(value)
            
            self.pos = match.end()
        
        return self.tokens

# Тестируем наш лексер
if __name__ == "__main__":
    code = """
    ; Это комментарий
    (+ 1 2 3)
    (define pi 3.14159)
    "hello world"
    """
    
    lexer = Lexer(code)
    tokens = lexer.tokenize()
    
    for token in tokens:
        print(token)
