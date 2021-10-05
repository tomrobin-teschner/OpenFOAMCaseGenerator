from abc import ABCMeta, abstractmethod


class CasePropertiesBase(metaclass=ABCMeta):
    @staticmethod
    @abstractmethod
    def get_properties():
        pass
