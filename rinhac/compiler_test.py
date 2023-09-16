import json
import os
from types import CodeType
import unittest
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
    def setUp(self) -> None:
        self.if_else_test_code = (self._build(IF_ELSE_TEST_JSON),)
        self.operators_test_code = (self._build(OPERATORS_TEST_JSON),)
        self.tuples_test_code = (self._build(TUPLES_TEST_JSON),)
        self.variables_test_code = self._build(VARIABLES_TEST_JSON)
        return super().setUp()

    def _build(self, json_path) -> CodeType:
        with open(json_path) as f:
            json_ast = json.load(f)
        ast = parse_json_to_object(json_ast)
        symbol_table = create_symbol_table(ast)
        compiler = Compiler(symbol_table)
        return compiler.to_bytecode(ast).to_code()

    def test_if_else(self):
        """rinha code:
        let if_else_fn = fn(a) => {
            let b = 20;
            if (a < b){
                b
            } else {
                a
            }
        };
        """
        exec(self.if_else_test_code)
        self.assertEqual(if_else_fn(10), 20)
        self.assertEqual(if_else_fn(30), 30)

    def test_operators(self):
        """rinha code:
        // Soma:
        let add_fn = fn(a, b) => {
            a + b
        }

        // Subtração:
        let sub_fn = fn(a, b) => {
            a - b
        }

        // Multiplicação:
        let mul_fn = fn(a, b) => {
            a * b
        }

        // Divisão:
        let div_fn = fn(a, b) => {
            a / b
        }

        // Resto da divisão:
        let rem_fn = fn(a, b) => {
            a % b
        }

        // Igualdade:
        let eq_fn = fn(a, b) => {
            a == b
        }

        // Diferente:
        let neq_fn = fn(a, b) => {
            a != b
        }

        // Menor:
        let lt_fn = fn(a, b) => {
            a < b
        }

        let gt_fn = fn(a, b) => {
            a > b
        }

        let lte_fn = fn(a, b) => {
            a <= b
        }

        let gte_fn = fn(a, b) => {
            a >= b
        }

        let and_fn = fn(a, b) => {
            a && b
        }

        let or_fn = fn(a, b) => {
            a || b
        }

        """
        exec(self.operators_test_code)
        self.assertEqual(add_fn(10, 20), 30)
        self.assertEqual(sub_fn(10, 20), -10)
        self.assertEqual(mul_fn(10, 20), 200)
        self.assertEqual(div_fn(10, 20), 0.5)
        self.assertEqual(rem_fn(10, 20), 10)
        self.assertEqual(eq_fn(10, 20), False)
        self.assertEqual(neq_fn(10, 20), True)
        self.assertEqual(lt_fn(10, 20), True)
        self.assertEqual(gt_fn(10, 20), False)
        self.assertEqual(lte_fn(10, 20), True)
        self.assertEqual(gte_fn(10, 20), False)
        self.assertEqual(and_fn(True, False), False)
        self.assertEqual(or_fn(True, False), True)

    def test_tuples(self):
        """rinha code:
        let tuple_var = (1, 2)

        let get_first_fn = fn(tuple) {
            first(tuple)
        };

        let get_second_fn = fn(tuple) {
            second(tuple)
        };
        """
        exec(self.tuples_test_code)
        self.assertEqual(tuple_var, (1, 2))
        self.assertEqual(get_first_fn(tuple_var), 1)
        self.assertEqual(get_second_fn(tuple_var), 2)

    def test_variables(self):
        """rinha code:
        let module_var = "module_var";

        let module_fn = fn(local_var) => {
            local_var + module_var
        };

        let inner_outer_fn = fn() => {
            let fn_var = "fn_var_outer"
            let inner_fun = fn() => {
                let fn_var_inner = "fn_var_inner"
                fn_var + fn_var_inner
            }
            inner_fun()
        };

        let shadowing_fn = fn() => {
            let shadowed = "outer"
            let shadow = fn() => {
                let shadowed = "inner"
                shadowed
            }
            shadow()
        };
        """

        exec(self.variables_test_code)
        self.assertEqual(module_var, "module_var")
        self.assertEqual(module_fn("local_var"), "local_varmodule_var")
        self.assertEqual(inner_outer_fn()(), "fn_var_outerfn_var_inner")
        self.assertEqual(shadowing_fn()(), "inner")
