from pq.utils import *
from rich import print_json
import json

execution_context = {}

class Filter:
    def __init__(self, expr, producer, first=False):
        self.first = first
        self.producer = producer
        self.accumulate = False

        if len(expr) > 1 and expr[:2] == "-a":
            self.accumulate = True
            expr = expr[2:]
        
        self.expr = expr
        if not first:
            self._compiled = self._compile()

    def _compile(self):
        return compile(f"({self.expr})", "<string>", "eval")

    def evaluate(self, item):
        return eval(self._compiled, {"j": item}, execution_context)

    def eval_loop(self):
        if self.first:
            yield self.producer
        else:
            #get generator from producer
            producer_gen = self.producer.eval_loop()
            for p in producer_gen:
                # Accumulate means that this we will buffer up all the producers data into a list
                # Allows us to do max() etc.
                if self.accumulate:
                    acc = [a for a in producer_gen]
                    acc.insert(0, p)
                    p = acc

                if not p:
                    continue
                val = self.evaluate(p)
                
                if not val:
                    continue

                # Always iterate if list
                elif type(val) == list:
                    for l in val:
                        yield l
                else:
                    yield val


class Pipeline:
    """One or multiple filters connected"""

    def __init__(self, json_stream, str_input, output=True):
        str_input = str_input or ""
        self.output = output
        jsondata = json.loads(json_stream.read())

        # Array constructs around expression
        if len(str_input) and (str_input[0] == "[" and str_input[-1] == "]"):
            str_input = str_input[1:-1]
            self.array = True
        else:
            self.array = False

        pipe_filters = [s.strip() for s in str_input.split("|")]
        self.filters = self._build_pipeline(jsondata, pipe_filters)

        self._output_function = self.json_output

    @property
    def last(self):
        """Returns last filter in pipeline"""
        if len(self.filters):
            return self.filters[-1]
        else:
            raise IndexError("No filters in pipeline")

    @property
    def first(self):
        """Returns first user declared filters in pipeline"""
        if len(self.filters):
            return self.filters[1]
        else:
            raise IndexError("No filters in pipeline")

    @property
    def output_function(self):
        return self._output_function

    @output_function.setter
    def output_function(self, func):
        self._output_function = func

    def _build_pipeline(self, input_data, pipe_expression):
        """Build a pipeline from user input pipeline-string

        A pipeline consist of atleast "input | output" even if users has not defined any filters, where filters
        are between input and output.

        Example of user defined filters:
        $ pq "j[:] | j['name']"
        --->
        The right right filter consumes what the left filter j[:] yields.

        Under the hood, with input and output attached:
        (input data) | j[:] | j['name'] | -> (output)
        """
        filters = []
        for e in pipe_expression:
            if not filters:
                # input data, not a filter per se
                filters.append(Filter(e, producer=input_data, first=True))
            if e:
                filters.append(Filter(e, producer=filters[-1]))
        return filters

    def run(self):
        """Run pipeline chain with a callback for output"""
        if self.output:
            self._output_function(self.last.eval_loop())

    def json_output(self, output):
        # Buff yielded items if array filter
        if self.array:
            buff = []
            for o in output:
                buff.append(output)
        else:
            for o in output:
                try:
                    print_json(json.dumps(o))
                except:
                    print(json.dumps(o, indent=2))


def _import_custom_modules(str_or_path, from_file=False):
    """Import Python file or input string and read it to Filters execution context
    """
    if from_file:
        module_str = open(str_or_path, "r").read()
    else:
        module_str = str_or_path

    exec(module_str, execution_context)

    
