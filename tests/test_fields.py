import sys

import pytest
from django.core.exceptions import ValidationError
from django.db.models import Sum

from .models import MyModel


@pytest.mark.parametrize("fname", ["c_field", "c_field_nullable"])
def test_field_choices_text(fname: str):
    f = MyModel._meta.get_field(fname)
    assert f.choices == [
        ("foo", "T Foo Description"),
        ("bar", "T Bar Description"),
    ]


@pytest.mark.parametrize("fname", ["i_field", "i_field_nullable"])
def test_field_choices_integer(fname: str):
    f = MyModel._meta.get_field(fname)
    assert f.choices == [
        (1, "I Foo Description"),
        (2, "I Bar Description"),
    ]


@pytest.mark.parametrize(
    "fname",
    ["if_field", "if_field_nullable", "ift_field", "ift_field_nullable"],
)
def test_field_choices_integer_flags(fname: str):
    f = MyModel._meta.get_field(fname)
    assert f.choices == [
        (1, "IF Foo Description"),
        (2, "IF Bar Description"),
        (4, "IF Bin Description"),
        (3, "IF Foo Description|IF Bar Description"),
        (5, "IF Foo Description|IF Bin Description"),
        (6, "IF Bar Description|IF Bin Description"),
        (7, "IF Foo Description|IF Bar Description|IF Bin Description"),
    ]


def test_default_value_text():
    m = MyModel()
    assert isinstance(m.c_field, MyModel.TextEnum)
    assert m.c_field == MyModel.TextEnum.C_FOO
    assert m.c_field_nullable is None


def test_default_value_integer():
    m = MyModel()
    assert isinstance(m.i_field, MyModel.IntegerEnum)
    assert m.i_field == MyModel.IntegerEnum.I_FOO
    assert m.i_field_nullable is None


def test_default_value_integer_flag():
    m = MyModel()
    assert isinstance(m.if_field, MyModel.IntegerFlagEnum)
    assert m.if_field == MyModel.IntegerFlagEnum.IF_FOO
    assert m.if_field_nullable is None


def test_created_value_text():
    m = MyModel(c_field=MyModel.TextEnum.C_BAR)

    assert isinstance(m.c_field, MyModel.TextEnum)
    assert m.c_field == MyModel.TextEnum.C_BAR
    assert m.c_field_nullable is None


def test_created_value_integer():
    m = MyModel(i_field=MyModel.IntegerEnum.I_BAR)
    assert isinstance(m.i_field, MyModel.IntegerEnum)
    assert m.i_field == MyModel.IntegerEnum.I_BAR
    assert m.i_field_nullable is None


def test_created_value_integer_flag():
    m = MyModel(if_field=MyModel.IntegerFlagEnum.IF_BAR)
    assert isinstance(m.if_field, MyModel.IntegerFlagEnum)
    assert m.if_field == MyModel.IntegerFlagEnum.IF_BAR
    assert m.if_field_nullable is None


@pytest.mark.skipif(sys.version_info < (3, 11), reason="Requires Python 3.11+ to work properly")
def test_created_value_integer_flag_multiple():
    m = MyModel(if_field=MyModel.IntegerFlagEnum.IF_BAR | MyModel.IntegerFlagEnum.IF_BIN)
    assert isinstance(m.if_field, MyModel.IntegerFlagEnum)
    assert m.if_field == MyModel.IntegerFlagEnum.IF_BAR | MyModel.IntegerFlagEnum.IF_BIN
    assert m.if_field_nullable is None


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


def test_set_value_integer_flag(db):
    m = MyModel()
    assert isinstance(m.if_field, MyModel.IntegerFlagEnum)
    assert m.if_field == MyModel.IntegerFlagEnum.IF_FOO
    m.if_field = MyModel.IntegerFlagEnum.IF_BAR
    assert isinstance(m.if_field, MyModel.IntegerFlagEnum)
    assert m.if_field == MyModel.IntegerFlagEnum.IF_BAR
    m.save()


@pytest.mark.skipif(sys.version_info < (3, 11), reason="Requires Python 3.11+ to work properly")
def test_set_value_integer_flag_multiple(db):
    m = MyModel()
    assert isinstance(m.if_field, MyModel.IntegerFlagEnum)
    assert m.if_field == MyModel.IntegerFlagEnum.IF_FOO
    m.if_field = MyModel.IntegerFlagEnum.IF_BAR | MyModel.IntegerFlagEnum.IF_BIN
    assert isinstance(m.if_field, MyModel.IntegerFlagEnum)
    assert m.if_field == MyModel.IntegerFlagEnum.IF_BAR | MyModel.IntegerFlagEnum.IF_BIN
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


def test_set_none_integer_flag(db):
    m = MyModel(if_field_nullable=MyModel.IntegerFlagEnum.IF_FOO)
    assert isinstance(m.if_field_nullable, MyModel.IntegerFlagEnum)
    assert m.if_field_nullable == MyModel.IntegerFlagEnum.IF_FOO
    m.if_field_nullable = None
    m.save()

    m = MyModel.objects.get(pk=m.pk)
    assert m.if_field_nullable is None


def test_set_text_integer(db):
    m = MyModel(i_field_nullable=MyModel.IntegerEnum.I_FOO)
    assert isinstance(m.i_field_nullable, MyModel.IntegerEnum)
    assert m.i_field_nullable == MyModel.IntegerEnum.I_FOO
    m.i_field = "2"  # type: ignore
    m.save()

    m = MyModel.objects.get(pk=m.pk)
    assert m.i_field == 2


@pytest.mark.parametrize("v", [10, "abc"])
def test_set_wrong_value_text(v, db):
    m = MyModel()
    m.c_field = v
    with pytest.raises(ValidationError) as exc:
        m.save()

    assert list(exc.value) == [f"“{v}” must be a subclass of <enum 'TextEnum'>."]


@pytest.mark.parametrize("v", [10, "abc"])
def test_set_wrong_value_integer(v, db):
    if isinstance(v, int):
        m = MyModel()
        m.i_field = v  # type: ignore
        with pytest.raises(ValidationError) as exc:
            m.save()

        assert list(exc.value) == [f"“{v}” must be a subclass of <enum 'IntegerEnum'>."]
    else:
        m = MyModel()
        m.i_field = v
        with pytest.raises(ValueError) as exc:  # noqa: PT011
            m.save()

        assert str(exc.value) == f"Field 'i_field' expected a number but got '{v}'."


@pytest.mark.parametrize("v", [10, "abc"])
def test_set_wrong_value_integer_flag(v, db):
    if isinstance(v, int):
        m = MyModel()
        m.if_field = v  # type: ignore
        with pytest.raises(ValidationError) as exc:
            m.save()

        cname = "flag" if sys.version_info >= (3, 11) else "enum"
        assert list(exc.value) == [f"“{v}” must be a subclass of <{cname} 'IntegerFlagEnum'>."]
    else:
        m = MyModel()
        m.if_field = v
        with pytest.raises(ValueError) as exc:  # noqa: PT011
            m.save()

        assert str(exc.value) == f"Field 'if_field' expected a number but got '{v}'."


@pytest.mark.skip(reason="TODO: Fix the aggregation coercion issue.")
def test_aggregate_integer(db):
    MyModel.objects.bulk_create([
        MyModel(),
        MyModel(),
        MyModel(),
    ])
    queryset = MyModel.objects.all()
    assert queryset.aggregate(sum=Sum("i_field")).get("sum", 0) == 3
