# tests/test_calculation_internal.py
import pytest
import pandas as pd
from app.calculation import CalculatorFacade

def test_capture_and_restore_empty_and_with_history(tmp_path):
    calc = CalculatorFacade()
    # perform a calc to create history entry
    res = calc.calculate("add", 2, 3)
    assert res == 5
    # capture state after calculation
    state = calc._capture_state()
    assert "last_result" in state
    assert state["last_result"] == 5

    # modify state and restore an empty state (simulate missing history)
    empty_state = {"last_result": None, "history": {}}
    calc._restore_state(empty_state)
    assert calc._last_result is None
    # restore the previously captured state
    calc._restore_state(state)
    assert calc._last_result == 5

def test_save_load_history_roundtrip(tmp_path):
    calc = CalculatorFacade()
    calc.calculate("mul", 4, 5)
    p = tmp_path / "h.csv"
    calc.save_history(str(p))
    assert p.exists()
    # load into a fresh calculator
    calc2 = CalculatorFacade()
    calc2.load_history(str(p))
    df = calc2.get_history_df()
    assert not df.empty
    assert df.iloc[-1]["operation"] in {"mul", "*"}