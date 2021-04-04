import uuid

from django.contrib.postgres.fields import ArrayField, JSONField
from django.db import models
from django.db.models import ImageField

from images.enums import LabelClass
from images.structures import JsonSchemaValidator
from images.validators import LABEL_META_SCHEMA, LABEL_SHAPE_SCHEMA


class Image(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    image = ImageField()


class Annotation(models.Model):
    image = models.OneToOneField(Image, on_delete=models.PROTECT, null=True, blank=True, related_name='annotation')


class Label(models.Model):
    annotation = models.ForeignKey(Annotation, on_delete=models.CASCADE)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    class_id = models.CharField(
        choices=LabelClass.get_choices(),
        max_length=255,
        default=LabelClass.UNDEFINED.value,
    )
    surface = ArrayField(
        models.CharField(max_length=1),
    )
    shape = JSONField(
        validators=[JsonSchemaValidator(LABEL_SHAPE_SCHEMA)],
    )
    meta = JSONField(
        validators=[JsonSchemaValidator(LABEL_META_SCHEMA)],
    )
