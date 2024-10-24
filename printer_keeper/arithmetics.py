from dataclasses import dataclass
from random import Random


@dataclass(frozen=True)
class ArithmeticProblem:
    text: str


class ArithmeticProblemGenerator:
    def __init__(self, random_seed=None):
        self.rnd = Random(random_seed)

    def generate(self):
        def get():
            yield self._sum()
            yield self._sum()
            yield self._difference()
            yield self._difference()
            yield self._multiplication()
            yield self._multiplication()
            yield self._division()
            yield self._division()

        for _i in range(1000):
            problems = list(get())
            if len(set([p.text for p in problems])) == len(problems):
                return problems
        else:
            raise Exception(
                f"Couldn't get all problems different even after {_i + 1} attempts"
            )

    def _sum(self):
        a = self.rnd.randint(0, 30)
        b = self.rnd.randint(0, 30)
        return ArithmeticProblem(f"{a} + {b} = ")

    def _difference(self):
        while True:
            a = self.rnd.randint(0, 30)
            b = self.rnd.randint(0, 30)
            if 0 <= a - b:
                return ArithmeticProblem(f"{a} - {b} = ")

    def _multiplication(self):
        a = self.rnd.randint(3, 9)
        b = self.rnd.randint(4, 9)
        return ArithmeticProblem(f"{a} * {b} = ")

    def _division(self):
        a = self.rnd.randint(4, 9)
        b = self.rnd.randint(3, 9)
        return ArithmeticProblem(f"{a * b} / {b} = ")
