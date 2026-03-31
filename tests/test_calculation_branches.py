# tests/test_calculation_branches.py
import pytest
from app.calculation import CalculatorFacade
from app.exceptions import InvalidInputError
from pathlib import Path

def test_unknown_operation_raises():
    calc = CalculatorFacade()
    with pytest.raises(InvalidInputError):
        calc.calculate("this_op_does_not_exist", 1, 2)

def test_save_and_load_history_roundtrip(tmp_path):
    calc = CalculatorFacade()
    calc.calculate("add", 1, 2)
    csv = tmp_path / "h.csv"
    calc.save_history(str(csv))
    assert csv.exists()
    # create new calculator and load
    calc2 = CalculatorFacade()
    calc2.load_history(str(csv))
    df = calc2.get_history_df()
    assert not df.empty
    assert df.iloc[0]["operation"] == "add"