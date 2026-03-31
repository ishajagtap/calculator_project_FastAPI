# tests/test_input_validators_extra_edges.py
import pytest
from app.input_validators import parse_command
from app.exceptions import InvalidInputError

def test_parse_empty_input_raises():
    with pytest.raises(InvalidInputError):
        parse_command("")

def test_parse_non_numeric_operands():
    with pytest.raises(InvalidInputError):
        parse_command("add one two")