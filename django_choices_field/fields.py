import functools
import itertools
from collections.abc import Callable, Sequence
from typing import (
    ClassVar,
    cast,
)

from django.core.exceptions import ImproperlyConfigured, ValidationError
from django.db import models

from .types import IntegerChoicesFlag


def _get_flag_description(descs: Sequence[str]) -> str:
    return "|".join(str(desc) for desc in descs)


def _get_integer_enum_members(choices: list[tuple[int | None, str]]) -> dict[str, int]:
    # choices can contain the `None` key which can't be mapped to an enum. See
    # Django Model Field docs about Enumeration Types for more info about
    # labelling empty states with `__empty__`.
    filtered_choices = [(k, v) for (k, v) in choices if k is not None]
    return {desc.replace(" ", "_").upper(): value for value, desc in filtered_choices}


try:
    from django.utils.functional import Promise, lazy
except ImportError:  # pragma: nocover
    Promise = None
    _get_flag_description_lazy = None
else:
    _get_flag_description_lazy = cast(
        "Callable[[Sequence[str]], str]",
        lazy(_get_flag_description, str),
    )


class TextChoicesField(models.CharField):
    """A CharField that validates and stores values from a TextChoices enum.

    This field ensures that only valid values from the specified TextChoices enum
    are accepted, providing type safety and validation at the database level.
    """

    description: ClassVar[str] = "TextChoices"
    default_error_messages: ClassVar[dict[str, str]] = {
        "invalid": "“%(value)s” must be a subclass of %(enum)s.",
    }

    def __init__(
        self,
        choices_enum: type[models.TextChoices] | None = None,
        verbose_name: str | None = None,
        name: str | None = None,
        **kwargs,
    ):
        if choices_enum is not None:
            self.choices_enum = choices_enum
            if getattr(self, "null", False) or kwargs.get("null"):
                kwargs["choices"] = choices_enum.choices
            else:
                kwargs["choices"] = [
                    (k, v) for (k, v) in choices_enum.choices if cast("object", k) is not None
                ]
        elif "choices" in kwargs:
            self.choices_enum = models.TextChoices(
                "ChoicesEnum",
                [(k, (k, v)) for k, v in kwargs["choices"] if k is not None],
            )
        else:
            raise TypeError("either of choices_enum or choices must be provided")

        kwargs.setdefault(
            "max_length",
            max(len(c[0]) for c in kwargs["choices"] if c[0] is not None),
        )

        super().__init__(verbose_name=verbose_name, name=name, **kwargs)

        if self.blank and not self.null:
            raise ImproperlyConfigured(
                f"{self.__class__.__name__} with blank=True must also have null=True.",
            )

    def to_python(self, value):
        if value in self.empty_values:  # type: ignore[attr-defined]
            return None

        try:
            return self.choices_enum(value)  # type: ignore[operator]
        except ValueError as e:
            raise ValidationError(
                self.error_messages["invalid"],
                code="invalid",
                params={"value": value, "enum": self.choices_enum},
            ) from e

    def from_db_value(self, value, expression, connection):
        return self.to_python(value)

    def get_prep_value(self, value):
        value = super().get_prep_value(value)
        return self.to_python(value)


