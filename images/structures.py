from enum import Enum
from typing import Tuple

import jsonschema
from django.core.exceptions import ValidationError as DjangoValidationError
from django.utils.deconstruct import deconstructible


class ChoicesEnum(Enum):
    @classmethod
    def get_choices(cls) -> Tuple[Tuple[str, str], ...]:
        if not hasattr(cls, '_choices'):
            cls._choices = tuple(
                (member.value, member.name) for member in cls
            )
        return cls._choices


@deconstructible
class JsonSchemaValidator(object):
    def __init__(self, schema: dict):
        self.schema = schema

    def __call__(self, value):
        try:
            jsonschema.validate(
                value, self.schema, format_checker=jsonschema.FormatChecker(),
            )
        except jsonschema.ValidationError as exc:
            raise DjangoValidationError(exc)
