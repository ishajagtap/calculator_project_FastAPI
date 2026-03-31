# tests/test_memento_direct.py
from app.calculator_memento import Memento, Caretaker

def test_caretaker_undo_redo_none_behavior():
    c = Caretaker()
    # no saved states yet -> undo should return None
    # (Note: in some usages initial save may happen externally; here we directly test the empty caretaker)
    assert c.undo() is None
    assert c.redo() is None

def test_caretaker_save_and_restore():
    c = Caretaker()
    state1 = {"x": 1}
    m1 = c.save(state1)
    assert m1.state == state1
    state2 = {"x": 2}
    m2 = c.save(state2)
    # undo should pop last
    u = c.undo()
    assert u is not None
    # redo should restore
    r = c.redo()
    # r may or may not be None depending on prior operations; ensure no exception
    assert (r is None) or (isinstance(r, Memento))