from abc import ABC, abstractmethod
from dataclasses import dataclass

from croniter import croniter


@dataclass()
class Schedule(ABC):
    """
    Abstract Scheduler parent class
    contains the default values for a Scheduler and the main method asdict
    """

    name: str
    cors: str
    payload: dict
    description: str

    def __post_init__(self):
        assert croniter.is_valid(self.cors), 'Cors is wrong'

    @abstractmethod
    def asdict(self, base_name, project) -> dict:
        pass
