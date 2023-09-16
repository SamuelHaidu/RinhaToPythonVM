from dataclasses import dataclass
from typing import Dict, Literal, Optional
from rinhac.ast import (
    Var,
    Function,
    Call,
    Let,
    Binary,
    File,
)
from rinhac.ast.json_parser import parse_json_to_object


@dataclass(slots=True)
class Symbol:
    name: str
    symbol_type: Literal["Var", "Function"]
    load_type: Literal["GLOBAL", "NAME", "FAST", "DEREF"]
    context_name: str
    referenced_count: int = 0


class SymbolTable:
    module_context_name = "<rinha:module>"
    def __init__(self, context_name: str = None, parent: "SymbolTable" = None):
        self.context_name = context_name or self.module_context_name
        self._context_symbols: Dict[str, Symbol] = {}
        self.parent: SymbolTable = parent
        self._tables: Dict[str, SymbolTable] = {}

    def get_context(self, context_name: str) -> Optional["SymbolTable"]:
        return self._tables.get(context_name)

    def lookup(self, symbol_name: str) -> Symbol | None:
        symbol = self._context_symbols.get(symbol_name)
        if symbol:
            return symbol

        if symbol_name == self.context_name:  # Special case, load recursive function
            return Symbol(symbol_name, "Function", "GLOBAL", self.context_name)

        if self.parent:
            return self.parent.lookup(symbol_name)

        return None

    def declare(
        self,
        symbol_name: str,
        symbol_type: Literal["Var", "Function"],
        load_type: Literal["GLOBAL", "NAME", "FAST", "DREF"] = "FAST",
    ):
        if symbol_name in self._context_symbols:
            raise Exception(f"Symbol {symbol_name} already declared!")

        symbol = Symbol(symbol_name, symbol_type, load_type, self.context_name)
        if self.context_name == "<rinha:module>":
            symbol.load_type = "NAME"

        self._context_symbols[symbol_name] = symbol
        if symbol_type == "Function":
            self._tables[symbol_name] = SymbolTable(symbol_name, self)

    def reference(self, symbol_name: str):
        symbol = self.lookup(symbol_name)
        if symbol:
            symbol.referenced_count += 1
            if symbol.context_name != self.context_name:
                symbol.load_type = "DEREF"


def print_symbol_table(table: SymbolTable, depth: int = 0):
    prefix = "│   " * (depth - 1) + "├─ " if depth > 0 else ""
    for symbol in table._context_symbols.values():
        print(f"{prefix} {symbol.symbol_type} {symbol.name} {symbol.load_type}")
        if symbol.symbol_type == "Function":
            print_symbol_table(table.get_context(symbol.name), depth + 1)


def create_symbol_table(term, table: SymbolTable = None):
    if isinstance(term, File):
        table = SymbolTable()
        create_symbol_table(term.expression, table)

    elif isinstance(term, Let) and not isinstance(term.value, Function):
        table.declare(term.name.text, "Var")
        create_symbol_table(term.next_term, table)

    elif isinstance(term, Let) and isinstance(term.value, Function):
        table.declare(term.name.text, "Function")
        function_context = table.get_context(term.name.text)
        for param in term.value.parameters:
            function_context.declare(param.text, "Var", "FAST")
        create_symbol_table(term.value.value, function_context)
        create_symbol_table(term.next_term, table)

    elif isinstance(term, Var):
        table.reference(term.text)

    elif isinstance(term, Call):
        create_symbol_table(term.callee, table)
        for arg in term.arguments:
            create_symbol_table(arg, table)

    elif isinstance(term, Binary):
        create_symbol_table(term.lhs, table)
        create_symbol_table(term.rhs, table)

    return table


if __name__ == "__main__":
    import json
    with open(".drafts/rinha/sum/sum.json") as f:
        json_ast = json.load(f)
        ast = parse_json_to_object(json_ast)
    symbol_table = create_symbol_table(ast)
    print_symbol_table(symbol_table)