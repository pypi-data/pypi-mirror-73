from rest_framework import serializers

__all__ = ['NestedCreaterSerializer']


class NestedCreaterSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        obj = super().create(validated_data)
        for field in getattr(self.Meta, 'relations_create', []):
            if field.__class__.__name__ == 'NestedCreate':
                request_data = self.context['request'].data.get(field.source).copy()
                request_data.update({field.source: obj})
                field.set_data(request_data)
                field.is_valid()
                field.create()
        return obj
