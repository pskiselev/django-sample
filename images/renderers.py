from rest_framework.renderers import JSONRenderer

from images.enums import FormatType


class InternalRenderer(JSONRenderer):
    format = FormatType.INTERNAL.value


class ExportRenderer(JSONRenderer):
    format = FormatType.EXPORT.value
