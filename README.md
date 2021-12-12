# django-choices-field

[![build status](https://img.shields.io/endpoint.svg?url=https%3A%2F%2Factions-badge.atrox.dev%2Fbellini666%2Fdjango-choices-field%2Fbadge%3Fref%3Dmaster&style=flat)](https://actions-badge.atrox.dev/bellini666/django-choices-field/goto?ref=master)
[![coverage](https://img.shields.io/codecov/c/github/bellini666/django-choices-field.svg)](https://codecov.io/gh/bellini666/django-choices-field)
[![PyPI version](https://img.shields.io/pypi/v/django-choices-field.svg)](https://pypi.org/project/django-choices-field/)
![python version](https://img.shields.io/pypi/pyversions/django-choices-field.svg)
![django version](https://img.shields.io/pypi/djversions/django-choices-field.svg)

Django field that set/get django's new TextChoices/IntegerChoices enum.

## Install

```bash
pip install django-choices-field
```

## Usage

```python
from django.db import models
from django_choices_field import TexChoicesField, IntegerChoicesField


class MyModel(models.Model):
    class TextEnum(models.TextChoices):
        FOO = "foo", "Foo Description"
        BAR = "bar", "Bar Description"

    class IntegerEnum(models.IntegerChoices):
        FIRST = 1, "First Description"
        SECOND = 2, "Second Description"

    c_field = TextChoicesField(
        choices_enum=TextEnum,
        default=TextEnum.FOO,
    )
    i_field = IntegerChoicesField(
        choices_enum=IntegerEnum,
        default=IntegerEnum.FIRST,
    )


obj = MyModel()
obj.c_field  # MyModel.TextEnum.FOO
isinstance(obj.c_field, MyModel.TextEnum) # True
obj.i_field  # MyModel.IntegerEnum.FIRST
isinstance(obj.i_field, MyModel.IntegerEnum) # True
```

## License

This project is licensed under MIT licence (see `LICENSE` for more info)

## Contributing

Make sure to have [poetry](https://python-poetry.org/) installed.

Install dependencies with:

```bash
poetry install
```

Run the testsuite with:

```bash
poetry run pytest
```

Feel free to fork the project and send me pull requests with new features,
corrections and translations. I'll gladly merge them and release new versions
ASAP.