class IntegerChoicesField(models.IntegerField):
    """An IntegerField that validates and stores values from an IntegerChoices enum.

    This field ensures that only valid integer values from the specified IntegerChoices enum
    are accepted, providing type safety and validation at the database level.
    """

    description: ClassVar[str] = "IntegerChoices"
    default_error_messages: ClassVar[dict[str, str]] = {
        "invalid": "“%(value)s” must be a subclass of %(enum)s.",
    }

    def __init__(
        self,
        choices_enum: type[models.IntegerChoices] | None = None,
        verbose_name: str | None = None,
        name: str | None = None,
        **kwargs,
    ):
        if choices_enum is not None:
            self.choices_enum = choices_enum
            if getattr(self, "null", False) or kwargs.get("null"):
                kwargs["choices"] = choices_enum.choices
            else:
                kwargs["choices"] = [
                    (k, v) for (k, v) in choices_enum.choices if cast("object", k) is not None
                ]
        elif "choices" in kwargs:
            enum_members = _get_integer_enum_members(kwargs["choices"])
            self.choices_enum = models.IntegerChoices("ChoicesEnum", enum_members)
        else:
            raise TypeError("either of choices_enum or choices must be provided")

        super().__init__(verbose_name=verbose_name, name=name, **kwargs)

        if self.blank and not self.null:
            raise ImproperlyConfigured(
                f"{self.__class__.__name__} with blank=True must also have null=True.",
            )

    def to_python(self, value):
        if value is None:
            return None

        try:
            return self.choices_enum(int(value) if isinstance(value, str) else value)
        except ValueError as e:
            raise ValidationError(
                self.error_messages["invalid"],
                code="invalid",
                params={"value": value, "enum": self.choices_enum},
            ) from e

    def from_db_value(self, value, expression, connection):
        return self.to_python(value)

    def get_prep_value(self, value):
        value = super().get_prep_value(value)
        return self.to_python(value)

    def formfield(self, **kwargs):  # pragma:nocover
        return super().formfield(
            **{
                "coerce": self.to_python,
                **kwargs,
            },
        )


class IntegerChoicesFlagField(models.IntegerField):
    """An IntegerField that validates and stores bitwise flag values from an IntegerChoicesFlag enum.

    This field supports storing combinations of flags from the specified IntegerChoicesFlag enum,
    allowing multiple enum values to be combined using bitwise operations.
    """

    description: ClassVar[str] = "IntegerChoicesFlag"
    default_error_messages: ClassVar[dict[str, str]] = {
        "invalid": "“%(value)s” must be a subclass of %(enum)s.",
    }

    def __init__(
        self,
        choices_enum: type[IntegerChoicesFlag] | None = None,
        verbose_name: str | None = None,
        name: str | None = None,
        **kwargs,
    ):
        if choices_enum is not None:
            self.choices_enum = choices_enum

            choices: list[tuple[int | None, str]]
            if getattr(self, "null", False) or kwargs.get("null"):
                choices = list(choices_enum.choices)
            else:
                choices = [
                    (k, v) for (k, v) in choices_enum.choices if cast("object", k) is not None
                ]

            default_choices = [(x.value, x.label) for x in choices_enum]
            for i in range(1, len(default_choices)):
                for combination in itertools.combinations(default_choices, i + 1):
                    value = functools.reduce(lambda a, b: a | b[0], combination, 0)

                    descs = [c[1] for c in combination]
                    if Promise is not None and any(isinstance(desc, Promise) for desc in descs):
                        assert _get_flag_description_lazy is not None
                        desc = _get_flag_description_lazy(descs)
                    else:
                        desc = _get_flag_description(descs)

                    choices.append((value, desc))

            kwargs["choices"] = choices
        elif "choices" in kwargs:
            default_choices_length = len(kwargs["choices"]).bit_length()
            default_choices = [kwargs["choices"][i] for i in range(default_choices_length)]
            enum_members = _get_integer_enum_members(default_choices)
            self.choices_enum = models.IntegerChoices("ChoicesEnum", enum_members)
        else:
            raise TypeError("either of choices_enum or choices must be provided")

        super().__init__(verbose_name=verbose_name, name=name, **kwargs)

        if self.blank and not self.null:
            raise ImproperlyConfigured(
                f"{self.__class__.__name__} with blank=True must also have null=True.",
            )

    def to_python(self, value):
        if value is None:
            return None

        try:
            return self.choices_enum(int(value) if isinstance(value, str) else value)
        except ValueError as e:
            raise ValidationError(
                self.error_messages["invalid"],
                code="invalid",
                params={"value": value, "enum": self.choices_enum},
            ) from e

    def from_db_value(self, value, expression, connection):
        return self.to_python(value)

    def get_prep_value(self, value):
        value = super().get_prep_value(value)
        return self.to_python(value)

    def formfield(self, **kwargs):  # pragma:nocover
        return super().formfield(
            **{
                "coerce": self.to_python,
                **kwargs,
            },
        )
