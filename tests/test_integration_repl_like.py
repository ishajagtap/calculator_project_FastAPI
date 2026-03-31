# tests/test_integration_repl_like.py
from app.calculation import CalculatorFacade

def test_multiple_calcs_and_history():
    calc = CalculatorFacade()
    assert calc.calculate("add", 2, 2) == 4
    assert calc.calculate("pow", 2, 5) == 32
    df = calc.get_history_df()
    assert len(df) == 2
    assert df.iloc[0]["operation"] in {"add", "+"}