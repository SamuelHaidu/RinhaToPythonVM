from enum import Enum
from dataclasses import dataclass
from abc import ABC
from typing import Any, Dict


class Term(ABC):
    pass


@dataclass(slots=True)
class Location:
    start: int
    end: int
    filename: str


@dataclass(slots=True)
class File:
    name: str
    expression: Term
    location: Location


@dataclass(slots=True)
class Parameter:
    text: str
    location: Location


@dataclass(slots=True)
class Var(Term):
    text: str
    location: Location


@dataclass(slots=True)
class Function(Term):
    parameters: list[Parameter]
    value: Term
    location: Location


@dataclass(slots=True)
class Call(Term):
    callee: Term
    arguments: list[Term]
    location: Location


@dataclass(slots=True)
class Let(Term):
    name: Parameter
    value: Term
    next_term: Term
    location: Location


@dataclass(slots=True)
class Str(Term):
    value: str
    location: Location


@dataclass(slots=True)
class Int(Term):
    value: int
    location: Location


class BinaryOp(Enum):
    Add = "Add"
    Sub = "Sub"
    Mul = "Mul"
    Div = "Div"
    Rem = "Rem"
    Eq = "Eq"
    Neq = "Neq"
    Lt = "Lt"
    Gt = "Gt"
    Lte = "Lte"
    Gte = "Gte"
    And = "And"
    Or = "Or"


@dataclass(slots=True)
class Binary(Term):
    lhs: Term
    op: BinaryOp
    rhs: Term
    location: Location


@dataclass(slots=True)
class Bool(Term):
    value: bool
    location: Location


@dataclass(slots=True)
class If(Term):
    condition: Term
    then: Term
    otherwise: Term
    location: Location


@dataclass(slots=True)
class Tuple(Term):
    first: Term
    second: Term
    location: Location


@dataclass(slots=True)
class First(Term):
    value: Term
    location: Location


@dataclass(slots=True)
class Second(Term):
    value: Term
    location: Location


@dataclass(slots=True)
class Print(Term):
    value: Term
    location: Location
