from table import replace_table, table
from utils import Utils


class Preprocess(object):

    @staticmethod
    def preprocess(input_):
        """
        :param input_: String
        :return: void
        """
        for p, r in replace_table:
            input_ = input_.replace(p, r)
        preprocessed = []
        num_left = 0
        for word in input_.lower().split():
            word = Preprocess.preprocessTerminator(word)
            if word == "left":
                num_left += 1
            elif word == "right":
                num_left -= 1
            if word:
                preprocessed.append(word)
        ret = Preprocess.combineNumbers(preprocessed)
        while num_left > 0:
            ret.append("right")
            num_left -= 1
        return " ".join(ret)

    @staticmethod
    def preprocessTerminator(word):
        """
        remove trailing '.' and ','
        """
        if word[-1] in (",", "."):
            word = word[0:-1]
        return table.get(word, word)

    @staticmethod
    def combineNumbers(preprocessed):
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


if __name__ == '__main__':
    assert Preprocess.preprocess("x square") == "x ^ 2"
    assert Preprocess.preprocess("(x + 1) square") == "(x + 1) ^ 2"
    assert Preprocess.preprocess("x power of 3") == "x ^ 3"
    assert Preprocess.preprocess("x to power of 3") == "x ^ 3"
    assert Preprocess.preprocess("x to the power of 3") == "x ^ 3"

    assert Preprocess.preprocess("square root of x") == "2 root x"
    assert Preprocess.preprocess("square root of x + 1") == "2 root x + 1"
    assert Preprocess.preprocess("square root of (x + 1)") == "2 root (x + 1)"
    assert Preprocess.preprocess("cube root of x") == "3 root x"
    assert Preprocess.preprocess("cube root of x + 1") == "3 root x + 1"
    assert Preprocess.preprocess("seventh root of x") == "7 root x"
    assert Preprocess.preprocess("seven root of x") == "7 root x"
    assert Preprocess.preprocess("seven root x") == "7 root x"

    assert Preprocess.preprocess("1 2 . 34 . , 5 + 6 + 8 , 9") == "12345 + 6 + 89"
