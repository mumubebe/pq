import logging
from pq.utils import odig
from rich import print_json
import sys, json


class Expression:
    def __init__(self, expr, producer, first=False):
        self.first = first
        self.producer = producer
        self.expr = expr
        if not first:
            self._compiled = self._compile()

    def _compile(self):
        return compile(f"({self.expr})", "<string>", "eval")

    def evaluate(self, row):
        return eval(self._compiled, {"j": row, "odig": odig})

    def eval_loop(self):
        if self.first:
            yield self.producer
        else:
            for p in self.producer.eval_loop():
                if not p:
                    continue
                val = self.evaluate(p)

                if not val:
                    continue
                elif type(val) == list:
                    for l in val:
                        yield l
                else:
                    yield val


class Pipeline:
    """One or multiple expressions connected"""

    def __init__(self, jsondata, str_input):
        str_input = str_input or ""
        
        if len(str_input) and (str_input[0] == "[" and str_input[-1] == "]"):
            str_input = str_input[1:-1]
            self.array = True
        else:
            self.array = False

        pipe_expressions = [s.strip() for s in str_input.split("|")]

        self.exprs = self._build_pipeline(jsondata, pipe_expressions)

    @property
    def last(self):
        """Returns last expression in pipeline"""
        if len(self.exprs):
            return self.exprs[-1]
        else:
            raise IndexError("No expressions in pipeline")

    @property
    def first(self):
        """Returns first user declared expression in pipeline"""
        if len(self.exprs):
            return self.exprs[1]
        else:
            raise IndexError("No expressions in pipeline")

    def _build_pipeline(self, input_data, pipe_expression):
        """Build a pipeline from user input pipeline-string

        Example:
        $ pq "j[:] | j['name']"
        --->
        The left right expression consumes a generator produces by the expression j[:].
        """
        exprs = []
        for e in pipe_expression:
            if not exprs:
                exprs.append(Expression(e, producer=input_data, first=True))

            if e:
                exprs.append(Expression(e, producer=exprs[-1]))
        return exprs

    def run(self):
        """Run pipeline chain and print ouput"""

        # Buff yielded items if array expression
        if self.array:
            buff = []
            for output in self.last.eval_loop():
                buff.append(output)

            self.print(buff)
        else:
            for output in self.last.eval_loop():
                self.print(output)

    def print(self, output):
        if type(output) == dict or type(output) == list:
            print_json(json.dumps(output))
        else:
            print(json.dumps(output, indent=2))
