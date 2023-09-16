import json
import os
import unittest
from rinhac.ast.json_parser import parse_json_to_object

from rinhac.symbol_table import create_symbol_table
from rinhac.utils.index_line_mapper import IndexLineMapper

_current_dir = os.path.dirname(os.path.abspath(__file__))
EXAMPLE_AST_JSON_PATH = os.path.join(_current_dir, "test_data", "symbol_table_test.json")


class TestSymbolTable(unittest.TestCase):
    def test_symbol_table(self):
        with open(EXAMPLE_AST_JSON_PATH) as f:
            json_ast = json.load(f)
        index_line_mapper = IndexLineMapper(EXAMPLE_AST_JSON_PATH)
        ast = parse_json_to_object(json_ast)
        symbol_table = create_symbol_table(ast)

        """ Tree structure of symbol table
         Function add NAME
        ├─  Var a FAST
        ├─  Var b FAST
        Function minus NAME
        ├─  Var a DEREF
        ├─  Var b FAST
        ├─  Function useless_fn FAST
        """
        self.assertEqual(symbol_table.lookup("add").symbol_type, "Function")
        self.assertEqual(symbol_table.lookup("add").load_type, "NAME")
        self.assertEqual(symbol_table.lookup("add").referenced_count, 0)

        self.assertEqual(symbol_table.lookup("minus").symbol_type, "Function")
        self.assertEqual(symbol_table.lookup("minus").load_type, "NAME")
        self.assertEqual(symbol_table.lookup("minus").referenced_count, 0)

        add_table = symbol_table.get_context("add")
        self.assertEqual(add_table.lookup("a").symbol_type, "Var")
        self.assertEqual(add_table.lookup("a").load_type, "FAST")
        self.assertEqual(add_table.lookup("a").referenced_count, 1)

        self.assertEqual(add_table.lookup("b").symbol_type, "Var")
        self.assertEqual(add_table.lookup("b").load_type, "FAST")
        self.assertEqual(add_table.lookup("b").referenced_count, 1)

        minus_table = symbol_table.get_context("minus")
        self.assertEqual(minus_table.lookup("a").symbol_type, "Var")
        self.assertEqual(minus_table.lookup("a").load_type, "DEREF")
        self.assertEqual(minus_table.lookup("a").referenced_count, 1)

        self.assertEqual(minus_table.lookup("b").symbol_type, "Var")
        self.assertEqual(minus_table.lookup("b").load_type, "FAST")
        self.assertEqual(minus_table.lookup("b").referenced_count, 1)

        self.assertEqual(minus_table.lookup("useless_fn").symbol_type, "Function")
        self.assertEqual(minus_table.lookup("useless_fn").load_type, "FAST")
        self.assertEqual(minus_table.lookup("useless_fn").referenced_count, 1)
