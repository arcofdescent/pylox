
import sys
from typing import List
from pylox.token import Token
from pylox.scanner import Scanner

class Lox():
    def __init__(self):
        self.had_error = False
    
    def run_prompt(self):
        print("Running Lox REPL...")
        while True:
            try:
                line = input("lox> ")
                if line.strip().lower() in ("exit", "quit"):
                    print("Exiting Lox REPL.")
                    break
                self.run(line)
                self.had_error = False
            except EOFError:
                print("\nExiting Lox REPL.")
                break

    def run_file(self, path: str):
        print(f"Running Lox file: {path}")
        try:
            with open(path, 'r') as file:
                source = file.read()
                self.run(source)

                if self.had_error:
                    sys.exit(65)
        except FileNotFoundError:
            print(f"File not found: {path}")

    def run(self, source: str):
        print(f"Executing Lox source:\n{source}")

        scanner = Scanner(source, report_error=lambda line, where, message: self.report(line, where, message))
        tokens: List[Token] = scanner.scan_tokens()
        for token in tokens:
            print(token)

    def error(self, line: int, message: str):
        self.report(line, "", message)

    def report(self, line: int, where: str, message: str):
        print(f"[line {line}] Error{where}: {message}")
        self.had_error = True
        
