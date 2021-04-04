from django.db.models import Prefetch
from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet

from images.enums import FormatType
from images.exceptions import NotValidFormatType
from images.models import Image, Label
from images.renderers import InternalRenderer, ExportRenderer
from images.serializers import SerializerRegistry


class ImagesView(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    GenericViewSet
):
    renderer_classes = (InternalRenderer, ExportRenderer)

    def get_serializer_class(self):
        if self.request.method == 'GET':
            query = self.request.query_params.get('format')
            try:
                serializer_cls = SerializerRegistry.get_serializer_class(FormatType(query))
                return serializer_cls
            except ValueError:
                raise NotValidFormatType(f'The format {query} is not supported')
        else:
            return SerializerRegistry.get_serializer_class(FormatType.INTERNAL)

    def get_queryset(self):
        query = self.request.query_params.get('format')

        labels_prefetch_qs = Label.objects.all()
        if query == FormatType.EXPORT.value:
            labels_prefetch_qs = labels_prefetch_qs.filter(meta__confirmed=True)

        return Image.objects.select_related('annotation').prefetch_related(
            Prefetch(
                'annotation__label_set',
                queryset=labels_prefetch_qs,
            )
        ).all()

    def get_serializer_context(self):
        result = super().get_serializer_context()

        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field
        result['image_id'] = self.kwargs.get(lookup_url_kwarg)

        return result

