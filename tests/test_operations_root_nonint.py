# tests/test_operations_root_nonint.py
import pytest
from app.operations import Root

def test_root_with_non_int_b_triggers_except_branch():
    """
    Calls Root.execute with a non-numeric 'b' (string) so the 'int(b)'
    conversion raises inside the try/except and that except path is executed.
    We expect an exception (TypeError/ValueError) to be raised eventually,
    but the goal is to exercise the except branch in the implementation.
    """
    with pytest.raises(Exception):
        Root().execute(8, "not-an-int")