
from .creators import SerializerCreator, ModelCreator

__all__ = ['NestedCreate']


class NestedCreate:
    def __init__(self, model=None, validators=None, serializer_class=None, source=None, context=None):
        self.source = source or model.__class__.__name__.lower()
        if serializer_class:
            self.creator = SerializerCreator(serializer_class=serializer_class, context=context)
        else:
            self.creator = ModelCreator(model=model)

        self.validators = validators
        self.source_obj = None
        self.data = {}

    def set_data(self, data):
        self.data = data

    def is_valid(self):
        assert self.data is not None, (
            f'You should first set to data attr  {self.__class__.__name__}'
        )
        if self.validators:
            all(map(lambda x: x(self.data), self.validators))

    def create(self):
        assert self.data is not None, (
            f'You should first set to data attr  {self.__class__.__name__}'
        )
        self.creator.source_obj = self.source_obj
        return self.creator.create(self.data)
