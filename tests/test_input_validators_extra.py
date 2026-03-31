# tests/test_input_validators_extra.py
import pytest
from app.input_validators import parse_command
from app.exceptions import InvalidInputError

def test_parse_clear_command():
    cmd, a, b = parse_command("clear")
    assert cmd == "clear" and a is None and b is None

def test_parse_invalid_operands():
    with pytest.raises(InvalidInputError):
        parse_command("add one two")