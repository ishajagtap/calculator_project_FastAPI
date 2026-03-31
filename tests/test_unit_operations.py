"""Unit tests for app/operations.py — covers every operation class and the factory."""
import math
import pytest

from app.operations import (
    OperationFactory, Add, Sub, Mul, Div, Pow, Root,
    Modulus, IntDivide, Percent, AbsDiff,
)
from app.exceptions import DivisionByZeroError, OperationError


# ── OperationFactory ───────────────────────────────────────────────────────────

class TestOperationFactory:
    def test_create_add(self):
        op = OperationFactory.create("add")
        assert isinstance(op, Add)

    def test_create_alias_plus(self):
        op = OperationFactory.create("+")
        assert isinstance(op, Add)

    def test_create_case_insensitive(self):
        op = OperationFactory.create("ADD")
        assert isinstance(op, Add)

    def test_create_unknown_raises(self):
        with pytest.raises(OperationError):
            OperationFactory.create("unknown_op")

    def test_generate_help_contains_commands(self):
        help_text = OperationFactory.generate_help()
        assert "add" in help_text
        assert "div" in help_text
        assert "history" in help_text


# ── Add ───────────────────────────────────────────────────────────────────────

class TestAdd:
    def test_positive(self):
        assert Add().execute(3, 4) == 7

    def test_negative(self):
        assert Add().execute(-1, -2) == -3

    def test_floats(self):
        assert Add().execute(1.5, 2.5) == 4.0

    def test_zero(self):
        assert Add().execute(0, 0) == 0


# ── Sub ───────────────────────────────────────────────────────────────────────

class TestSub:
    def test_positive(self):
        assert Sub().execute(10, 3) == 7

    def test_negative_result(self):
        assert Sub().execute(3, 10) == -7

    def test_floats(self):
        assert Sub().execute(5.5, 2.5) == 3.0

    def test_zero(self):
        assert Sub().execute(0, 0) == 0


# ── Mul ───────────────────────────────────────────────────────────────────────

class TestMul:
    def test_positive(self):
        assert Mul().execute(3, 4) == 12

    def test_by_zero(self):
        assert Mul().execute(100, 0) == 0

    def test_negative(self):
        assert Mul().execute(-3, 4) == -12

    def test_floats(self):
        assert abs(Mul().execute(2.5, 4.0) - 10.0) < 1e-9


# ── Div ───────────────────────────────────────────────────────────────────────

class TestDiv:
    def test_positive(self):
        assert Div().execute(10, 2) == 5.0

    def test_fractional(self):
        assert abs(Div().execute(1, 3) - 1 / 3) < 1e-9

    def test_negative(self):
        assert Div().execute(-9, 3) == -3.0

    def test_by_zero_raises(self):
        with pytest.raises(DivisionByZeroError):
            Div().execute(5, 0)


# ── Pow ───────────────────────────────────────────────────────────────────────

class TestPow:
    def test_square(self):
        assert Pow().execute(4, 2) == 16

    def test_zero_exponent(self):
        assert Pow().execute(5, 0) == 1

    def test_negative_base(self):
        assert Pow().execute(-2, 3) == -8

    def test_fractional_exponent(self):
        assert abs(Pow().execute(8, 1 / 3) - 2.0) < 1e-9


# ── Root ──────────────────────────────────────────────────────────────────────

class TestRoot:
    def test_square_root(self):
        assert abs(Root().execute(9, 2) - 3.0) < 1e-9

    def test_cube_root(self):
        assert abs(Root().execute(27, 3) - 3.0) < 1e-9

    def test_negative_odd_root(self):
        result = Root().execute(-27, 3)
        assert abs(result - (-3.0)) < 1e-9

    def test_negative_even_root_raises(self):
        with pytest.raises(OperationError):
            Root().execute(-4, 2)

    def test_zero_degree_raises(self):
        with pytest.raises(OperationError):
            Root().execute(8, 0)


# ── Modulus ───────────────────────────────────────────────────────────────────

class TestModulus:
    def test_basic(self):
        assert Modulus().execute(10, 3) == 1

    def test_exact_division(self):
        assert Modulus().execute(9, 3) == 0

    def test_by_zero_raises(self):
        with pytest.raises(DivisionByZeroError):
            Modulus().execute(10, 0)


# ── IntDivide ─────────────────────────────────────────────────────────────────

class TestIntDivide:
    def test_basic(self):
        assert IntDivide().execute(10, 3) == 3

    def test_negative(self):
        # math.trunc(-10/3) == -3
        assert IntDivide().execute(-10, 3) == -3

    def test_by_zero_raises(self):
        with pytest.raises(DivisionByZeroError):
            IntDivide().execute(10, 0)


# ── Percent ───────────────────────────────────────────────────────────────────

class TestPercent:
    def test_basic(self):
        assert Percent().execute(50, 200) == 25.0

    def test_hundred_percent(self):
        assert Percent().execute(5, 5) == 100.0

    def test_by_zero_raises(self):
        with pytest.raises(DivisionByZeroError):
            Percent().execute(50, 0)


# ── AbsDiff ───────────────────────────────────────────────────────────────────

class TestAbsDiff:
    def test_positive_order(self):
        assert AbsDiff().execute(10, 3) == 7

    def test_reverse_order(self):
        assert AbsDiff().execute(3, 10) == 7

    def test_equal(self):
        assert AbsDiff().execute(5, 5) == 0

    def test_negative_inputs(self):
        assert AbsDiff().execute(-3, -7) == 4
