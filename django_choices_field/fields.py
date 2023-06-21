import functools
import itertools
from typing import Callable, ClassVar, Dict, Optional, Sequence, Type, cast

from django.core.exceptions import ValidationError
from django.db import models

from .types import IntegerChoicesFlag


def _get_flag_description(descs: Sequence[str]) -> str:
    return "|".join(str(desc) for desc in descs)


try:
    from django.utils.functional import Promise, lazy
except ImportError:  # pragma: nocover
    Promise = None
    _get_flag_description_lazy = None
else:
    _get_flag_description_lazy = cast(
        Callable[[Sequence[str]], str],
        lazy(_get_flag_description, str),
    )


class TextChoicesField(models.CharField):
    description: ClassVar[str] = "TextChoices"
    default_error_messages: ClassVar[Dict[str, str]] = {
        "invalid": "“%(value)s” must be a subclass of %(enum)s.",
    }

    def __init__(
        self,
        choices_enum: Type[models.TextChoices],
        verbose_name: Optional[str] = None,
        name: Optional[str] = None,
        **kwargs,
    ):
        self.choices_enum = choices_enum
        kwargs["choices"] = choices_enum.choices
        kwargs.setdefault("max_length", max(len(c.value) for c in choices_enum))
        super().__init__(verbose_name=verbose_name, name=name, **kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        kwargs["choices_enum"] = self.choices_enum
        return name, path, args, kwargs

    def to_python(self, value):
        if value is None:
            return None

        try:
            return self.choices_enum(value)
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
    description: ClassVar[str] = "IntegerChoices"
    default_error_messages: ClassVar[Dict[str, str]] = {
        "invalid": "“%(value)s” must be a subclass of %(enum)s.",
    }

    def __init__(
        self,
        choices_enum: Type[models.IntegerChoices],
        verbose_name: Optional[str] = None,
        name: Optional[str] = None,
        **kwargs,
    ):
        self.choices_enum = choices_enum
        kwargs["choices"] = choices_enum.choices
        super().__init__(verbose_name=verbose_name, name=name, **kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        kwargs["choices_enum"] = self.choices_enum
        return name, path, args, kwargs

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
    description: ClassVar[str] = "IntegerChoicesFlag"
    default_error_messages: ClassVar[Dict[str, str]] = {
        "invalid": "“%(value)s” must be a subclass of %(enum)s.",
    }

    def __init__(
        self,
        choices_enum: Type[IntegerChoicesFlag],
        verbose_name: Optional[str] = None,
        name: Optional[str] = None,
        **kwargs,
    ):
        self.choices_enum = choices_enum

        default_choices = choices_enum.choices
        kwargs["choices"] = default_choices[:]
        for i in range(1, len(default_choices)):
            for combination in itertools.combinations(default_choices, i + 1):
                value = functools.reduce(lambda a, b: a | b[0], combination, 0)

                descs = [c[1] for c in combination]
                if Promise is not None and any(isinstance(desc, Promise) for desc in descs):
                    assert _get_flag_description_lazy is not None
                    desc = _get_flag_description_lazy(descs)
                else:
                    desc = _get_flag_description(descs)

                kwargs["choices"].append((value, desc))

        super().__init__(verbose_name=verbose_name, name=name, **kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        kwargs["choices_enum"] = self.choices_enum
        return name, path, args, kwargs

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
