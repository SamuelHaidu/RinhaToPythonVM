from typing import Any, Dict
from compiler.ast.ast_objects import (
    BinaryOp,
    Parameter,
    Term,
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
    Location,
)


def parse_parameter(json_parameter: Dict[str, Any]) -> Parameter:
    return Parameter(
        text=json_parameter["text"],
        location=Location(**json_parameter["location"]),
    )


def parse_json_to_object(json_data) -> File:
    has_expression = "expression" in json_data
    if has_expression:
        return File(
            name=json_data["name"],
            expression=parse_json_to_object(json_data["expression"]),
            location=Location(**json_data["location"]),
        )
    is_a_term = "kind" in json_data
    if is_a_term:
        kind = json_data["kind"]
        location = Location(**json_data["location"])

        if kind == "Var":
            return Var(text=json_data["text"], location=location)
        elif kind == "Function":
            return Function(
                parameters=[
                    parse_parameter(parameter) for parameter in json_data["parameters"]
                ],
                value=parse_json_to_object(json_data["value"]),
                location=location,
            )
        elif kind == "Call":
            return Call(
                callee=parse_json_to_object(json_data["callee"]),
                arguments=[
                    parse_json_to_object(argument)
                    for argument in json_data["arguments"]
                ],
                location=location,
            )
        elif kind == "Let":
            return Let(
                name=parse_parameter(json_data["name"]),
                value=parse_json_to_object(json_data["value"]),
                next_term=parse_json_to_object(json_data["next"]),
                location=location,
            )
        elif kind == "Str":
            return Str(
                value=json_data["value"],
                location=location,
            )
        elif kind == "Int":
            return Int(
                value=json_data["value"],
                location=location,
            )
        elif kind == "Binary":
            return Binary(
                lhs=parse_json_to_object(json_data["lhs"]),
                op=BinaryOp(json_data["op"]),
                rhs=parse_json_to_object(json_data["rhs"]),
                location=location,
            )
        elif kind == "Bool":
            return Bool(
                value=json_data["value"],
                location=location,
            )
        elif kind == "If":
            return If(
                condition=parse_json_to_object(json_data["condition"]),
                then=parse_json_to_object(json_data["then"]),
                otherwise=parse_json_to_object(json_data["otherwise"]),
                location=location,
            )
        elif kind == "Tuple":
            return Tuple(
                first=parse_json_to_object(json_data["first"]),
                second=parse_json_to_object(json_data["second"]),
                location=location,
            )
        elif kind == "First":
            return First(
                value=parse_json_to_object(json_data["value"]),
                location=location,
            )
        elif kind == "Second":
            return Second(
                value=parse_json_to_object(json_data["value"]),
                location=location,
            )
        elif kind == "Print":
            return Print(
                value=parse_json_to_object(json_data["value"]),
                location=location,
            )


def print_term_tree(file: File):
    print(file.name)
    print_term(file.expression, 0)


def print_term(term: Term, level: int):
    print(" " * level, end="")
    if isinstance(term, Var):
        print(f"Var {term.text}")
    elif isinstance(term, Function):
        print("Function", end=" ")
        for parameter in term.parameters:
            print(parameter.text, end=" ")
        print()
        print_term(term.value, level + 2)
    elif isinstance(term, Call):
        print("Call")
        print_term(term.callee, level + 2)
        for argument in term.arguments:
            print_term(argument, level + 2)
    elif isinstance(term, Let):
        print("Let", term.name.text)
        print_term(term.value, level + 2)
        print_term(term.next_term, level + 2)
    elif isinstance(term, Str):
        print(f'Str "{term.value}"')
    elif isinstance(term, Int):
        print(f"Int {term.value}")
    elif isinstance(term, Binary):
        print(f"Binary {term.op.name}")
        print_term(term.lhs, level + 2)
        print_term(term.rhs, level + 2)
    elif isinstance(term, Bool):
        print(f"Bool {term.value}")
    elif isinstance(term, If):
        print("If")
        print_term(term.condition, level + 2)
        print_term(term.then, level + 2)
        print_term(term.otherwise, level + 2)
    elif isinstance(term, Tuple):
        print("Tuple")
        print_term(term.first, level + 2)
        print_term(term.second, level + 2)
    elif isinstance(term, First):
        print("First")
        print_term(term.value, level + 2)
    elif isinstance(term, Second):
        print("Second")
        print_term(term.value, level + 2)
    elif isinstance(term, Print):
        print("Print")
        print_term(term.value, level + 2)
