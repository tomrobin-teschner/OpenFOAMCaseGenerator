from abc import ABC, abstractmethod


class TestCaseBase(ABC):
    @abstractmethod
    def setup_case(self):
        pass