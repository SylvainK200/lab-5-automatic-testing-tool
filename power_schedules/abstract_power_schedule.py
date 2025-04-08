import abc
from common.abstract_seed import AbstractSeed
import random


class AbstractPowerSchedule:
    """Define how fuzzing time should be distributed across the population.
    Implementation partly borrowed from https://www.fuzzingbook.org/html/GreyboxFuzzer.html
    In your implementation consider assigninng more energy to
    seeds that are shorter, that execute faster, and yield coverage increases more often. Implement this in the
    _assign_energy method. The _normalized_energy method should then normalize the energy values to sum to 1.
    """

    def __init__(self) -> None:
        """Constructor"""
        self.path_frequency: dict = {}

    @abc.abstractmethod
    def _assign_energy(self, seeds: list[AbstractSeed]) -> list[AbstractSeed]:
        """Assigns each seed the same energy"""
        for seed in seeds:
            seed.energy = 1
        return seeds

    def _normalized_energy(self, seeds: list[AbstractSeed]) -> list[float]:
        """Normalize energy"""
        energy = [seed.energy for seed in seeds]
        sum_energy = sum(energy)  # Add up all values in energy
        assert sum_energy != 0
        norm_energy = [nrg / sum_energy for nrg in energy]
        return norm_energy

    def choose(self, seeds: list[AbstractSeed]) -> AbstractSeed:
        """Choose weighted by normalized energy."""
        seeds = self._assign_energy(seeds)
        norm_energy = self._normalized_energy(seeds)
        seed = random.choices(seeds, weights=norm_energy)[0]
        return seed
