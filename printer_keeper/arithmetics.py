from dataclasses import dataclass
from random import Random
from typing import List


@dataclass(frozen=True)
class ArithmeticProblem:
    text: str


class ArithmeticProblemGenerator:
    def __init__(self, random_seed=None):
        self.rnd = Random(random_seed)

    def generate(self):
        yield self._sum()
        yield self._sum()
        yield self._difference()
        yield self._difference()
        yield self._multiplication()
        yield self._multiplication()
        yield self._division()
        yield self._division()

    def _sum(self):
        a = self.rnd.randint(8, 20)
        b = self.rnd.randint(5, 40)
        return ArithmeticProblem(f"{a} + {b} = ")

    def _difference(self):
        while True:
            a = self.rnd.randint(8, 40)
            b = self.rnd.randint(5, 30)
            if a - b >= 1:
                return ArithmeticProblem(f"{a} - {b} = ")

    def _multiplication(self):
        while True:
            a = self.rnd.randint(3, 9)
            b = self.rnd.randint(4, 9)
            return ArithmeticProblem(f"{a} * {b} = ")

    def _division(self):
        while True:
            a = self.rnd.randint(4, 9)
            b = self.rnd.randint(3, 9)
            return ArithmeticProblem(f"{a * b} / {b} = ")
