import json
import os
from types import CodeType, FunctionType, ModuleType
import unittest
import sys
from bytecode import Bytecode
from rinhac.ast.json_parser import parse_json_to_object
from rinhac.symbol_table import create_symbol_table
from rinhac import Compiler

_current_dir = os.path.dirname(os.path.abspath(__file__))

IF_ELSE_TEST_JSON = os.path.join(
    _current_dir, "test_data", "compiler", "if_else_test.json"
)
OPERATORS_TEST_JSON = os.path.join(
    _current_dir, "test_data", "compiler", "operators_test.json"
)
TUPLES_TEST_JSON = os.path.join(
    _current_dir, "test_data", "compiler", "tuples_test.json"
)
VARIABLES_TEST_JSON = os.path.join(
    _current_dir, "test_data", "compiler", "variables_test.json"
)


class TestCompiler(unittest.TestCase):    
    def _import_rinha_module(self, json_ast_file_path: str) -> ModuleType:
        code = self._build(json_ast_file_path)
        module_name = os.path.splitext(os.path.basename(code.co_filename))[0]
        module = ModuleType(module_name)
        module.__file__ = code.co_filename
        sys.modules[module_name] = module
        exec(code, module.__dict__)
        return module

    def _build(self, json_path) -> CodeType:
        with open(json_path) as f:
            json_ast = json.load(f)
        ast = parse_json_to_object(json_ast)
        symbol_table = create_symbol_table(ast)
        compiler = Compiler()
        return compiler.to_bytecode(ast, Bytecode(), symbol_table).to_code()
    

    def test_if_else(self):
        if_else_test = self._import_rinha_module(IF_ELSE_TEST_JSON)

        self.assertEqual(if_else_test.if_else_fn(10), 20)
        self.assertEqual(if_else_test.if_else_fn(30), 30)

    def test_operators(self):
        operators_test = self._import_rinha_module(OPERATORS_TEST_JSON)

        self.assertEqual(operators_test.add_fn(10, 20), 30)
        self.assertEqual(operators_test.sub_fn(10, 20), -10)
        self.assertEqual(operators_test.mul_fn(10, 20), 200)
        self.assertEqual(operators_test.div_fn(5, 2), 2)
        self.assertEqual(operators_test.rem_fn(10, 20), 10)
        self.assertEqual(operators_test.eq_fn(10, 20), False)
        self.assertEqual(operators_test.neq_fn(10, 20), True)
        self.assertEqual(operators_test.lt_fn(10, 20), True)
        self.assertEqual(operators_test.gt_fn(10, 20), False)
        self.assertEqual(operators_test.lte_fn(10, 20), True)
        self.assertEqual(operators_test.gte_fn(10, 20), False)
        self.assertEqual(operators_test.and_fn(True, False), False)
        self.assertEqual(operators_test.or_fn(True, False), True)

    def test_tuples(self):
        tuple_test = self._import_rinha_module(TUPLES_TEST_JSON)
        self.assertEqual(tuple_test.tuple_var, (1, 2))
        self.assertEqual(tuple_test.get_first_fn(tuple_test.tuple_var), 1)
        self.assertEqual(tuple_test.get_second_fn(tuple_test.tuple_var), 2)

    def test_variables(self):
        variables_test = self._import_rinha_module(VARIABLES_TEST_JSON)

        self.assertEqual(variables_test.module_var, "module_var")
        self.assertEqual(variables_test.module_fn("local_var"), "local_varmodule_var")
        # self.assertEqual(variables_test.inner_outer_fn(), "fn_var_outerfn_var_inner")
        self.assertEqual(variables_test.shadowing_fn(), "outerinner")
