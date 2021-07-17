from typing import Optional, Type

from django.core.exceptions import ValidationError
from django.db import models


class TextChoicesField(models.CharField):
    description = "TextChoices"
    default_error_messages = {
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
        except ValueError:
            raise ValidationError(
                self.error_messages["invalid"],
                code="invalid",
                params={"value": value, "enum": self.choices_enum},
            )

    def from_db_value(self, value, expression, connection):
        return self.to_python(value)

    def get_prep_value(self, value):
        value = super().get_prep_value(value)
        return self.to_python(value)


class IntegerChoicesField(models.IntegerField):
    description = "IntegerChoices"
    default_error_messages = {
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
            return self.choices_enum(value)
        except ValueError:
            raise ValidationError(
                self.error_messages["invalid"],
                code="invalid",
                params={"value": value, "enum": self.choices_enum},
            )

    def from_db_value(self, value, expression, connection):
        return self.to_python(value)

    def get_prep_value(self, value):
        value = super().get_prep_value(value)
        return self.to_python(value)
