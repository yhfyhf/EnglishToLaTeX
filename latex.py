# encoding: utf-8
from utils import Utils
from table import table


class EnglishToLatex(object):
    def preprocess(self, input):
        """
        :param input: String
        :return: void
        """
        preprocessed = filter(lambda x: bool(x), map(self.preprocessTerminator, input.lower().split()))
        ret = self.combineNumbers(preprocessed)
        return " ".join(ret)

    def preprocessTerminator(self, word):
        """
        remove trailing '.' and ','
        """
        if word[-1] in (",", "."):
            word = word[0:-1]
        return table.get(word, word)

    def combineNumbers(self, preprocessed):
        """
        combine separate numbers into one
        :param preprocessed: "1 2 . 34 . , 5 + 6 + 8 , 9"
        :return: "12345 + 6 + 89"
        """
        ret = []
        i = 0
        while i < len(preprocessed):
            if not Utils.is_float(preprocessed[i]):
                ret.append(preprocessed[i])
            else:
                temp = preprocessed[i]
                i += 1
                while i < len(preprocessed) and Utils.is_float(preprocessed[i]):
                    temp += preprocessed[i]
                    i += 1
                i -= 1
                ret.append(temp)
            i += 1
        return ret

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
        preprocessed_input = self.preprocess(input)
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
            elif self.is_times(tokens[i].val):
                res.append(Token("\\times", False))
            elif self.is_plus(tokens[i].val):
                res.append(Token("+", False))
            elif self.is_minus(tokens[i].val):
                res.append(Token("-", False))
            else:
                res.append(tokens[i])
            i += 1

        return Token(" ".join(map(lambda x: x.val, res)), True)

    def to_frac(self, dividend, divisor):
        # val = "\\frac{\{\}}{\{\}}".format(dividend.val, divisor.val)
        val = "\\frac{" + dividend.val + "}{" + divisor.val + "}"
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


class Token(object):
    def __init__(self, val, atomic):
        self.val = val
        self.atomic = atomic


if __name__ == '__main__':
    s = EnglishToLatex()

    assert s.preprocess("1 2 . 34 . , 5 + 6 + 8 , 9") == "12345 + 6 + 89"

    assert s.to_latex("1 plus 2") == "1 + 2"
    assert s.to_latex("124 + 4 * 5") == "124 + 4 \\times 5"
    assert s.to_latex("1 + 2 * 3, - 4 divided by 5.") == "1 + 2 \\times 3 - \\frac{4}{5}"
    assert s.to_latex("3 times left 2 + 4 right.") == "3 \\times (2 + 4)"
    assert s.to_latex(
        "2 times left left 3 + 2. Right. Divided by left 2 minus. 1. right right") == "2 \times (\frac{(3 + 2)}{(2 - 1)})"
    assert s.to_latex(
        "2 times left left 3 + 2. Right. Divided by left 2 minus. 1. right right") == "2 \\times (\\frac{(3 + 2)}{(2 - 1)})"
