import pytest
from inline_snapshot import snapshot

from .utils import (
    Result,
    requires_mypy,
    requires_pyright,
    requires_ty,
    typecheck,
)

pytestmark = [requires_pyright, requires_mypy, requires_ty]


CODE = """
from django.db import models

from django_choices_field import IntegerChoicesField, TextChoicesField
from django_choices_field.fields import IntegerChoicesFlagField
from django_choices_field.types import IntegerChoicesFlag


class TextEnum(models.TextChoices):
    FOO = "foo", "Foo Description"
    BAR = "bar", "Bar Description"


class IntegerEnum(models.IntegerChoices):
    FOO = 1, "Foo Description"
    BAR = 2, "Bar Description"


class IntegerFlagEnum(IntegerChoicesFlag):
    FOO = 1
    BAR = 2


class MyModel(models.Model):
    # TextChoicesField - non-null
    text_field = TextChoicesField(
        choices_enum=TextEnum,
        default=TextEnum.FOO,
    )
    # TextChoicesField - nullable
    text_field_nullable = TextChoicesField(
        choices_enum=TextEnum,
        null=True,
    )
    # IntegerChoicesField - non-null
    int_field = IntegerChoicesField(
        choices_enum=IntegerEnum,
        default=IntegerEnum.FOO,
    )
    # IntegerChoicesField - nullable
    int_field_nullable = IntegerChoicesField(
        choices_enum=IntegerEnum,
        null=True,
    )
    # IntegerChoicesFlagField - non-null
    flag_field = IntegerChoicesFlagField(
        choices_enum=IntegerFlagEnum,
        default=IntegerFlagEnum.FOO,
    )
    # IntegerChoicesFlagField - nullable
    flag_field_nullable = IntegerChoicesFlagField(
        choices_enum=IntegerFlagEnum,
        null=True,
    )

    class Meta:
        app_label = "test"


instance = MyModel()

# Reveal types for non-null fields
reveal_type(instance.text_field)
reveal_type(instance.int_field)
reveal_type(instance.flag_field)

# Reveal types for nullable fields
reveal_type(instance.text_field_nullable)
reveal_type(instance.int_field_nullable)
reveal_type(instance.flag_field_nullable)
"""


def test_field_types(subtests: pytest.Subtests):
    results = typecheck(CODE)

    with subtests.test(msg="pyright"):
        assert results.pyright == snapshot(
            [
                Result(
                    type="information",
                    message='Type of "instance.text_field" is "TextEnum"',
                    line=63,
                    column=13,
                ),
                Result(
                    type="information",
                    message='Type of "instance.int_field" is "IntegerEnum"',
                    line=64,
                    column=13,
                ),
                Result(
                    type="information",
                    message='Type of "instance.flag_field" is "IntegerFlagEnum"',
                    line=65,
                    column=13,
                ),
                Result(
                    type="information",
                    message='Type of "instance.text_field_nullable" is "TextEnum | None"',
                    line=68,
                    column=13,
                ),
                Result(
                    type="information",
                    message='Type of "instance.int_field_nullable" is "IntegerEnum | None"',
                    line=69,
                    column=13,
                ),
                Result(
                    type="information",
                    message='Type of "instance.flag_field_nullable" is "IntegerFlagEnum | None"',
                    line=70,
                    column=13,
                ),
            ]
        )

    with subtests.test(msg="mypy"):
        assert results.mypy == snapshot(
            [
                Result(
                    type="note",
                    message='Revealed type is "mypy_test.TextEnum"',
                    line=63,
                    column=13,
                ),
                Result(
                    type="note",
                    message='Revealed type is "mypy_test.IntegerEnum"',
                    line=64,
                    column=13,
                ),
                Result(
                    type="note",
                    message='Revealed type is "mypy_test.IntegerFlagEnum"',
                    line=65,
                    column=13,
                ),
                Result(
                    type="note",
                    message='Revealed type is "mypy_test.TextEnum | None"',
                    line=68,
                    column=13,
                ),
                Result(
                    type="note",
                    message='Revealed type is "mypy_test.IntegerEnum | None"',
                    line=69,
                    column=13,
                ),
                Result(
                    type="note",
                    message='Revealed type is "mypy_test.IntegerFlagEnum | None"',
                    line=70,
                    column=13,
                ),
            ]
        )

    # ty doesn't fully support Django model fields yet.
    # See: https://github.com/astral-sh/ty/issues/1018
    with subtests.test(msg="ty"):
        pytest.xfail("ty doesn't support Django model fields yet")
        assert results.ty == snapshot(
            [
                Result(
                    type="information",
                    message="Revealed type: `TextEnum`",
                    line=63,
                    column=13,
                ),
                Result(
                    type="information",
                    message="Revealed type: `IntegerEnum`",
                    line=64,
                    column=13,
                ),
                Result(
                    type="information",
                    message="Revealed type: `IntegerFlagEnum`",
                    line=65,
                    column=13,
                ),
                Result(
                    type="information",
                    message="Revealed type: `TextEnum | None`",
                    line=68,
                    column=13,
                ),
                Result(
                    type="information",
                    message="Revealed type: `IntegerEnum | None`",
                    line=69,
                    column=13,
                ),
                Result(
                    type="information",
                    message="Revealed type: `IntegerFlagEnum | None`",
                    line=70,
                    column=13,
                ),
            ]
        )
