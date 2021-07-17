from django.db import models

from django_choices_field import ChoicesField


class MyModel(models.Model):
    class MyEnum(models.TextChoices):
        FOO = "foo", "Foo Description"
        BAR = "bar", "Bar Description"

    objects = models.Manager["MyModel"]()

    c_field = ChoicesField(
        choices_enum=MyEnum,
        default=MyEnum.FOO,
    )
    c_field_nullable = ChoicesField(
        choices_enum=MyEnum,
        null=True,
    )
