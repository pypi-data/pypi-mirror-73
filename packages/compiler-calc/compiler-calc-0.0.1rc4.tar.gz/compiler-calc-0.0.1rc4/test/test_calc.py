from unittest import TestCase
from compiler_calc.simple_calc import SyntaxAnalysis, LexAnalysis


class BasicOperations(TestCase):
    def setUp(self) -> None:
        self.lex_analyser = LexAnalysis()
        self.syntax_analyser = SyntaxAnalysis()

    def calculate(self, expr):
        expr_list = self.lex_analyser(expr)
        return self.syntax_analyser(expr_list)

    def test_two_pos_add(self):
        assert self.calculate("1+1") == 2

    def test_three_pos_add(self):
        assert self.calculate("1+1+1") == 3

    def test_two_neg_add(self):
        assert self.calculate("-1+(-1)") == -2

    def test_three_neg_add(self):
        assert self.calculate("-1+(-1)+(-1)") == -3

    def test_one_pos_one_neg(self):
        assert self.calculate("1-1") == 0

    def test_one_pos_one_neg(self):
        assert self.calculate("-1+1") == 0

    def test_two_sub(self):
        assert self.calculate("2-1") == 1

    def test_three_sub(self):
        assert self.calculate("2-1-1") == 0

    def test_two_pos_mul(self):
        assert self.calculate("2*3") == 6

    def test_three_pos_mul(self):
        assert self.calculate("2*3*4") == 24

    def test_two_neg_mul(self):
        assert self.calculate("(-2)*(-3)") == 6

    def test_three_neg_mul(self):
        assert self.calculate("(-2)*(-3)*(-4)") == -24

    def test_three_mix_mul(self):
        assert self.calculate("(-2)*3*(-4)") == 24

    def test_three_zero_mul(self):
        assert self.calculate("(-2)*3*(-4)*1*0") == 0

    def test_two_pos_div(self):
        assert self.calculate("4/2") == 2

    def test_three_pos_div(self):
        assert self.calculate("4/2/2") == 1

    def test_two_neg_div(self):
        assert self.calculate("4/(-2)") == -2

    def test_three_pos_div(self):
        assert self.calculate("4/(-2)/2") == -1

    def test_zero_division(self):
        with self.assertRaises(ValueError):
            self.calculate("4/0")

    def test_high_order_operators_mid(self):
        assert self.calculate("1+2*3*4-1") == 24

    def test_high_order_operators_beg(self):
        assert self.calculate("2*3*4-1+1") == 24

    def test_high_order_operators_end(self):
        assert self.calculate("-1+1+2*3*4") == 24

    def test_high_order_operators_middle_complex(self):
        assert self.calculate("1 + 2^3^2 - 3*2*10 - 4") == 1

    def test_lo_mi_hi(self):
        assert self.calculate("1+2*3^2") == 19

    def test_lo_hi_mi(self):
        assert self.calculate("1+2^3*2") == 17

    def test_mi_lo_hi(self):
        assert self.calculate("1*2+3^2") == 11

    def test_mi_hi_lo(self):
        assert self.calculate("1*2^3+2") == 10

    def test_hi_lo_mi(self):
        assert self.calculate("2^2+3*2") == 10

    def test_hi_mi_lo(self):
        assert self.calculate("2^2*3+2") == 14

    def test_single_pos(self):
        assert self.calculate("2") == 2

    def test_single_neg(self):
        assert self.calculate("-2") == -2

    def test_manual1(self):
        assert self.calculate("-1 + ((2*3)-6+(2)-(-1)) + 2^3/8 - 3") == 0

    def test_manual2(self):
        assert self.calculate("1+2*(9-3/(8-5))+4") == 21

    def test_leecode(self):
        assert self.calculate("2-((5-6)*(2-3))") == 1

    def test_float(self):
        assert str(self.calculate("4 + 2 * 5 - 7 / 11"))[:5] == "13.36"

    def test_error_ops(self):
        with self.assertRaises(ValueError):
            self.calculate("4 + + 2")

    def test_error_unmatched_brackets(self):
        with self.assertRaises(ValueError):
            self.calculate("1 + (2")
        with self.assertRaises(ValueError):
            self.calculate("1 + ((2)")
        with self.assertRaises(ValueError):
            self.calculate("1 + ((2)))")
        with self.assertRaises(ValueError):
            self.calculate("1 + )(2")

    def test_error_beg(self):
        with self.assertRaises(ValueError):
            self.calculate("*1+2")

    def test_error_end(self):
        with self.assertRaises(ValueError):
            self.calculate("1+2-")

    def test_error_ops(self):
        with self.assertRaises(ValueError):
            self.calculate("1#2")
