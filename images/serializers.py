import json
from typing import Dict, Type, Optional

from django.shortcuts import get_object_or_404
from rest_framework.exceptions import ValidationError
from rest_framework.fields import UUIDField, CharField, ListField, JSONField, SerializerMethodField
from rest_framework.serializers import ModelSerializer, BaseSerializer

from images.enums import FormatType
from images.models import Image, Label, Annotation


class SerializerRegistry:
    _registry: Dict[FormatType, Type[BaseSerializer]] = {}
    response_format: FormatType = NotImplementedError

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        cls._registry[cls.response_format] = cls

    @classmethod
    def get_serializer_class(cls, response_format: FormatType) -> Optional[Type[BaseSerializer]]:
        return cls._registry.get(response_format)


class InternalLabelSerializer(ModelSerializer):

    def get_fields(self, *args, **kwargs):
        fields = super().get_fields(*args, **kwargs)
        request = self.context.get('request', None)
        if request and getattr(request, 'method', None) == 'PUT':
            fields['id'].required = True
        return fields

    id = UUIDField(required=False)
    class_id = CharField()
    surface = ListField(child=CharField())
    shape = JSONField()
    meta = JSONField()

    class Meta:
        model = Label
        fields = ('id', 'class_id', 'surface', 'shape', 'meta',)


class ExportLabelSerializer(ModelSerializer):
    id = UUIDField(read_only=True)
    class_id = CharField()
    surface = SerializerMethodField()

    def get_surface(self, label: Label) -> str:
        return ''.join(label.surface)

    class Meta:
        model = Label
        fields = ('id', 'class_id', 'surface',)


class InternalImageSerializer(SerializerRegistry, ModelSerializer):
    response_format = FormatType.INTERNAL

    labels = InternalLabelSerializer(source='annotation.label_set', many=True, required=False)

    def get_fields(self, *args, **kwargs):
        fields = super().get_fields(*args, **kwargs)
        request = self.context.get('request', None)
        if request and getattr(request, 'method', None) == 'PUT':
            fields['image'].required = False
        return fields

    def to_internal_value(self, data):
        meta_file = data.pop('metadata', None)

        # will remove image metadata
        result = super().to_internal_value(data)

        metadata = json.load(meta_file[0]) if meta_file else {'labels': []}
        labels_data = InternalLabelSerializer(many=True).to_internal_value(metadata['labels'])
        result.update({'annotation': {'label_set': labels_data}})
        return result

    def create(self, validated_data):
        # drop annotation because DRF does not support writable dotted-source
        labels_data = validated_data.pop('annotation')['label_set']
        image_instance = super().create(validated_data)
        annotation = Annotation.objects.create(image=image_instance)
        labels_object = [Label(annotation=annotation, **label_data) for label_data in labels_data]
        Label.objects.bulk_create(labels_object)
        return image_instance

    def update(self, instance, validated_data):
        labels_data = validated_data['annotation']['label_set']

        labels_objects = []
        image_id = self.context['image_id']
        for label_data in labels_data:
            label = get_object_or_404(Label, id=label_data.get('id'))

            if str(label.annotation.image.id) != image_id:
                raise ValidationError('Does not allow to update labels not connected with image')

            for field_name, field_value in label_data.items():
                setattr(label, field_name, field_value)
            labels_objects.append(label)

        Label.objects.bulk_update(labels_objects, ['class_id', 'surface', 'shape', 'meta'])
        instance.refresh_from_db()
        return instance

    class Meta:
        model = Image
        fields = ('id', 'image', 'labels',)


class ExportImageSerializer(SerializerRegistry, ModelSerializer):

    response_format = FormatType.EXPORT

    labels = ExportLabelSerializer(source='annotation.label_set', many=True)

    class Meta:
        model = Image
        fields = ('id', 'image', 'labels',)
