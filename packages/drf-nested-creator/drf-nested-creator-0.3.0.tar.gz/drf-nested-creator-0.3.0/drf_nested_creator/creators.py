__all__ = ['SerializerCreator', 'ModelCreator']


class BaseCreator:
    def create(self, data):
        raise NotImplementedError

    def perform_data(self, data):
        if isinstance(data, list):
            return map(lambda x: x.update(
                {self.source_obj.__class__.__name__.lower():
                     self.source_obj, f'{self.source_obj.__class__.__name__.lower()}_id': self.source_obj.id}), data)
        else:
            new_data = data.copy()
            new_data[self.source_obj.__class__.__name__.lower()] = self.source_obj
            new_data[f'{self.source_obj.__class__.__name__.lower()}_id'] = self.source_obj.id
            return new_data


class SerializerCreator(BaseCreator):
    def __init__(self, serializer_class, context, **kwargs):
        self.serializer_class = serializer_class
        self.context = context
        self.kwargs = kwargs
        self.source_obj = None

    def get_serializer(self, *args, **kwargs):
        return self.serializer_class(*args, **kwargs)

    def create(self, data):
        data = self.perform_data(data)
        serializer = self.get_serializer(context=self.context, data=data, many=isinstance(data, list))
        if serializer.is_valid():
            obj = serializer.save()
            return obj
        raise BaseException(str(serializer.errors))


class ModelCreator(BaseCreator):
    def __init__(self, model):
        self.model = model

    def create(self, data):
        perform_data = self.perform_data(d)
        try:
            if isinstance(data, list):
                for d in perform_data:
                    self.model.objects.create(**d)
            else:
                self.model.objects.create(**data)
            return True
        except BaseException as e:
            print(e)
            return str(e)
