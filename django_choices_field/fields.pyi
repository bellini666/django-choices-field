from typing import (
    Any,
    Callable,
    Dict,
    Generic,
    Iterable,
    Optional,
    Tuple,
    Type,
    TypeVar,
    Union,
    overload,
)

from django.db.models import Field, TextChoices

_Choice = Tuple[Any, str]
_ChoiceNamedGroup = Tuple[str, Iterable[_Choice]]
_FieldChoices = Iterable[Union[_Choice, _ChoiceNamedGroup]]
_ValidatorCallable = Callable[..., None]
_ErrorMessagesToOverride = Dict[str, Any]
_C = TypeVar("_C", bound="Optional[TextChoices]")

class ChoicesField(Generic[_C], Field[_C, _C]):
    @overload
    def __new__(
        cls,
        choices_enum: Type[_C],
        verbose_name: Optional[Union[str, bytes]] = ...,
        name: Optional[str] = ...,
        primary_key: bool = ...,
        max_length: Optional[int] = ...,
        unique: bool = ...,
        blank: bool = ...,
        null: Literal[False] = ...,
        db_index: bool = ...,
        default: Any = ...,
        editable: bool = ...,
        auto_created: bool = ...,
        serialize: bool = ...,
        unique_for_date: Optional[str] = ...,
        unique_for_month: Optional[str] = ...,
        unique_for_year: Optional[str] = ...,
        choices: Optional[_FieldChoices] = ...,
        help_text: str = ...,
        db_column: Optional[str] = ...,
        db_tablespace: Optional[str] = ...,
        validators: Iterable[_ValidatorCallable] = ...,
        error_messages: Optional[_ErrorMessagesToOverride] = ...,
    ) -> ChoicesField[_C]: ...
    @overload
    def __new__(
        cls,
        choices_enum: Type[_C],
        verbose_name: Optional[Union[str, bytes]] = ...,
        name: Optional[str] = ...,
        primary_key: bool = ...,
        max_length: Optional[int] = ...,
        unique: bool = ...,
        blank: bool = ...,
        null: Literal[True] = ...,
        db_index: bool = ...,
        default: Any = ...,
        editable: bool = ...,
        auto_created: bool = ...,
        serialize: bool = ...,
        unique_for_date: Optional[str] = ...,
        unique_for_month: Optional[str] = ...,
        unique_for_year: Optional[str] = ...,
        choices: Optional[_FieldChoices] = ...,
        help_text: str = ...,
        db_column: Optional[str] = ...,
        db_tablespace: Optional[str] = ...,
        validators: Iterable[_ValidatorCallable] = ...,
        error_messages: Optional[_ErrorMessagesToOverride] = ...,
    ) -> ChoicesField[Optional[_C]]: ...
    @overload
    def __get__(self: ChoicesField[_C], instance: Any, owner: Any) -> _C: ...
    @overload
    def __get__(self: ChoicesField[Optional[_C]], instance: Any, owner: Any) -> Optional[_C]: ...
    @overload
    def __set__(self, instance: ChoicesField[_C], value: _C) -> None: ...
    @overload
    def __set__(self, instance: ChoicesField[Optional[_C]], value: Optional[_C]) -> None: ...
