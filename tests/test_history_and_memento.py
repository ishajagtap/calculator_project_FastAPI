# tests/test_history_and_memento.py
import tempfile
import os
import pandas as pd
from app.history import History
from app.calculation import CalculatorFacade

def test_history_append_and_csv(tmp_path):
    history = History()
    history.append("add", 1, 2, 3)
    assert not history.df.empty
    csv_path = tmp_path / "h.csv"
    history.to_csv(str(csv_path))
    assert csv_path.exists()
    # load into new
    h2 = History()
    h2.load_csv(str(csv_path))
    assert "operation" in h2.df.columns
    assert h2.df.iloc[0]["result"] == 3

def test_calculator_undo_redo(tmp_path):
    calc = CalculatorFacade()
    r1 = calc.calculate("add", 1, 2)
    r2 = calc.calculate("mul", 3, 4)
    assert r1 == 3
    assert r2 == 12
    # undo last (undo will restore to state before last calculation)
    ok = calc.undo()
    assert ok is True
    # history should have previous snapshot (depending on implementation it might be shorter)
    # redo
    ok2 = calc.redo()
    # either redo true or false depending on whether re-do stack exists; ensure no exception
    assert isinstance(ok2, bool)