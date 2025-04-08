from fuzzers.abstract_fuzzer import AbstractFuzzer
import random
import numpy as np
from common.abstract_seed import AbstractSeed
from power_schedules.abstract_power_schedule import AbstractPowerSchedule



class MutationFuzzer(AbstractFuzzer):
    """
    # The `MutationFuzzer` class is a fuzzer that generates new inputs by mutating existing seeds using
    # various mutation techniques.
    A fuzzer that mutates the seed to generate new inputs.
    #https://www.fuzzingbook.org/html/MutationFuzzer.html
    """

    def __init__(
        self,
        executor,
        seeds: list[AbstractSeed],
        power_schedule: AbstractPowerSchedule = None,
        character_list: list = None,
        min_mutations: int = 1,
        max_mutations: int = 10,

    ):
        super().__init__(executor)
        self.seeds = seeds
        self.character_list = character_list
        self.seed_index = 0
        self.executor = executor
        self.power_schedule = power_schedule
        self.min_mutations = min_mutations
        self.max_mutations = max_mutations
        self.mutators = [ self._replace_random_character, self._insert_random_character]

    def generate_input(self):

        """Mutate the seed to generate input for fuzzing.
        With this function we first use the gien seeds to generate inputs 
        and then we mutate the seeds to generate new inputs."""
        if self.seed_index < len(self.seeds):
            # Still seeding
            inp = self.seeds[self.seed_index].data
            self.seed_index += 1
        else:
            # Mutating
            inp = self._create_candidate()

        return inp

    def _update(self, input):
        """Update the fuzzer with the input and its coverage."""
        if len(self.data["coverage"]) > 1:
            if self.data["coverage"][-1] > self.data["coverage"][-2]:
                self.seeds.append(AbstractSeed(input))

    def _create_candidate(self):
        seed = np.random.choice(self.seeds)

        # Stacking: Apply multiple mutations to generate the candidate
        if self.power_schedule:
            candidate = self.power_schedule.choose(self.seeds).data
        else:
            candidate = seed.data
        # Apply power schedule to generate the candidate
        #
        trials = random.randint(self.min_mutations, self.max_mutations)
        for i in range(trials):
            candidate = self.mutate(candidate)
        return candidate

    def mutate(self, s):
        """Return s with a random mutation applied"""
        mutator = random.choice(self.mutators)
        return mutator(s)

    def _delete_random_character(self, s):
        """Returns s with a random character deleted"""
        if len(s) > 5:
            pos = random.randint(0, len(s) - 1)
            return s[:pos] + s[pos + 1 :]
        else:
            return s

    def _insert_random_character(self, s):
        """Returns s with a random character inserted"""
        pos = random.randint(0, len(s))
        random_character = random.choice(self.character_list)
        return s[:pos] + random_character + s[pos:]

    def _replace_random_character(self, s):
        """Returns s with a random character replaced"""
        if s == "":
            return ""
        pos = random.randint(0, len(s) - 1)
        random_character = random.choice(self.character_list)
        return s[:pos] + random_character + s[pos + 1 :]
