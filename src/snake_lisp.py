#!/usr/bin/env python3
"""
Snake-Lisp REPL 🐍
Интерактивная среда для нашего Lisp интерпретатора
"""

import sys
from lexer import Lexer
from parser import Parser
from eval import evaluate, Environment, setup_global_env

def repl():
    """Read-Eval-Print Loop"""
    env = Environment()
    setup_global_env(env)
    
    print("🐍 Snake-Lisp REPL")
    print("Введите Lisp код (Ctrl+C для выхода)")
    print("=" * 40)
    
    while True:
        try:
            # Читаем ввод
            code = input("snake-lisp> ")
            if not code.strip():
                continue
            
            # Лексический анализ
            lexer = Lexer(code)
            tokens = lexer.tokenize()
            
            # Синтаксический анализ
            parser = Parser(tokens)
            
            # Выполняем все выражения
            while True:
                ast = parser.parse()
                if ast is None:
                    break
                
                result = evaluate(ast, env)
                if result is not None:
                    print(f"⇒ {result}")
                    
        except KeyboardInterrupt:
            print("\n🐍 До свидания!")
            break
        except EOFError:
            print("\n🐍 До свидания!")
            break
        except Exception as e:
            print(f"Ошибка: {e}")

if __name__ == "__main__":
    repl()
