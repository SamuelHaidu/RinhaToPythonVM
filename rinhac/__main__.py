#!/usr/bin/env python3
import argparse
import json
import os
from rinhac.ast.ast_objects import File
from rinhac.ast.json_parser import parse_json_to_object
from rinhac.compiler import Compiler
from rinhac.symbol_table import SymbolTable, create_symbol_table, print_symbol_table
from rinhac.utils.index_line_mapper import IndexLineMapper
from rinhac.utils.print_ast import print_tree
from rinhac.utils.pyc_converter import code_to_pyc_bytecode
from bytecode import Bytecode


def _get_ast(ast_file_path) -> File:
    try:
        with open(ast_file_path, "r") as f:
            json_ast = json.load(f)
            index_line_mapper = IndexLineMapper(ast_file_path)
            ast = parse_json_to_object(json_ast, index_line_mapper)
            return ast
    except FileNotFoundError:
        print("File not found:", ast_file_path)
        exit(1)
    except json.JSONDecodeError:
        print("File is not a valid JSON:", ast_file_path)
        exit(1)


def _get_symbol_table(ast: File) -> SymbolTable:
    return create_symbol_table(ast)


def build(ast_file, output):
    if output is None:
        output = os.path.splitext(ast_file)[0] + ".pyc"

    output_parts = os.path.splitext(output)
    has_no_extension = output_parts[1] == ""
    if has_no_extension:
        output = output_parts[0] + ".pyc"

    ast = _get_ast(ast_file)
    symbol_table = _get_symbol_table(ast)
    compiler = Compiler()
    ast_bytecode = compiler.to_bytecode(ast, Bytecode(), symbol_table)
    ast_code = ast_bytecode.to_code()
    pyc_data = code_to_pyc_bytecode(ast_code)

    with open(output, "wb") as f:
        f.write(pyc_data)


def print_ast(ast_file):
    ast = _get_ast(ast_file)
    print_tree(ast)


def print_symbol(ast_file):
    ast = _get_ast(ast_file)
    symbol_table = _get_symbol_table(ast)
    print_symbol_table(symbol_table)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Rinhac compiler. Compiles Rinhac AST to Python bytecode."
    )
    parser.add_argument("filename", help="Path to the file containing the AST.")

    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        "-b", "--build", action="store_true", help="Build pyc from the AST."
    )
    group.add_argument("-a", "--print-ast", action="store_true", help="Print the AST.")
    group.add_argument(
        "-s", "--print-symbol", action="store_true", help="Print the symbol table."
    )
    group.add_argument(
        "-o", "--output", action="store", help="Output file.", default=None
    )

    args = parser.parse_args()

    if args.build:
        build(args.filename, args.output)
    elif args.print_ast:
        print_ast(args.filename)
    elif args.print_symbol:
        print_symbol(args.filename)
    else:
        build(args.filename, args.output)
