# encoding: utf-8
from preprocess import Preprocess


class EnglishToLatex(object):
    def createAllTokens(self, input):
        tokens = []

        for elem in input.split():
            if self.is_left(elem) or \
                    self.is_right(elem) or \
                    self.is_plus(elem) or \
                    self.is_minus(elem) or \
                    self.is_times(elem) or \
                    self.is_divide(elem):
                tokens.append(Token(elem, False))
            elif len(elem) > 0:
                tokens.append(Token(elem, True))
        return tokens

    def to_latex(self, input):
        preprocessed_input = Preprocess.preprocess(input)
        tokens = self.createAllTokens(preprocessed_input)

        stack = []
        # handle parenthesis.
        for token in tokens:
            if self.is_right(token.val):
                to_eval = []
                while not self.is_left(stack[-1].val):
                    to_eval.insert(0, stack.pop())
                stack.pop()
                res = self.eval(to_eval)
                res.val = "(" + res.val + ")"
                stack.append(res)
            else:
                stack.append(token)

        to_eval = []
        while stack:
            to_eval.insert(0, stack.pop())
        res = self.eval(to_eval)
        return res.val

    def eval(self, tokens):
        res = []
        i = 0
        while i < len(tokens):
            if self.is_divide(tokens[i].val):
                dividend = res.pop()
                i += 1
                divisor = tokens[i]
                res.append(self.to_frac(dividend, divisor))
            elif self.is_root(tokens[i].val):
                nth = res.pop()
                i += 1
                value = tokens[i]
                res.append(self.to_root(nth, value))
            elif self.is_times(tokens[i].val):
                res.append(Token("\\times", False))
            elif self.is_plus(tokens[i].val):
                res.append(Token("+", False))
            elif self.is_minus(tokens[i].val):
                res.append(Token("-", False))
            else:
                res.append(tokens[i])
            i += 1

        tokens = res
        res = []
        i = 0
        while i < len(tokens):
            if i < len(tokens) - 1 and self.is_power(tokens[i].val):
                res.append(tokens[i])
                i += 1
                next_token = tokens[i]
                next_token.val = "{" + next_token.val + "}"
                res.append(next_token)
            else:
                res.append(tokens[i])
            i += 1

        return Token(" ".join(map(lambda x: x.val, res)), True)

    def to_frac(self, dividend, divisor):
        val = "\\frac{" + dividend.val + "}{" + divisor.val + "}"
        return Token(val, True)

    def to_root(self, nth, value):
        val = "\\sqrt[" + nth.val + "]{" + value.val + "}"
        return Token(val, True)

    def is_left(self, elem):
        return elem.lower() == "left"

    def is_right(self, elem):
        return elem.lower() == "right"

    def is_plus(self, elem):
        return elem.lower() == "+"

    def is_minus(self, elem):
        return elem.lower() == "-"

    def is_times(self, elem):
        return elem.lower() == "*"

    def is_divide(self, elem):
        return elem.lower() == "/"

    def is_root(self, elem):
        return elem.lower() == "root"

    def is_power(self, elem):
        return elem == "^"


class Token(object):
    def __init__(self, val, atomic):
        self.val = val
        self.atomic = atomic


if __name__ == '__main__':
    s = EnglishToLatex()

    assert s.to_latex("1 plus 2") == "1 + 2"
    assert s.to_latex("124 + 4 * 5") == "124 + 4 \\times 5"
    assert s.to_latex("1 + 2 * 3, - 4 divided by 5.") == "1 + 2 \\times 3 - \\frac{4}{5}"
    assert s.to_latex("3 times left 2 + 4 right.") == "3 \\times (2 + 4)"
    assert s.to_latex(
        "2 times left left 3 + 2. Right. Divided by left 2 minus. 1. right right") == "2 \\times (\\frac{(3 + 2)}{(2 - 1)})"
    assert s.to_latex("2 plus 3 divided by left 2 - 1") == "2 + \\frac{3}{(2 - 1)}"  # add missing right parentheses

    assert s.to_latex("2 to the power of 3 divided by left 2 - 1") == "2 ^ {\\frac{3}{(2 - 1)}}"

    assert s.to_latex("2 root of 3") == "\sqrt[2]{3}"
    assert s.to_latex("2 to power left Ninth root of x ") == "2 ^ {(\sqrt[9]{x})}"

    assert s.to_latex("3 to the power of left b divided by c") == "3 ^ {(\\frac{b}{c})}"

    assert s.to_latex("3 to the power of left b divided by c right") == "3 ^ {(\\frac{b}{c})}"
