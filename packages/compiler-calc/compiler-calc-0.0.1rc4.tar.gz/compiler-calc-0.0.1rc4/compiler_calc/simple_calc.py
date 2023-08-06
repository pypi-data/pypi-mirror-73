#!/usr/bin/env python

"""This programmes calculate expressions like "3 + 4 * 5".
The following operators are supported: +, -, *, /, ^, (, ).
The following types are supported: float, int

VAL = 0|1|2|3|4|5|6|7|8|9|0|.   # support integer and float
OP = +|-|*|/|^                  # ^ is pow function
EXPR = VAL|EXPR OP EXPR|(EXPR)|-EXPR
"""

import os
import re
import numbers
import traceback
from typing import Union


__author__ = "Bo HAN"
__license__ = "MIT"
__version__ = "0.0.1rc4"
__email__ = "bohan.academic@gmail.com"


# operators and their priority
OP_DICT = {
    '+': 1,
    '-': 1,
    '*': 2,
    '/': 2,
    '^': 3   # pow func
}
# brackets have highest priorities
LEFT_BRACKET = "("
RIGHT_BRACKET = ")"


class LexAnalysis:
    """Perform lexical analysis of an input
    """
    WS = re.compile(r'\s+')
    NUM_SET = set(c for c in '0123456789.')

    def _remove_ws(self, expr: str) -> str:
        """Remove whitespaces from the input expression
        :param expr:  input expression string
        :return: a string without whitespaces
        """
        expr = re.sub(LexAnalysis.WS, '', expr)
        assert expr, f"Empty input after whitespace removal {expr}"
        return expr

    @staticmethod
    def make_val(val: list) -> Union[float, int]:
        val = "".join(val)
        val = float(val) if "." in val else int(val)
        return val

    def _analyse(self, expr: str) -> list:
        """Generate a list of lexical terms (numeric values or operators)
        :param expr: input expression string (without whitespaces)
        :return: a list of lexical terms
        """
        expr_list = []
        val = []
        for i, c in enumerate(expr):
            if c in LexAnalysis.NUM_SET:
                val.append(c)
            elif c in OP_DICT or c in (LEFT_BRACKET, RIGHT_BRACKET):
                if val:
                    expr_list.append(LexAnalysis.make_val(val))
                    val.clear()
                expr_list.append(c)
            else:
                raise ValueError(f"Invalid expr character: {c} found at {i} in {expr}")
        if val:
            expr_list.append(LexAnalysis.make_val(val))
        return expr_list

    def _audit_expr_list(self, expr_list: list) -> None:
        for i in range(len(expr_list) - 1):
            cur, next_ = expr_list[i], expr_list[i + 1]
            if isinstance(cur, numbers.Number) and isinstance(next_, numbers.Number):
                raise ValueError(f"Invalid consecutive value {cur} {next_}")
            elif cur in OP_DICT and next_ in OP_DICT:
                raise ValueError(f"Invalid consecutive operators {cur} {next_}")
            else:
                pass
        if expr_list[-1] in OP_DICT:
            raise ValueError("Last item cannot be an operator")
        if expr_list[0] in OP_DICT and expr_list[0] != "-":
            raise ValueError("First item cannot be an operator other than '-'")

    def __call__(self, expr: str) -> list:
        expr = self._remove_ws(expr)
        expr_list = self._analyse(expr)
        self._audit_expr_list(expr_list)
        return expr_list


enable_context = os.environ.get("enable_context", True)


