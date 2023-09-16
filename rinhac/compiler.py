from bytecode import Bytecode, Compare, Instr, CellVar, FreeVar, Label
from rinhac.ast import (
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
from rinhac import SymbolTable
from rinhac.symbol_table import SymbolTable


class Compiler:
    binary_map = {
        BinaryOp.Add: Instr("BINARY_ADD"),
        BinaryOp.Sub: Instr("BINARY_SUBTRACT"),
        BinaryOp.Mul: Instr("BINARY_MULTIPLY"),
        BinaryOp.Div: Instr("BINARY_FLOOR_DIVIDE"),
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

    @staticmethod
    def _extend_vars(origin: Bytecode, new: Bytecode):
        origin.cellvars = list(set(origin.cellvars).union(set(new.cellvars)))
        origin.freevars = list(set(origin.freevars).union(set(new.freevars)))

    def to_bytecode(
        self, term, bytecode: Bytecode, symbol_table: SymbolTable
    ) -> Bytecode:
        if isinstance(term, File):
            bytecode = self.to_bytecode(term.expression, bytecode, symbol_table)
            bytecode.extend(
                [Instr("POP_TOP"), Instr("LOAD_CONST", None), Instr("RETURN_VALUE")]
            )
            bytecode.name = "<rinha:module>"
            bytecode.filename = term.location.filename
            bytecode.first_lineno = term.location.line_number
            return bytecode
        elif isinstance(term, Let) and not isinstance(term.value, Function):
            variable_name = term.name.text
            symbol = symbol_table.lookup(variable_name)
            if symbol.load_type == "NAME":
                bytecode.extend(self.to_bytecode(term.value, Bytecode(), symbol_table))
                bytecode.append(
                    Instr("STORE_NAME", variable_name, lineno=term.location.line_number)
                )
            elif symbol.load_type == "DEREF":
                bytecode.extend(self.to_bytecode(term.value, Bytecode(), symbol_table))
                bytecode.cellvars.append(
                    variable_name
                ) if variable_name not in bytecode.cellvars else None
                bytecode.append(
                    Instr(
                        "STORE_DEREF",
                        CellVar(variable_name),
                        lineno=term.location.line_number,
                    )
                )
            elif symbol.load_type == "FAST":
                bytecode.extend(self.to_bytecode(term.value, Bytecode(), symbol_table))
                bytecode.append(
                    Instr("STORE_FAST", variable_name, lineno=term.location.line_number)
                )
            elif symbol.load_type == "GLOBAL":
                bytecode.extend(self.to_bytecode(term.value, Bytecode(), symbol_table))
                bytecode.append(
                    Instr(
                        "STORE_GLOBAL", variable_name, lineno=term.location.line_number
                    )
                )

            return self.to_bytecode(term.next_term, bytecode, symbol_table)

        elif isinstance(term, Let) and isinstance(term.value, Function):
            function_name = term.name.text
            function_symbol_table = symbol_table.get_context(function_name)
            function_terms = term.value.value
            function_bytecode = Bytecode()
            function_bytecode.argcount = len(term.value.parameters)
            function_bytecode.argnames = [param.text for param in term.value.parameters]
            compiled_function_bytecode = self.to_bytecode(
                function_terms, Bytecode(), function_symbol_table
            )
            function_bytecode.cellvars = compiled_function_bytecode.cellvars
            function_bytecode.freevars = compiled_function_bytecode.freevars
            function_bytecode.extend(compiled_function_bytecode)
            function_bytecode.append(Instr("RETURN_VALUE"))

            function_bytecode.name = function_name
            function_bytecode.filename = term.location.filename
            function_bytecode.first_lineno = term.location.start + 1

            bytecode.append(
                Instr(
                    "LOAD_CONST",
                    function_bytecode.to_code(),
                    lineno=term.value.location.line_number,
                )
            )
            bytecode.append(
                Instr(
                    "LOAD_CONST", function_name, lineno=term.value.location.line_number
                )
            )
            function_flag = 0
            if function_bytecode.freevars:
                for freevar in function_bytecode.freevars:
                    bytecode.cellvars.append(
                        freevar
                    ) if freevar not in bytecode.cellvars else None
                    bytecode.append(Instr("LOAD_CLOSURE", CellVar(freevar), lineno=term.value.location.line_number))
                bytecode.append(Instr("BUILD_TUPLE", len(function_bytecode.freevars), lineno=term.value.location.line_number))
                function_flag = 8
            bytecode.append(Instr("MAKE_FUNCTION", function_flag, lineno=term.value.location.line_number))
            symbol = symbol_table.lookup(function_name)

            if symbol.load_type == "NAME":
                bytecode.append(Instr("STORE_NAME", function_name, lineno=term.value.location.line_number))
            elif symbol.load_type == "DEREF":
                bytecode.cellvars.append(
                    function_name
                ) if function_name not in bytecode.cellvars else None
                bytecode.append(Instr("STORE_DEREF", CellVar(function_name), lineno=term.value.location.line_number))
            elif symbol.load_type == "FAST":
                bytecode.append(Instr("STORE_FAST", function_name, lineno=term.value.location.line_number))
            elif symbol.load_type == "GLOBAL":
                bytecode.append(Instr("STORE_GLOBAL", function_name, lineno=term.value.location.line_number))

            return self.to_bytecode(term.next_term, bytecode, symbol_table)

        elif isinstance(term, Var):
            symbol = symbol_table.lookup(term.text)
            if symbol.load_type == "NAME":
                bytecode.append(Instr("LOAD_NAME", term.text, lineno=term.location.line_number))
            elif symbol.load_type == "DEREF":
                bytecode.freevars.append(
                    term.text
                ) if term.text not in bytecode.freevars else None
                bytecode.append(Instr("LOAD_DEREF", FreeVar(term.text), lineno=term.location.line_number))
            elif symbol.load_type == "FAST":
                bytecode.append(Instr("LOAD_FAST", term.text, lineno=term.location.line_number))
            elif symbol.load_type == "GLOBAL":
                bytecode.append(Instr("LOAD_GLOBAL", term.text, lineno=term.location.line_number))

        elif isinstance(term, Call):
            callee_bytecode = self.to_bytecode(term.callee, Bytecode(), symbol_table)
            arguments_bytecode = Bytecode()
            for arg in term.arguments:
                arguments_bytecode.extend(
                    self.to_bytecode(arg, Bytecode(), symbol_table)
                )
            bytecode.extend(callee_bytecode)
            bytecode.extend(arguments_bytecode)
            bytecode.append(Instr("CALL_FUNCTION", len(term.arguments), lineno=term.location.line_number))

        elif isinstance(term, Str) or isinstance(term, Int) or isinstance(term, Bool):
            bytecode.extend([Instr("LOAD_CONST", term.value, lineno=term.location.line_number)])

        elif isinstance(term, Binary):
            opcode = self.binary_map[term.op]
            left_code = self.to_bytecode(term.lhs, Bytecode(), symbol_table)
            self._extend_vars(bytecode, left_code)
            right_code = self.to_bytecode(term.rhs, Bytecode(), symbol_table)
            self._extend_vars(bytecode, right_code)
            bytecode.extend(left_code)
            bytecode.extend(right_code)
            bytecode.append(opcode)

        elif isinstance(term, Print):
            bytecode.append(Instr("LOAD_GLOBAL", "print", lineno=term.location.line_number))
            value_bytecode = self.to_bytecode(term.value, Bytecode(), symbol_table)
            bytecode.extend(value_bytecode)
            bytecode.append(Instr("CALL_FUNCTION", 1, lineno=term.location.line_number))

        elif isinstance(term, If):
            condition_bytecode = self.to_bytecode(
                term.condition, Bytecode(), symbol_table
            )
            true_bytecode = self.to_bytecode(term.then, Bytecode(), symbol_table)
            self._extend_vars(bytecode, true_bytecode)
            false_bytecode = self.to_bytecode(term.otherwise, Bytecode(), symbol_table)
            self._extend_vars(bytecode, false_bytecode)
            bytecode.extend(condition_bytecode)
            else_label = Label()
            end_if_label = Label()
            bytecode.append(Instr("POP_JUMP_IF_FALSE", else_label, lineno=term.location.line_number))
            bytecode.extend(true_bytecode)
            bytecode.append(Instr("JUMP_FORWARD", end_if_label, lineno=true_bytecode[-1].lineno))
            bytecode.append(else_label)
            bytecode.extend(false_bytecode)
            bytecode.append(end_if_label)

        elif isinstance(term, Tuple):
            first_bytecode = self.to_bytecode(term.first, Bytecode(), symbol_table)
            self._extend_vars(bytecode, first_bytecode)
            second_bytecode = self.to_bytecode(term.second, Bytecode(), symbol_table)
            self._extend_vars(bytecode, second_bytecode)
            bytecode.extend(first_bytecode)
            bytecode.extend(second_bytecode)
            bytecode.append(Instr("BUILD_TUPLE", 2, lineno=term.location.line_number))

        elif isinstance(term, First):
            value_bytecode = self.to_bytecode(term.value, Bytecode(), symbol_table)
            self._extend_vars(bytecode, value_bytecode)
            bytecode.extend(value_bytecode)
            bytecode.append(Instr("LOAD_CONST", 0, lineno=term.location.line_number))
            bytecode.append(Instr("BINARY_SUBSCR", lineno=term.location.line_number))

        elif isinstance(term, Second):
            value_bytecode = self.to_bytecode(term.value, Bytecode(), symbol_table)
            self._extend_vars(bytecode, value_bytecode)
            bytecode.extend(value_bytecode)
            bytecode.append(Instr("LOAD_CONST", 1, lineno=term.location.line_number))
            bytecode.append(Instr("BINARY_SUBSCR", lineno=term.location.line_number))

        return bytecode
