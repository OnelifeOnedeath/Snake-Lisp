#!/usr/bin/env python3
"""
Snake-Lisp Evaluator 🐍
Интерпретатор - выполняет AST и возвращает результат
"""

class Environment:
    """Окружение - хранит переменные и функции"""
    def __init__(self, parent=None):
        self.parent = parent
        self.vars = {}
    
    def define(self, name, value):
        """Определяем переменную"""
        self.vars[name] = value
    
    def lookup(self, name):
        """Ищем переменную в текущем или родительском окружении"""
        if name in self.vars:
            return self.vars[name]
        elif self.parent:
            return self.parent.lookup(name)
        else:
            raise NameError(f"Переменная '{name}' не определена")

class LispFunction:
    """Пользовательская функция Lisp"""
    def __init__(self, params, body, env):
        self.params = params
        self.body = body
        self.env = env
    
    def __repr__(self):
        return f"<function {self.params}>"

def evaluate(ast, env=None):
    """Выполняет AST и возвращает результат"""
    if env is None:
        env = Environment()
        setup_global_env(env)
    
    # Число - возвращаем как есть
    if isinstance(ast, NumberNode):
        return ast.value
    
    # Строка - возвращаем как есть
    if isinstance(ast, StringNode):
        return ast.value
    
    # Символ - ищем в окружении
    if isinstance(ast, SymbolNode):
        return env.lookup(ast.name)
    
    # Список - выполняем как S-Expression
    if isinstance(ast, ListNode):
        return evaluate_list(ast.elements, env)
    
    raise TypeError(f"Неизвестный тип AST: {type(ast)}")

def evaluate_list(elements, env):
    """Выполняет список (S-Expression)"""
    if not elements:
        return None
    
    # Первый элемент - функция/оператор
    func = evaluate(elements[0], env)
    args = [evaluate(arg, env) for arg in elements[1:]]
    
    # Встроенные функции
    if callable(func):
        return func(*args)
    
    # Пользовательские функции
    if isinstance(func, LispFunction):
        # Создаём новое окружение для вызова функции
        func_env = Environment(func.env)
        for param, arg in zip(func.params, args):
            func_env.define(param, arg)
        return evaluate(func.body, func_env)
    
    raise TypeError(f"{func} не является функцией")

def setup_global_env(env):
    """Настраиваем глобальное окружение со встроенными функциями"""
    
    # Арифметические операции
    env.define('+', lambda *args: sum(args))
    env.define('-', lambda x, *rest: x - sum(rest) if rest else -x)
    env.define('*', lambda *args: __import__('functools').reduce(lambda x, y: x * y, args, 1))
    env.define('/', lambda x, y: x / y)
    
    # Сравнения
    env.define('=', lambda x, y: x == y)
    env.define('<', lambda x, y: x < y)
    env.define('>', lambda x, y: x > y)
    
    # Логические операции
    env.define('not', lambda x: not x)
    
    # Функции для списков
    env.define('list', lambda *args: list(args))
    env.define('car', lambda x: x[0] if x else None)
    env.define('cdr', lambda x: x[1:] if x else [])
    env.define('cons', lambda x, y: [x] + y)
    
    # Вывод
    env.define('display', lambda x: print(x, end=''))
    env.define('newline', lambda: print())

# Тестируем весь пайплайн!
if __name__ == "__main__":
    from lexer import Lexer
    from parser import Parser, NumberNode, SymbolNode, ListNode, StringNode
    
    code = """
    (+ 1 2 3)
    (* 2 (+ 3 4))
    (display "Hello, Snake-Lisp!")
    (newline)
    """
    
    print("=== SNAKE-LISP ИНТЕРПРЕТАТОР ===")
    
    # Весь пайплайн: Code → Tokens → AST → Result
    lexer = Lexer(code)
    tokens = lexer.tokenize()
    
    parser = Parser(tokens)
    
    # Выполняем все выражения по очереди
    while True:
        ast = parser.parse()
        if ast is None:
            break
        
        try:
            result = evaluate(ast)
            if result is not None:
                print(f"⇒ {result}")
        except Exception as e:
            print(f"Ошибка: {e}")
            break
