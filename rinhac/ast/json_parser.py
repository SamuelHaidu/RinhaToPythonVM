from typing import Any, Dict
from rinhac.ast.ast_objects import (
    BinaryOp,
    Parameter,
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
from rinhac.utils.index_line_mapper import IndexLineMapper


def parse_parameter(json_parameter: Dict[str, Any], index_line_mapper: IndexLineMapper) -> Parameter:
    return Parameter(
        text=json_parameter["text"],
        location=parse_location(json_parameter["location"], index_line_mapper),
    )


def parse_location(
    json_location: Dict[str, Any], index_line_mapper: IndexLineMapper
) -> Location:
    start = json_location["start"]
    end = json_location["end"]
    filename = json_location["filename"]
    line_number = index_line_mapper.get_line_number(start)
    return Location(start=start, end=end, filename=filename, line_number=line_number)


def parse_json_to_object(
    json_data: Dict[str, Any], index_line_mapper: IndexLineMapper
) -> File:
    has_expression = "expression" in json_data
    if has_expression:
        return File(
            name=json_data["name"],
            expression=parse_json_to_object(json_data["expression"], index_line_mapper),
            location=parse_location(json_data["location"], index_line_mapper),
        )
    is_a_term = "kind" in json_data
    if is_a_term:
        kind = json_data["kind"]
        location = parse_location(json_data["location"], index_line_mapper)

        if kind == "Var":
            return Var(text=json_data["text"], location=location)
        elif kind == "Function":
            return Function(
                parameters=[
                    parse_parameter(parameter, index_line_mapper) for parameter in json_data["parameters"]
                ],
                value=parse_json_to_object(json_data["value"], index_line_mapper),
                location=location,
            )
        elif kind == "Call":
            return Call(
                callee=parse_json_to_object(json_data["callee"], index_line_mapper),
                arguments=[
                    parse_json_to_object(argument, index_line_mapper)
                    for argument in json_data["arguments"]
                ],
                location=location,
            )
        elif kind == "Let":
            return Let(
                name=parse_parameter(json_data["name"], index_line_mapper),
                value=parse_json_to_object(json_data["value"], index_line_mapper),
                next_term=parse_json_to_object(json_data["next"], index_line_mapper),
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
                lhs=parse_json_to_object(json_data["lhs"], index_line_mapper),
                op=BinaryOp(json_data["op"]),
                rhs=parse_json_to_object(json_data["rhs"], index_line_mapper),
                location=location,
            )
        elif kind == "Bool":
            return Bool(
                value=json_data["value"],
                location=location,
            )
        elif kind == "If":
            return If(
                condition=parse_json_to_object(json_data["condition"], index_line_mapper),
                then=parse_json_to_object(json_data["then"], index_line_mapper),
                otherwise=parse_json_to_object(json_data["otherwise"], index_line_mapper),
                location=location,
            )
        elif kind == "Tuple":
            return Tuple(
                first=parse_json_to_object(json_data["first"], index_line_mapper),
                second=parse_json_to_object(json_data["second"], index_line_mapper),
                location=location,
            )
        elif kind == "First":
            return First(
                value=parse_json_to_object(json_data["value"], index_line_mapper),
                location=location,
            )
        elif kind == "Second":
            return Second(
                value=parse_json_to_object(json_data["value"], index_line_mapper),
                location=location,
            )
        elif kind == "Print":
            return Print(
                value=parse_json_to_object(json_data["value"], index_line_mapper),
                location=location,
            )
