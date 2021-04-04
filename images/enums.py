from enum import unique

from images.structures import ChoicesEnum


@unique
class LabelClass(ChoicesEnum):
    TOOTH = 'tooth'
    UNDEFINED = 'undefined'


@unique
class FormatType(ChoicesEnum):
    INTERNAL = 'internal'
    EXPORT = 'export'
