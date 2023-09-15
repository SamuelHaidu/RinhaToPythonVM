from typing import List
from bytecode import Bytecode, Compare, Instr, CellVar, FreeVar, Label
from compiler.ast.json_parser import parse_json_to_object
import json
from typing import Dict
from compiler.ast import (
    BinaryOp,
    Var,
    Function,
    Call,
    Let,
    Str,
    Int,
    Binary,
    Bool,
    If,
    Tuple,
    First,
    Second,
    Print,
    File,
)
from compiler import SymbolTable
from compiler.symbol_table import to_symbol_table


class Compiler:
    binary_map = {
        BinaryOp.Add: Instr("BINARY_ADD"),
        BinaryOp.Sub: Instr("BINARY_SUBTRACT"),
        BinaryOp.Mul: Instr("BINARY_MULTIPLY"),
        BinaryOp.Div: Instr("BINARY_TRUE_DIVIDE"),
        BinaryOp.Rem: Instr("BINARY_MODULO"),
        BinaryOp.Eq: Instr("COMPARE_OP", Compare.EQ),
        BinaryOp.Neq: Instr("COMPARE_OP", Compare.NE),
        BinaryOp.Lt: Instr("COMPARE_OP", Compare.LT),
        BinaryOp.Gt: Instr("COMPARE_OP", Compare.GT),
        BinaryOp.Lte: Instr("COMPARE_OP", Compare.LE),
        BinaryOp.Gte: Instr("COMPARE_OP", Compare.GE),
        BinaryOp.And: Instr("BINARY_AND"),
        BinaryOp.Or: Instr("BINARY_OR"),
    }

    def __init__(self, symbol_table: SymbolTable):
        self.symbol_table = symbol_table

    def to_bytecode(self, term, bytecode: Bytecode, scope="module") -> Bytecode:
        if isinstance(term, File):
            self.filename = term.name
            bytecode = self.to_bytecode(term.expression, bytecode, "module")
            bytecode.extend(
                [Instr("POP_TOP"), Instr("LOAD_CONST", None), Instr("RETURN_VALUE")]
            )
            bytecode.name = "<rinha:module>"
            bytecode.filename = self.filename
            bytecode.first_lineno = term.location.start + 1
            return bytecode
        elif isinstance(term, Let) and not isinstance(term.value, Function):
            variable_name = term.name.text
            symbol = self.symbol_table.get_closest(scope, variable_name)
            if symbol["load_type"] == "NAME":
                bytecode.extend(self.to_bytecode(term.value, Bytecode(), scope))
                bytecode.append(Instr("STORE_NAME", variable_name))
            elif symbol["load_type"] == "DEREF":
                bytecode.extend(self.to_bytecode(term.value, Bytecode(), scope))
                bytecode.append(Instr("STORE_DEREF", CellVar(variable_name)))
            elif symbol["load_type"] == "FAST":
                bytecode.extend(self.to_bytecode(term.value, Bytecode(), scope))
                bytecode.append(Instr("STORE_FAST", variable_name))
            elif symbol["load_type"] == "GLOBAL":
                bytecode.extend(self.to_bytecode(term.value, Bytecode(), scope))
                bytecode.append(Instr("STORE_GLOBAL", variable_name))

            return self.to_bytecode(term.next_term, bytecode, scope)

        elif isinstance(term, Let) and isinstance(term.value, Function):
            function_name = term.name.text
            function_scope = f"{scope}.{function_name}"
            function_terms = term.value.value
            function_bytecode = Bytecode()
            function_bytecode.argcount = len(term.value.parameters)
            function_bytecode.argnames = [param.text for param in term.value.parameters]
            compiled_function_bytecode = self.to_bytecode(
                function_terms, Bytecode(), function_scope
            )
            function_bytecode.cellvars = compiled_function_bytecode.cellvars
            function_bytecode.freevars = compiled_function_bytecode.freevars
            function_bytecode.extend(compiled_function_bytecode)
            function_bytecode.append(Instr("RETURN_VALUE"))

            function_bytecode.name = function_name
            function_bytecode.filename = self.filename
            function_bytecode.first_lineno = term.location.start + 1

            bytecode.append(Instr("LOAD_CONST", function_bytecode.to_code()))
            bytecode.append(Instr("LOAD_CONST", function_name))
            function_flag = 0
            if function_bytecode.freevars:
                for freevar in function_bytecode.freevars:
                    bytecode.cellvars.append(
                        freevar
                    ) if freevar not in bytecode.cellvars else None
                    bytecode.append(Instr("LOAD_CLOSURE", CellVar(freevar)))
                bytecode.append(Instr("BUILD_TUPLE", len(function_bytecode.freevars)))
                function_flag = 8
            bytecode.append(Instr("MAKE_FUNCTION", function_flag))
            symbol = self.symbol_table.get_closest(scope, function_name)

            if symbol["load_type"] == "NAME":
                bytecode.append(Instr("STORE_NAME", function_name))
            elif symbol["load_type"] == "DEREF":
                bytecode.cellvars.append(
                    function_name
                ) if function_name not in bytecode.cellvars else None
                bytecode.append(Instr("STORE_DEREF", CellVar(function_name)))
            elif symbol["load_type"] == "FAST":
                bytecode.append(Instr("STORE_FAST", function_name))
            elif symbol["load_type"] == "GLOBAL":
                bytecode.append(Instr("STORE_GLOBAL", function_name))

            return self.to_bytecode(term.next_term, bytecode, scope)

        elif isinstance(term, Var):
            symbol = self.symbol_table.get_closest(scope, term.text)
            if symbol["load_type"] == "NAME":
                bytecode.append(Instr("LOAD_NAME", term.text))
            elif symbol["load_type"] == "DEREF":
                bytecode.freevars.append(
                    term.text
                ) if term.text not in bytecode.freevars else None
                bytecode.append(Instr("LOAD_DEREF", FreeVar(term.text)))
            elif symbol["load_type"] == "FAST":
                bytecode.append(Instr("LOAD_FAST", term.text))
            elif symbol["load_type"] == "GLOBAL":
                bytecode.append(Instr("LOAD_GLOBAL", term.text))

        elif isinstance(term, Call):
            callee_bytecode = self.to_bytecode(term.callee, Bytecode(), scope)
            arguments_bytecode = Bytecode()
            for arg in term.arguments:
                arguments_bytecode.extend(self.to_bytecode(arg, Bytecode(), scope))
            bytecode.extend(callee_bytecode)
            bytecode.extend(arguments_bytecode)
            bytecode.append(Instr("CALL_FUNCTION", len(term.arguments)))

        elif isinstance(term, Str) or isinstance(term, Int) or isinstance(term, Bool):
            bytecode.extend([Instr("LOAD_CONST", term.value)])

        elif isinstance(term, Binary):
            opcode = self.binary_map[term.op]
            bytecode.extend(self.to_bytecode(term.lhs, Bytecode(), scope))
            bytecode.extend(self.to_bytecode(term.rhs, Bytecode(), scope))
            bytecode.append(opcode)

        elif isinstance(term, Print):
            bytecode.append(Instr("LOAD_GLOBAL", "print"))
            bytecode.extend(self.to_bytecode(term.value, Bytecode(), scope))
            bytecode.append(Instr("CALL_FUNCTION", 1))

        elif isinstance(term, If):
            condition_bytecode = self.to_bytecode(term.condition, Bytecode(), scope)
            true_bytecode = self.to_bytecode(term.then, Bytecode(), scope)
            false_bytecode = self.to_bytecode(term.otherwise, Bytecode(), scope)
            bytecode.extend(condition_bytecode)
            else_label = Label()
            end_if_label = Label()
            bytecode.append(Instr("POP_JUMP_IF_FALSE", else_label))
            bytecode.extend(true_bytecode)
            bytecode.append(Instr("JUMP_FORWARD", end_if_label))
            bytecode.append(else_label)
            bytecode.extend(false_bytecode)
            bytecode.append(end_if_label)

        elif isinstance(term, Tuple):
            bytecode.extend(self.to_bytecode(term.first, Bytecode(), scope))
            bytecode.extend(self.to_bytecode(term.second, Bytecode(), scope))
            bytecode.append(Instr("BUILD_TUPLE", 2))

        elif isinstance(term, First):
            bytecode.extend(self.to_bytecode(term.value, Bytecode(), scope))
            bytecode.append(Instr("LOAD_CONST", 0))
            bytecode.append(Instr("BINARY_SUBSCR"))

        elif isinstance(term, Second):
            bytecode.extend(self.to_bytecode(term.value, Bytecode(), scope))
            bytecode.append(Instr("LOAD_CONST", 1))
            bytecode.append(Instr("BINARY_SUBSCR"))

        return bytecode


if __name__ == "__main__":
    with open("./first_test/first_test.json", "r") as f:
        data = json.load(f)
        data = parse_json_to_object(data)
    symbol_table = to_symbol_table(data, SymbolTable(), "module")
    compiler = Compiler(symbol_table)
    bytecode = compiler.to_bytecode(data, Bytecode())
    from compiler.utils import code_to_pyc_bytecode
    with open("./first_test/first_test.pyc", "wb") as f:
        f.write(code_to_pyc_bytecode(bytecode.to_code()))