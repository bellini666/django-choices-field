from django.core.exceptions import ValidationError
import pytest

from .models import MyModel


def test_default_value_text():
    m = MyModel()
    assert isinstance(m.c_field, MyModel.TextEnum)
    assert not isinstance(m.c_field, MyModel.IntegerEnum)
    assert m.c_field == MyModel.TextEnum.C_FOO
    assert m.c_field_nullable is None


def test_default_value_integer():
    m = MyModel()
    assert isinstance(m.i_field, MyModel.IntegerEnum)
    assert not isinstance(m.i_field, MyModel.TextEnum)
    assert m.i_field == MyModel.IntegerEnum.I_FOO
    assert m.i_field_nullable is None


def test_created_value_text():
    m = MyModel(c_field=MyModel.TextEnum.C_BAR)

    assert isinstance(m.c_field, MyModel.TextEnum)
    assert not isinstance(m.c_field, MyModel.IntegerEnum)
    assert m.c_field == MyModel.TextEnum.C_BAR
    assert m.c_field_nullable is None


def test_created_value_integer():
    m = MyModel(i_field=MyModel.IntegerEnum.I_BAR)
    assert isinstance(m.i_field, MyModel.IntegerEnum)
    assert not isinstance(m.i_field, MyModel.TextEnum)
    assert m.i_field == MyModel.IntegerEnum.I_BAR
    assert m.i_field_nullable is None


def test_set_value_text(db):
    m = MyModel()
    assert isinstance(m.c_field, MyModel.TextEnum)
    assert m.c_field == MyModel.TextEnum.C_FOO
    m.c_field = MyModel.TextEnum.C_BAR
    assert isinstance(m.c_field, MyModel.TextEnum)
    assert m.c_field == MyModel.TextEnum.C_BAR
    m.save()


def test_set_value_integer(db):
    m = MyModel()
    assert isinstance(m.i_field, MyModel.IntegerEnum)
    assert m.i_field == MyModel.IntegerEnum.I_FOO
    m.i_field = MyModel.IntegerEnum.I_BAR
    assert isinstance(m.i_field, MyModel.IntegerEnum)
    assert m.i_field == MyModel.IntegerEnum.I_BAR
    m.save()


def test_set_none_text(db):
    m = MyModel(c_field_nullable=MyModel.TextEnum.C_FOO)
    assert isinstance(m.c_field_nullable, MyModel.TextEnum)
    assert m.c_field_nullable == MyModel.TextEnum.C_FOO
    m.c_field_nullable = None
    m.save()

    m = MyModel.objects.get(pk=m.pk)
    assert m.c_field_nullable is None


def test_set_none_integer(db):
    m = MyModel(i_field_nullable=MyModel.IntegerEnum.I_FOO)
    assert isinstance(m.i_field_nullable, MyModel.IntegerEnum)
    assert m.i_field_nullable == MyModel.IntegerEnum.I_FOO
    m.i_field_nullable = None
    m.save()

    m = MyModel.objects.get(pk=m.pk)
    assert m.i_field_nullable is None


@pytest.mark.parametrize("v", [10, "abc"])
def test_set_wrong_value_text(v, db):
    m = MyModel()
    with pytest.raises(ValidationError) as exc:
        m.c_field = v
        m.save()

    assert list(exc.value) == [f"“{v}” must be a subclass of <enum 'TextEnum'>."]


@pytest.mark.parametrize("v", [10, "abc"])
def test_set_wrong_value_integer(v, db):
    if isinstance(v, int):
        m = MyModel()
        with pytest.raises(ValidationError) as exc:
            m.i_field = v  # type:ignore (we really want the error here)
            m.save()

        assert list(exc.value) == [f"“{v}” must be a subclass of <enum 'IntegerEnum'>."]
    else:
        m = MyModel()
        with pytest.raises(ValueError) as exc:
            m.i_field = v
            m.save()

        assert str(exc.value) == f"Field 'i_field' expected a number but got '{v}'."
