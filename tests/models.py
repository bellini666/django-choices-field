from django.db import models

from django_choices_field import IntegerChoicesField, TextChoicesField


class MyModel(models.Model):
    class TextEnum(models.TextChoices):
        C_FOO = "foo", "T Foo Description"
        C_BAR = "bar", "T Bar Description"

    class IntegerEnum(models.IntegerChoices):
        I_FOO = 1, "I Foo Description"
        I_BAR = 2, "I Bar Description"

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
