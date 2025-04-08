class AbstractSeed:
    """Represent an seed with additional attributes, such as energy.
    It is necessary to create a power schedule that assigns energy to seeds.
    """

    def __init__(self, data: str) -> None:
        """Initialize from seed data"""
        self.data = data

        # These will be needed for advanced power schedules
        self.coverage = 0
        self.energy = 0.0

    def __str__(self) -> str:
        """Returns data as string representation of the seed"""
        return self.data
