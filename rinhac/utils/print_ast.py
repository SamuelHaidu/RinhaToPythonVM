import json
from rinhac.ast.json_parser import parse_json_to_object
from rinhac.ast.ast_objects import (
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
    prefix = "│   " * (depth - 1) + "├─ " if depth > 0 else ""

    def format_node(node):
        if isinstance(node, File):
            return f"[File {node.name}]"
        elif isinstance(node, Var):
            return f"Var {node.text}"
        elif isinstance(node, Function):
            params = " ".join(param.text for param in node.parameters)
            return f"Function {params}"
        elif isinstance(node, Call):
            return "Call"
        elif isinstance(node, Let):
            return f"Let {node.name.text}"
        elif isinstance(node, Str):
            return f'String "{node.value}"'
        elif isinstance(node, Int):
            return f"Int {node.value}"
        elif isinstance(node, Binary):
            return f"Binary Operator {node.op.value}"
        elif isinstance(node, Bool):
            return f"Bool {node.value}"
        elif isinstance(node, If):
            return "If"
        elif isinstance(node, Tuple):
            return "Tuple"
        elif isinstance(node, First):
            return "First"
        elif isinstance(node, Second):
            return "Second"
        elif isinstance(node, Print):
            return "Print"

    print(f"{prefix}{format_node(node)}")

    if isinstance(node, File):
        print_tree(node.expression, depth + 1)
    elif isinstance(node, Function):
        print_tree(node.value, depth + 1)
    elif isinstance(node, Call):
        print_tree(node.callee, depth + 1)
        for arg in node.arguments:
            print_tree(arg, depth + 2)
    elif isinstance(node, Let):
        print_tree(node.value, depth + 1)
        print_tree(node.next_term, depth)
    elif isinstance(node, Binary):
        print_tree(node.lhs, depth + 1)
        print_tree(node.rhs, depth + 1)
    elif isinstance(node, If):
        print_tree(node.condition, depth + 1)
        print_tree(node.then, depth + 1)
        print(prefix + "otherwise")
        print_tree(node.otherwise, depth + 1)
    elif isinstance(node, Tuple):
        print_tree(node.first, depth + 1)
        print_tree(node.second, depth + 1)
    elif isinstance(node, First) or isinstance(node, Second) or isinstance(node, Print):
        print_tree(node.value, depth + 1)


if __name__ == "__main__":
    with open("./test_if_else/test_if_else.json", "r") as f:
        tree_json = json.load(f)
        tree = parse_json_to_object(tree_json)
        print_tree(tree)
