import string
import random
from poly_fuzzer.fuzzers.abstract_fuzzer import AbstractFuzzer



class RandomFuzzer(AbstractFuzzer):
    '''
    A random fuzzer that generates random strings of a specified length.'''
    def __init__(self, executor, min_length=90, max_length=100):
        super().__init__(executor)
        self.min_length = min_length
        self.max_length = max_length

    def _update(self, input):
        pass

    def generate_random_string(self, length):
        """Generate a random string of specified length."""
        letters = string.ascii_letters + string.digits + string.punctuation
        return "".join(random.choice(letters) for _ in range(length))

    def generate_input(self):
        return self.generate_random_string(
            random.randint(self.min_length, self.max_length)
        )