class SyntaxAnalysis:
    """Syntax analysis to perform calculations
    """
    def _simple_calculate(self, var1: float, op: str, var2: float) -> float:
        """Simple compiler_calc for two numeric values and one operator
        :param var1: value 1
        :param op: operator
        :param var2: value 2
        :return: value1 op value2
        """
        if op == "+":
            return var1 + var2
        elif op == "-":
            return var1 - var2
        elif op == "*":
            return var1 * var2
        elif op == "/":
            if var2:
                return var1 / var2
            else:
                raise ValueError(f"Divisor cannot be zero: {var2}")
        elif op == "^":
            return pow(var1, var2)
        else:
            raise ValueError("Operator is invalid")

    def _calculate(self, expr_list: list) -> float:
        """Syntax analysis
        :param expr_list: a list of terms to be calculated
        :return: the calculation result
        """
        if LEFT_BRACKET in expr_list:
            # solve nested expressions in brackets by recursion
            expr_buf = []
            pos, max_len = 0, len(expr_list)
            while pos < max_len:
                var = expr_list[pos]
                if var in OP_DICT:
                    expr_buf.append(var)
                    pos += 1
                elif isinstance(var, numbers.Number):
                    expr_buf.append(var)
                    pos += 1
                elif var == LEFT_BRACKET:
                    offset = pos
                    lb, rb = 0, 0
                    while offset < max_len:
                        subvar = expr_list[offset]
                        if subvar == LEFT_BRACKET:
                            lb += 1
                        elif subvar == RIGHT_BRACKET:
                            rb += 1
                        else:
                            pass
                        offset += 1
                        if lb == rb:
                            break
                    if lb != rb:
                        raise ValueError(f"Unmatched brats in {expr_list[offset:]}")
                    expr_buf.append(self._calculate(expr_list[pos + 1: offset - 1]))
                    pos = offset
                else:
                    raise ValueError(f"Error {expr_list[pos]}")
            expr_list = expr_buf
        # Deal with first negative number
        assert len(expr_list) >= 1, f"Incorrect length of expressions: {expr_list}"
        if expr_list[0] == "-" and isinstance(expr_list[1], numbers.Number):
            expr_list = [-expr_list[1]] + expr_list[2:]
        # val1 op1 val2 op2 val3 op3 val4 ...
        vars_, ops, priority_set = [], [], set()
        for i, term in enumerate(expr_list):
            if isinstance(term, numbers.Number):
                vars_.append(term)
            elif term in OP_DICT:
                ops.append(term)
                priority_set.add(OP_DICT[term])
            else:
                raise ValueError(f"Incorrect reduced sequence {expr_list}")
        assert len(ops) + 1 == len(vars_), f"OPS: {len(ops)} vs Variables: {len(vars_)}"
        # reduce from highest to the lower priority calculation from left to right
        # each reduce calculation will consume two vars and one op.
        priority_list = sorted([p for p in priority_set], reverse=True)
        for priority in priority_list:
            pos = 0
            while ops and pos < len(ops):
                op = ops[pos]
                if OP_DICT[op] == priority:
                    reduced_result = self._simple_calculate(vars_[pos], op, vars_[pos + 1])
                    # TODO: performance overhead
                    vars_ = vars_[:pos] + [reduced_result] + vars_[pos + 2:]
                    ops = ops[:pos] + ops[pos + 1:]
                else:
                    pos += 1
        assert len(ops) + 1 == len(vars_), f"OPS: {len(ops)} vs Variables: {len(vars_)}"
        return vars_[0]

    def __call__(self, expr_list: list) -> Union[int, float]:
        try:
            result = self._calculate(expr_list)
        except (AssertionError, ValueError) as e:
            print(f"Calculation error caused by {e.args}")
            raise
        except Exception as e:
            tb_str = "\n".join(traceback.format_tb(e.__traceback__))
            print(f"Unknown error: {e.args}\n{tb_str}")
            raise
        else:
            return result


_lex_analyser = LexAnalysis()
_syntax_analyser = SyntaxAnalysis()


def calculate(expr: str, lex: LexAnalysis = _lex_analyser, syn: SyntaxAnalysis = _syntax_analyser) -> Union[float, int]:
    expr_list = lex(expr)
    result = syn(expr_list)
    return result


def main():
    while True:
        input_data = input("Please enter your expression to calculate (q to exit):\n>>> ")
        if input_data == "q":
            print("See you")
            break
        else:
            result = calculate(input_data)
            print(f"\n>>> '{input_data}' calculation result is '{result}'")


if __name__ == "__main__":
    main()
