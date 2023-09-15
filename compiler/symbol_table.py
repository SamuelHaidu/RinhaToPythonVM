from typing import Dict, List
from compiler.ast import (
    Var,
    Function,
    Call,
    Let,
    Binary,
    File,
)

class SymbolTable:
    def __init__(self):
        self.table = {}

    def insert(self, scope, name, load_type=None):
        if scope == "module":
            load_type = "NAME"
        else:
            load_type = "FAST"
        if scope not in self.table:
            self.table[scope] = {}
        self.table[scope][name] = {"load_type": load_type}

    def lookup(self, name) -> List[str]:
        # returns a list of scopes where the name was found
        finds = []
        for scope in self.table:
            if name in self.table[scope]:
                finds.append(scope)
        return finds

    def insert_load(self, scope, name):
        finds = self.lookup(name)
        if len(finds) == 0:
            raise Exception(f"Symbol {name} not found!")

        finds = [f.split(".") for f in finds]
        load_scope_chain = scope.split(".")
        finds = [
            f
            for f in finds
            if f[: len(load_scope_chain)] == load_scope_chain[: len(f)]
            and len(f) <= len(load_scope_chain)
        ]

        longest_chain = max(finds, key=len)
        if len(longest_chain) == 1:
            return

        if len(longest_chain) < len(load_scope_chain):
            longest_chain = ".".join(longest_chain)
            self.table[longest_chain][name]["load_type"] = "DEREF"

    def get_closest(self, scope, name) -> Dict[str, str]:
        if scope != "module" and scope.endswith(name):
            return {"load_type": "GLOBAL"}
        finds = self.lookup(name)
        if len(finds) == 0:
            raise Exception(f"Symbol {name} not found!")

        finds = [f.split(".") for f in finds]
        load_scope_chain = scope.split(".")
        finds = [
            f
            for f in finds
            if f[: len(load_scope_chain)] == load_scope_chain[: len(f)]
            and len(f) <= len(load_scope_chain)
        ]

        longest_chain = max(finds, key=len)
        if len(longest_chain) == 1:
            return self.table[longest_chain[0]][name]

        return self.table[".".join(longest_chain)][name]


def to_symbol_table(term, table: SymbolTable, scope: str = "module"):
    if isinstance(term, File):
        to_symbol_table(term.expression, table, "module")

    elif isinstance(term, Let) and not isinstance(term.value, Function):
        table.insert(scope, term.name.text)
        to_symbol_table(term.next_term, table)

    elif isinstance(term, Let) and isinstance(term.value, Function):
        table.insert(scope, term.name.text)
        function_scope = f"{scope}.{term.name.text}"
        for param in term.value.parameters:
            table.insert(function_scope, param.text, "FAST")
        to_symbol_table(term.value.value, table, function_scope)
        to_symbol_table(term.next_term, table, scope)

    elif isinstance(term, Var):
        table.insert_load(scope, term.text)

    elif isinstance(term, Call):
        to_symbol_table(term.callee, table, scope)

    elif isinstance(term, Binary):
        to_symbol_table(term.lhs, table, scope)
        to_symbol_table(term.rhs, table, scope)

    return table