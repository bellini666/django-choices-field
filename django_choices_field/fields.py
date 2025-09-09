import functools
import itertools
from typing import (
    Callable,
    ClassVar,
    Dict,
    List,
    Optional,
    Sequence,
    Tuple,
    Type,
    cast,
)

from django.core.exceptions import ValidationError
from django.db import models

from .types import IntegerChoicesFlag


def _get_flag_description(descs: Sequence[str]) -> str:
    return "|".join(str(desc) for desc in descs)


def _get_integer_enum_members(choices: List[Tuple[int, str]]) -> Dict[str, int]:
    return {desc.replace(" ", "_").upper(): value for value, desc in choices}


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
        choices_enum: Optional[Type[models.TextChoices]] = None,
        verbose_name: Optional[str] = None,
        name: Optional[str] = None,
        **kwargs,
    ):
        if choices_enum is not None:
            self.choices_enum = choices_enum
            kwargs["choices"] = [(x.value, x.label) for x in choices_enum]
        elif "choices" in kwargs:
            self.choices_enum = models.TextChoices(
                "ChoicesEnum",
                [(k, (k, v)) for k, v in kwargs["choices"]],
            )
        else:
            raise TypeError("either of choices_enum or choices must be provided")
        kwargs.setdefault("max_length", max(len(c[0]) for c in kwargs["choices"]))
        super().__init__(verbose_name=verbose_name, name=name, **kwargs)

    def to_python(self, value):
        if value in self.empty_values:
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
        choices_enum: Optional[Type[models.IntegerChoices]] = None,
        verbose_name: Optional[str] = None,
        name: Optional[str] = None,
        **kwargs,
    ):
        if choices_enum is not None:
            self.choices_enum = choices_enum
            kwargs["choices"] = [(x.value, x.label) for x in choices_enum]
        elif "choices" in kwargs:
            enum_members = _get_integer_enum_members(kwargs["choices"])
            self.choices_enum = models.IntegerChoices("ChoicesEnum", enum_members)
        else:
            raise TypeError("either of choices_enum or choices must be provided")
        super().__init__(verbose_name=verbose_name, name=name, **kwargs)

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
        choices_enum: Optional[Type[IntegerChoicesFlag]] = None,
        verbose_name: Optional[str] = None,
        name: Optional[str] = None,
        **kwargs,
    ):
        if choices_enum is not None:
            self.choices_enum = choices_enum

            default_choices = [(x.value, x.label) for x in choices_enum]
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
        elif "choices" in kwargs:
            default_choices_length = len(kwargs["choices"]).bit_length()
            default_choices = [kwargs["choices"][i] for i in range(default_choices_length)]
            enum_members = _get_integer_enum_members(default_choices)
            self.choices_enum = models.IntegerChoices("ChoicesEnum", enum_members)
        else:
            raise TypeError("either of choices_enum or choices must be provided")

        super().__init__(verbose_name=verbose_name, name=name, **kwargs)

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
