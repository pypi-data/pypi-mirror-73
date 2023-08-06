from abc import abstractmethod, ABCMeta
from typing import Any, List

converter_registry = {}


def convert(source: Any, destination: Any):
    converter = converter_registry.get(source.__class__, {}).get(destination, None)
    return converter.convert(source)


def convert_multiple(sources: List[Any], destination: Any):
    if len(sources) > 0:
        converter = converter_registry.get(sources[0].__class__, {}).get(destination, None)
        return [converter.convert(source) for source in sources]
    else:
        return []


class Converter(metaclass=ABCMeta):

    @classmethod
    def __init_subclass__(cls, **kwargs):
        cls.to_class = kwargs.pop("to_class")
        cls.from_class = kwargs.pop("from_class")
        super().__init_subclass__(**kwargs)
        converter_registry[cls.from_class] = converter_registry.get(cls.from_class, {})
        converter_registry[cls.from_class][cls.to_class] = cls()

    @abstractmethod
    def convert(self, source: Any):
        pass