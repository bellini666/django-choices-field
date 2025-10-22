import enum
import sys

from django.db import models
from django.utils.translation import gettext_lazy as _

from django_choices_field import IntegerChoicesField, TextChoicesField
from django_choices_field.fields import IntegerChoicesFlagField
from django_choices_field.types import IntegerChoicesFlag


class MyModel(models.Model):
    class TextEnum(models.TextChoices):
        C_FOO = "foo", "T Foo Description"
        C_BAR = "bar", "T Bar Description"

    class TextEnumWithEmptyStateLabel(models.TextChoices):
        __empty__ = "This is the label for the text empty value"
        C_FOO = "foo", "T Foo Description"
        C_BAR = "bar", "T Bar Description"

    class IntegerEnum(models.IntegerChoices):
        I_FOO = 1, "I Foo Description"
        I_BAR = 2, "I Bar Description"

    class IntegerEnumWithEmptyStateLabel(models.IntegerChoices):
        __empty__ = "This is the label for the int empty value"
        I_FOO = 1, "I Foo Description"
        I_BAR = 2, "I Bar Description"

    class IntegerFlagEnum(IntegerChoicesFlag):
        IF_FOO = (
            enum.auto() if sys.version_info >= (3, 11) else 1,
            "IF Foo Description",  # type: ignore
        )
        IF_BAR = (
            enum.auto() if sys.version_info >= (3, 11) else 2,
            "IF Bar Description",  # type: ignore
        )
        IF_BIN = (
            enum.auto() if sys.version_info >= (3, 11) else 4,
            "IF Bin Description",  # type: ignore
        )

    class IntegerFlagEnumTranslated(IntegerChoicesFlag):
        IF_FOO = (
            enum.auto() if sys.version_info >= (3, 11) else 1,
            _("IF Foo Description"),  # type: ignore
        )
        IF_BAR = (
            enum.auto() if sys.version_info >= (3, 11) else 2,
            _("IF Bar Description"),  # type: ignore
        )
        IF_BIN = (
            enum.auto() if sys.version_info >= (3, 11) else 4,
            _("IF Bin Description"),  # type: ignore
        )

    class IntegerFlagEnumWithEmptyStateLabel(IntegerChoicesFlag):
        __empty__ = "This is the label for the flag empty value"
        IF_FOO = (
            enum.auto() if sys.version_info >= (3, 11) else 1,
            "IF Foo Description",  # type: ignore
        )
        IF_BAR = (
            enum.auto() if sys.version_info >= (3, 11) else 2,
            "IF Bar Description",  # type: ignore
        )
        IF_BIN = (
            enum.auto() if sys.version_info >= (3, 11) else 4,
            "IF Bin Description",  # type: ignore
        )

    objects = models.Manager["MyModel"]()  # type: ignore

    c_field = TextChoicesField(
        choices_enum=TextEnum,
        default=TextEnum.C_FOO,
    )
    c_field_nullable = TextChoicesField(
        choices_enum=TextEnum,
        null=True,
    )
    c_field_with_empty_state = TextChoicesField(
        choices_enum=TextEnumWithEmptyStateLabel,
        default=TextEnumWithEmptyStateLabel.C_FOO,
    )
    c_field_with_empty_state_nullable = TextChoicesField(
        choices_enum=TextEnumWithEmptyStateLabel,
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
    i_field_with_empty_state = IntegerChoicesField(
        choices_enum=IntegerEnumWithEmptyStateLabel,
        default=IntegerEnumWithEmptyStateLabel.I_FOO,
    )
    i_field_with_empty_state_nullable = IntegerChoicesField(
        choices_enum=IntegerEnumWithEmptyStateLabel,
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
    ift_field = IntegerChoicesFlagField(
        choices_enum=IntegerFlagEnumTranslated,
        default=IntegerFlagEnumTranslated.IF_FOO,
    )
    ift_field_nullable = IntegerChoicesFlagField(
        choices_enum=IntegerFlagEnumTranslated,
        null=True,
    )
    if_field_with_empty_state = IntegerChoicesFlagField(
        choices_enum=IntegerFlagEnumWithEmptyStateLabel,
        default=IntegerFlagEnumWithEmptyStateLabel.IF_FOO,
    )
    if_field_with_empty_state_nullable = IntegerChoicesFlagField(
        choices_enum=IntegerFlagEnumWithEmptyStateLabel,
        null=True,
    )
