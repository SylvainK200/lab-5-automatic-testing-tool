import inspect
import time
import sys
from coverage import Coverage
import json
import time


class AbstractExecutor:
    '''
    The `AbstractExecutor` class is a Python class that provides functionality for executing a program
    module and tracking code coverage.
    '''

    def __init__(self, program_module):
        self.program_module = program_module
        self.execution_data = {}
        self._lines, _ = inspect.getsourcelines(program_module)
        self._eval_num = 0
        self.eval_budget = 100

    def _execute_input(self, input=None, input_list=None):
        exceptions = 0
        coverage_data = {}

        try:
            cov = Coverage(branch=True)
            # time.sleep(2)
            cov.start()
            # .. call your code ..
            start_time = time.time()
            if input is None and input_list is None:
                self.program_module()
            elif input_list is not None:
                for input in input_list:
                    self.program_module(input)
                self._eval_num = min(len(input_list), self.eval_budget)
            else:
                self.program_module(input)

            end_time = time.time()
            cov.stop()
            cov.json_report()
            with open("coverage.json", "r") as f:
                f = json.load(f)
            coverage_data = f["totals"]
            execution_time = end_time - start_time
        except AssertionError as e:
            # print(f"AssertionError: {e}")
            end_time = time.time()
            cov.stop()
            cov.json_report()
            with open("coverage.json", "r") as f:
                f = json.load(f)
            coverage_data = f["totals"]
            execution_time = end_time - start_time
        except Exception as e:
            # print(f"Exception: {e}")
            exceptions += 1
            end_time = time.time()
            execution_time = end_time - start_time

        self._eval_num += 1

        self.execution_data = {"input": input, "exceptions": exceptions, "execution_time": execution_time,
                               "coverage": coverage_data}

        if self._eval_num > self.eval_budget:
            raise Exception("Evaluation budget exceeded.")

        return self.execution_data