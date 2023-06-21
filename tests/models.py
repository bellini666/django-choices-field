import enum
import sys

from django.db import models

from django_choices_field import IntegerChoicesField, TextChoicesField
from django_choices_field.fields import IntegerChoicesFlagField
from django_choices_field.types import IntegerChoicesFlag


class MyModel(models.Model):
    class TextEnum(models.TextChoices):
        C_FOO = "foo", "T Foo Description"
        C_BAR = "bar", "T Bar Description"

    class IntegerEnum(models.IntegerChoices):
        I_FOO = 1, "I Foo Description"
        I_BAR = 2, "I Bar Description"

    class IntegerFlagEnum(IntegerChoicesFlag):
        IF_FOO = enum.auto() if sys.version_info >= (3, 11) else 1, "IF Foo Description"
        IF_BAR = enum.auto() if sys.version_info >= (3, 11) else 2, "IF Bar Description"
        IF_BIN = enum.auto() if sys.version_info >= (3, 11) else 4, "IF Bin Description"

    objects = models.Manager["MyModel"]()

    c_field = TextChoicesField(
        choices_enum=TextEnum,
        default=TextEnum.C_FOO,
    )
    c_field_nullable = TextChoicesField(
        choices_enum=TextEnum,
        null=True,
    )
    i_field = IntegerChoicesField(
        choices_enum=IntegerEnum,
        default=IntegerEnum.I_FOO,
    )
    i_field_nullable = IntegerChoicesField(
        choices_enum=IntegerEnum,
        null=True,
    )
    if_field = IntegerChoicesFlagField(
        choices_enum=IntegerFlagEnum,
        default=IntegerFlagEnum.IF_FOO,
    )
    if_field_nullable = IntegerChoicesFlagField(
        choices_enum=IntegerFlagEnum,
        null=True,
    )
