import json

from compiler.ast.rinha_ast import parse_json_to_object
from compiler.ast.ast_objects import (
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


def print_tree(node, depth=0):
    ident = "  " * depth
    if isinstance(node, File):
        print("File: " + node.name)
        print_tree(node.expression, depth + 1)
    elif isinstance(node, Var):
        print(ident + "Var " + node.text)
    elif isinstance(node, Function):
        print(ident + "Function", end=" ")
        for param in node.parameters:
            print(param.text, end=" ")
        print()
        print_tree(node.value, depth + 1)
    elif isinstance(node, Call):
        print(ident + "Call:")
        print_tree(node.callee, depth + 1)
        for arg in node.arguments:
            print_tree(arg, depth + 1)
    elif isinstance(node, Let):
        print(ident + "Let:")
        print(ident + "Name: " + node.name.text)
        print_tree(node.value, depth + 1)
        print_tree(node.next_term, depth)
    elif isinstance(node, Str):
        print(ident + 'String: "' + node.value + '"')
    elif isinstance(node, Int):
        print(ident + "Int: " + str(node.value))
    elif isinstance(node, Binary):
        print(ident + "Binary:")
        print_tree(node.lhs, depth + 1)
        print(ident + "Operator: " + node.op.value)
        print_tree(node.rhs, depth + 1)
    elif isinstance(node, Bool):
        print(ident + "Bool: " + str(node.value))
    elif isinstance(node, If):
        print(ident + "If:")
        print_tree(node.condition, depth + 1)
        print(ident + "Then:")
        print_tree(node.then, depth + 1)
        print(ident + "Else:")
        print_tree(node.otherwise, depth + 1)
    elif isinstance(node, Tuple):
        print(ident + "Tuple:")
        print_tree(node.first, depth + 1)
        print_tree(node.second, depth + 1)
    elif isinstance(node, First):
        print(ident + "First:")
        print_tree(node.value, depth + 1)
    elif isinstance(node, Second):
        print(ident + "Second:")
        print_tree(node.value, depth + 1)
    elif isinstance(node, Print):
        print(ident + "Print:")
        print_tree(node.value, depth + 1)


if __name__ == "__main__":
    with open("./tuple_test/tuple_test.json", "r") as f:
        tree_json = json.load(f)
        tree = parse_json_to_object(tree_json)
        print_tree(tree)