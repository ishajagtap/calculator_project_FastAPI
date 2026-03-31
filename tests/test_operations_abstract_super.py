# tests/test_operations_abstract_super.py
import pytest
from app.operations import Operation

def test_operation_execute_not_implemented_via_super():
    # create a concrete subclass that calls super().execute to trigger NotImplementedError
    class Dummy(Operation):
        def execute(self, a, b):
            # intentionally call the base implementation (should raise NotImplementedError)
            return super().execute(a, b)
    d = Dummy()
    with pytest.raises(NotImplementedError):
        d.execute(1, 2)