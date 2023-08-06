from random import choice


class Die:
    """parent class for all dice types"""
    _values = None

    @property
    def roll(self):
        return choice(self._values)


class HighVarianceD4(Die):
    _values = [1, 1, 4, 4]


class HighVarianceD6(Die):
    _values = [1, 1, 2, 5, 6, 6]


class HighVarianceD8(Die):
    _values = [1, 1, 2, 3, 6, 7, 8, 8]


class HighVarianceD10(Die):
    _values = [1, 1, 2, 2, 3, 8, 9, 9, 10, 10]


class HighVarianceD100(Die):
    _values = [i*10 for i in [1, 1, 2, 2, 3, 8, 9, 9, 10, 10]]


class HighVarianceD12(Die):
    _values = [1, 1, 2, 2, 3, 4, 9, 10, 11, 11, 12, 12]


class HighVarianceD20(Die):
    _values = [1, 1, 1, 2, 2, 3, 3, 4, 5, 6, 15, 16, 17, 18, 18, 19, 19, 20, 20, 20]
