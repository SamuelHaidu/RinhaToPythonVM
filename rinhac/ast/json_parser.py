from typing import Any, Dict
from rinhac.ast.ast_objects import (
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
