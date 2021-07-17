from django.core.exceptions import ValidationError
from django.db import models


class ChoicesField(models.CharField):
    description = "Choices"
    default_error_messages = {
        "invalid": "“%(value)s” must be a subclass of %(enum)s.",
    }

    def __init__(self, verbose_name=None, name=None, choices_enum=None, **kwargs):
        self.choices_enum = choices_enum
        kwargs["choices"] = choices_enum.choices
        kwargs.setdefault("max_length", max(len(c.value) for c in choices_enum))
        super().__init__(verbose_name=verbose_name, name=name, **kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        kwargs["choices_enum"] = self.choices_enum
        return name, path, args, kwargs

    def to_python(self, value):
        print(1, value, type(value))
        if value is None:
            return None

        if isinstance(value, self.choices_enum):
            return value

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
        return value.value if value is not None else None
