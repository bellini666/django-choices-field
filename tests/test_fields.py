from django.core.exceptions import ValidationError
import pytest

from .models import MyModel


def test_default_value():
    m = MyModel()
    assert isinstance(m.c_field, MyModel.MyEnum)
    assert m.c_field == MyModel.MyEnum.FOO
    assert m.c_field_nullable is None


def test_created_value():
    m = MyModel(c_field=MyModel.MyEnum.BAR)
    assert isinstance(m.c_field, MyModel.MyEnum)
    assert m.c_field == MyModel.MyEnum.BAR
    assert m.c_field_nullable is None


def test_set_value(db):
    m = MyModel()
    assert isinstance(m.c_field, MyModel.MyEnum)
    assert m.c_field == MyModel.MyEnum.FOO
    m.c_field = MyModel.MyEnum.BAR
    assert isinstance(m.c_field, MyModel.MyEnum)
    assert m.c_field == MyModel.MyEnum.BAR
    m.save()
    m = MyModel.objects.get(pk=m.pk)
    assert isinstance(m.c_field, MyModel.MyEnum)
    assert m.c_field == MyModel.MyEnum.BAR


def test_set_none(db):
    m = MyModel(c_field_nullable=MyModel.MyEnum.FOO)
    assert isinstance(m.c_field_nullable, MyModel.MyEnum)
    assert m.c_field_nullable == MyModel.MyEnum.FOO
    m.c_field_nullable = None
    m.save()
    m = MyModel.objects.get(pk=m.pk)
    assert m.c_field_nullable is None


def test_set_wrong_value(db):
    m = MyModel()
    with pytest.raises(ValidationError) as exc:
        m.c_field = 1
        m.save()

    assert list(exc.value) == ["“1” must be a subclass of <enum 'MyEnum'>."]
