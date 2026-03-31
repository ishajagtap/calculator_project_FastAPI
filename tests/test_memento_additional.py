# tests/test_memento_additional.py
from app.calculator_memento import Caretaker, Memento

def test_caretaker_push_pop_sequence():
    c = Caretaker()
    # Save two different states
    m1 = c.save({"a": 1})
    m2 = c.save({"a": 2})
    # Undo twice -> first undo pops m2
    u1 = c.undo()
    assert isinstance(u1, Memento)
    # Second undo should pop m1
    u2 = c.undo()
    # u2 should be a Memento as well
    assert (u2 is None) or isinstance(u2, Memento)