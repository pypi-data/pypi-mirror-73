__all__ = ['SerializerCreator', 'ModelCreator']


class BaseCreator:
    def create(self, data):
        raise NotImplementedError


class SerializerCreator(BaseCreator):
    def __init__(self, serializer_class, context, **kwargs):
        self.serializer_class = serializer_class
        self.context = context
        self.kwargs = kwargs

    def get_serializer(self, *args, **kwargs):
        return self.serializer_class(*args, **kwargs)

    def create(self, data):
        serializer = self.get_serializer(context=self.context, data=data, many=isinstance(data, list))
        if serializer.is_valid():
            obj = serializer.save()
            return obj
        raise BaseException(str(serializer.errors))


class ModelCreator(BaseCreator):
    def __init__(self, model):
        self.model = model

    def create(self, data):
        try:
            if isinstance(data, list):
                for d in data:
                    obj = self.model.objects.create(**d)
            else:
                self.model.objects.create(**data)
            return True
        except BaseException as e:
            print(e)
            return str(e)
