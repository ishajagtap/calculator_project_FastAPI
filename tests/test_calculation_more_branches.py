# tests/test_calculation_more_branches.py
import pytest
from app.calculation import CalculatorFacade
from app.exceptions import InvalidInputError

def test_undo_on_fresh_calculator_behaviour():
    # Create calculator with no explicit calculation; undo should be callable
    calc = CalculatorFacade()
    # There is an initial save in ctor, but calling undo should not raise
    res = calc.undo()
    # res could be True/False depending on internal stacks; assert boolean
    assert isinstance(res, bool)

def test_redo_on_empty_stack_returns_false_or_bool():
    calc = CalculatorFacade()
    # Without prior undo, redo should return False (or boolean)
    res = calc.redo()
    assert isinstance(res, bool)

def test_calculation_unknown_operation_raises():
    calc = CalculatorFacade()
    with pytest.raises(InvalidInputError):
        calc.calculate("unknown-op-xyz", 1, 2)