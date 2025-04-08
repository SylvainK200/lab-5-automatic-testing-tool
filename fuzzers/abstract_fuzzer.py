import abc

from common.abstract_executor import AbstractExecutor


class AbstractFuzzer(abc.ABC):
    def __init__(self, executor: AbstractExecutor):
        self.executor = executor

    @abc.abstractmethod
    def generate_input(self):
        """Generate input for fuzzing."""
        pass

    @abc.abstractmethod
    def _update(self, input):
        """Update the fuzzer with based on the result of the input evaluation.
        Results are stored in the data attribute of the fuzzer.
        """
        pass

    def run_fuzzer(self, budget=10):
        """Run the fuzzer within a time budget."""
        self.data = {
            "coverage": [],
            "inputs": [],
            "execution_times": [],
            "exceptions": 0,
        }
        #global coverage
        coverage = []

        try:
            for i in range(budget):
                input = self.generate_input()
                self.data["inputs"].append(input)
                exceptions, execution_time, coverage = self.executor._execute_input(
                    input
                )
                current_coverage = len(coverage)
                self.data["coverage"].append(current_coverage)
                self.data["execution_times"].append(execution_time)
                self.data["exceptions"] += exceptions
                self._update(input)

        except Exception as e:
            print(f"Error: {str(e)}")

        return self.data
