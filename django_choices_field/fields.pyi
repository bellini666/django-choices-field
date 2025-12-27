from collections.abc import Callable, Iterable
from typing import (
    Any,
    Generic,
    Literal,
    TypeAlias,
    TypeVar,
    overload,
)

from django.db.models import Field, IntegerChoices, TextChoices
from django.utils.functional import Promise

from django_choices_field.types import IntegerChoicesFlag

StrOrPromise: TypeAlias = str | Promise

_ValidatorCallable: TypeAlias = Callable[..., None]
_ErrorMessagesToOverride: TypeAlias = dict[str, Any]

_C = TypeVar("_C", bound=TextChoices | None)

class TextChoicesField(Field[_C, _C], Generic[_C]):
    choices_enum: type[_C]
    @overload
    def __new__(
        cls,
        choices_enum: type[_C],
        verbose_name: StrOrPromise | None = ...,
        name: str | None = ...,
        primary_key: bool = ...,
        max_length: int | None = ...,
        unique: bool = ...,
        blank: bool = ...,
        null: Literal[False] = ...,
        db_index: bool = ...,
        default: _C | Callable[[], _C] = ...,
        editable: bool = ...,
        auto_created: bool = ...,
        serialize: bool = ...,
        unique_for_date: str | None = ...,
        unique_for_month: str | None = ...,
        unique_for_year: str | None = ...,
        help_text: StrOrPromise = ...,
        db_column: str | None = ...,
        db_tablespace: str | None = ...,
        validators: Iterable[_ValidatorCallable] = ...,
        error_messages: _ErrorMessagesToOverride | None = ...,
        path: str | Callable[..., str] = ...,
        match: str | None = ...,
        recursive: bool = ...,
        allow_files: bool = ...,
        allow_folders: bool = ...,
    ) -> TextChoicesField[_C]: ...
    @overload
    def __new__(
        cls,
        choices_enum: type[_C],
        verbose_name: StrOrPromise | None = ...,
        name: str | None = ...,
        primary_key: bool = ...,
        max_length: int | None = ...,
        unique: bool = ...,
        blank: bool = ...,
        null: Literal[True] = ...,
        db_index: bool = ...,
        default: _C | Callable[[], _C] | None = ...,
        editable: bool = ...,
        auto_created: bool = ...,
        serialize: bool = ...,
        unique_for_date: str | None = ...,
        unique_for_month: str | None = ...,
        unique_for_year: str | None = ...,
        help_text: StrOrPromise = ...,
        db_column: str | None = ...,
        db_tablespace: str | None = ...,
        validators: Iterable[_ValidatorCallable] = ...,
        error_messages: _ErrorMessagesToOverride | None = ...,
        path: str | Callable[..., str] = ...,
        match: str | None = ...,
        recursive: bool = ...,
        allow_files: bool = ...,
        allow_folders: bool = ...,
    ) -> TextChoicesField[_C | None]: ...

_I = TypeVar("_I", bound=IntegerChoices | None)

class IntegerChoicesField(Field[_I, _I], Generic[_I]):
    choices_enum: type[_I]
    @overload
    def __new__(
        cls,
        choices_enum: type[_I],
        verbose_name: StrOrPromise | None = ...,
        name: str | None = ...,
        primary_key: bool = ...,
        max_length: int | None = ...,
        unique: bool = ...,
        blank: bool = ...,
        null: Literal[False] = ...,
        db_index: bool = ...,
        default: _I | Callable[[], _I] = ...,
        editable: bool = ...,
        auto_created: bool = ...,
        serialize: bool = ...,
        unique_for_date: str | None = ...,
        unique_for_month: str | None = ...,
        unique_for_year: str | None = ...,
        help_text: StrOrPromise = ...,
        db_column: str | None = ...,
        db_tablespace: str | None = ...,
        validators: Iterable[_ValidatorCallable] = ...,
        error_messages: _ErrorMessagesToOverride | None = ...,
        path: str | Callable[..., str] = ...,
        match: str | None = ...,
        recursive: bool = ...,
        allow_files: bool = ...,
        allow_folders: bool = ...,
    ) -> IntegerChoicesField[_I]: ...
    @overload
    def __new__(
        cls,
        choices_enum: type[_I],
        verbose_name: StrOrPromise | None = ...,
        name: str | None = ...,
        primary_key: bool = ...,
        max_length: int | None = ...,
        unique: bool = ...,
        blank: bool = ...,
        null: Literal[True] = ...,
        db_index: bool = ...,
        default: _I | Callable[[], _I] | None = ...,
        editable: bool = ...,
        auto_created: bool = ...,
        serialize: bool = ...,
        unique_for_date: str | None = ...,
        unique_for_month: str | None = ...,
        unique_for_year: str | None = ...,
        help_text: StrOrPromise = ...,
        db_column: str | None = ...,
        db_tablespace: str | None = ...,
        validators: Iterable[_ValidatorCallable] = ...,
        error_messages: _ErrorMessagesToOverride | None = ...,
        path: str | Callable[..., str] = ...,
        match: str | None = ...,
        recursive: bool = ...,
        allow_files: bool = ...,
        allow_folders: bool = ...,
    ) -> IntegerChoicesField[_I | None]: ...

_IF = TypeVar("_IF", bound=IntegerChoicesFlag | None)

class IntegerChoicesFlagField(Field[_IF, _IF], Generic[_IF]):
    choices_enum: type[_IF]
    @overload
    def __new__(
        cls,
        choices_enum: type[_IF],
        verbose_name: StrOrPromise | None = ...,
        name: str | None = ...,
        primary_key: bool = ...,
        max_length: int | None = ...,
        unique: bool = ...,
        blank: bool = ...,
        null: Literal[False] = ...,
        db_index: bool = ...,
        default: _IF | Callable[[], _IF] = ...,
        editable: bool = ...,
        auto_created: bool = ...,
        serialize: bool = ...,
        unique_for_date: str | None = ...,
        unique_for_month: str | None = ...,
        unique_for_year: str | None = ...,
        help_text: StrOrPromise = ...,
        db_column: str | None = ...,
        db_tablespace: str | None = ...,
        validators: Iterable[_ValidatorCallable] = ...,
        error_messages: _ErrorMessagesToOverride | None = ...,
        path: str | Callable[..., str] = ...,
        match: str | None = ...,
        recursive: bool = ...,
        allow_files: bool = ...,
        allow_folders: bool = ...,
    ) -> IntegerChoicesFlagField[_IF]: ...
    @overload
    def __new__(
        cls,
        choices_enum: type[_IF],
        verbose_name: StrOrPromise | None = ...,
        name: str | None = ...,
        primary_key: bool = ...,
        max_length: int | None = ...,
        unique: bool = ...,
        blank: bool = ...,
        null: Literal[True] = ...,
        db_index: bool = ...,
        default: _IF | Callable[[], _IF] | None = ...,
        editable: bool = ...,
        auto_created: bool = ...,
        serialize: bool = ...,
        unique_for_date: str | None = ...,
        unique_for_month: str | None = ...,
        unique_for_year: str | None = ...,
        help_text: StrOrPromise = ...,
        db_column: str | None = ...,
        db_tablespace: str | None = ...,
        validators: Iterable[_ValidatorCallable] = ...,
        error_messages: _ErrorMessagesToOverride | None = ...,
        path: str | Callable[..., str] = ...,
        match: str | None = ...,
        recursive: bool = ...,
        allow_files: bool = ...,
        allow_folders: bool = ...,
    ) -> IntegerChoicesFlagField[_IF | None]: ...
