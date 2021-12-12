from typing import (
    Any,
    Callable,
    Dict,
    Generic,
    Iterable,
    Literal,
    Optional,
    Tuple,
    Type,
    TypeVar,
    Union,
    overload,
)

from django.db.models import Field, IntegerChoices, TextChoices

_Choice = Tuple[Any, str]
_ChoiceNamedGroup = Tuple[str, Iterable[_Choice]]
_FieldChoices = Iterable[Union[_Choice, _ChoiceNamedGroup]]
_ValidatorCallable = Callable[..., None]
_ErrorMessagesToOverride = Dict[str, Any]

_C = TypeVar("_C", bound="Optional[TextChoices]")

class TextChoicesField(Generic[_C], Field[_C, _C]):
    choices_enum: Type[_C]
    @overload
    def __init__(
        self: TextChoicesField[_C],
        choices_enum: Type[_C],
        verbose_name: Optional[str] = ...,
        name: Optional[str] = ...,
        primary_key: bool = ...,
        max_length: Optional[int] = ...,
        unique: bool = ...,
        blank: bool = ...,
        null: Literal[False] = ...,
        db_index: bool = ...,
        default: Union[_C, Callable[[], _C]] = ...,
        editable: bool = ...,
        auto_created: bool = ...,
        serialize: bool = ...,
        unique_for_date: Optional[str] = ...,
        unique_for_month: Optional[str] = ...,
        unique_for_year: Optional[str] = ...,
        help_text: str = ...,
        db_column: Optional[str] = ...,
        db_tablespace: Optional[str] = ...,
        validators: Iterable[_ValidatorCallable] = ...,
        error_messages: Optional[_ErrorMessagesToOverride] = ...,
        path: Union[str, Callable[..., str]] = ...,
        match: Optional[str] = ...,
        recursive: bool = ...,
        allow_files: bool = ...,
        allow_folders: bool = ...,
    ) -> None: ...
    @overload
    def __init__(
        self: TextChoicesField[Optional[_C]],
        choices_enum: Type[_C],
        verbose_name: Optional[str] = ...,
        name: Optional[str] = ...,
        primary_key: bool = ...,
        max_length: Optional[int] = ...,
        unique: bool = ...,
        blank: bool = ...,
        null: Literal[True] = ...,
        db_index: bool = ...,
        default: Optional[Union[_C, Callable[[], _C]]] = ...,
        editable: bool = ...,
        auto_created: bool = ...,
        serialize: bool = ...,
        unique_for_date: Optional[str] = ...,
        unique_for_month: Optional[str] = ...,
        unique_for_year: Optional[str] = ...,
        help_text: str = ...,
        db_column: Optional[str] = ...,
        db_tablespace: Optional[str] = ...,
        validators: Iterable[_ValidatorCallable] = ...,
        error_messages: Optional[_ErrorMessagesToOverride] = ...,
        path: Union[str, Callable[..., str]] = ...,
        match: Optional[str] = ...,
        recursive: bool = ...,
        allow_files: bool = ...,
        allow_folders: bool = ...,
    ) -> None: ...
    @overload
    def __new__(
        cls,
        choices_enum: Type[_C],
        *args: Any,
        null: Literal[False] = ...,
        **kwargs: Any,
    ) -> TextChoicesField[_C]: ...
    @overload
    def __new__(
        cls,
        choices_enum: Type[_C],
        *args: Any,
        null: Literal[True],
        **kwargs: Any,
    ) -> TextChoicesField[Optional[_C]]: ...

_I = TypeVar("_I", bound="Optional[IntegerChoices]")

class IntegerChoicesField(Generic[_I], Field[_I, _I]):
    choices_enum: Type[_I]
    @overload
    def __init__(
        self: IntegerChoicesField[_I],
        choices_enum: Type[_I],
        verbose_name: Optional[str] = ...,
        name: Optional[str] = ...,
        primary_key: bool = ...,
        max_length: Optional[int] = ...,
        unique: bool = ...,
        blank: bool = ...,
        null: Literal[False] = ...,
        db_index: bool = ...,
        default: Union[_I, Callable[[], _I]] = ...,
        editable: bool = ...,
        auto_created: bool = ...,
        serialize: bool = ...,
        unique_for_date: Optional[str] = ...,
        unique_for_month: Optional[str] = ...,
        unique_for_year: Optional[str] = ...,
        help_text: str = ...,
        db_column: Optional[str] = ...,
        db_tablespace: Optional[str] = ...,
        validators: Iterable[_ValidatorCallable] = ...,
        error_messages: Optional[_ErrorMessagesToOverride] = ...,
        path: Union[str, Callable[..., str]] = ...,
        match: Optional[str] = ...,
        recursive: bool = ...,
        allow_files: bool = ...,
        allow_folders: bool = ...,
    ) -> None: ...
    @overload
    def __init__(
        self: IntegerChoicesField[Optional[_I]],
        choices_enum: Type[_I],
        verbose_name: Optional[str] = ...,
        name: Optional[str] = ...,
        primary_key: bool = ...,
        max_length: Optional[int] = ...,
        unique: bool = ...,
        blank: bool = ...,
        null: Literal[True] = ...,
        db_index: bool = ...,
        default: Optional[Union[_I, Callable[[], _I]]] = ...,
        editable: bool = ...,
        auto_created: bool = ...,
        serialize: bool = ...,
        unique_for_date: Optional[str] = ...,
        unique_for_month: Optional[str] = ...,
        unique_for_year: Optional[str] = ...,
        help_text: str = ...,
        db_column: Optional[str] = ...,
        db_tablespace: Optional[str] = ...,
        validators: Iterable[_ValidatorCallable] = ...,
        error_messages: Optional[_ErrorMessagesToOverride] = ...,
        path: Union[str, Callable[..., str]] = ...,
        match: Optional[str] = ...,
        recursive: bool = ...,
        allow_files: bool = ...,
        allow_folders: bool = ...,
    ) -> None: ...
    @overload
    def __new__(
        cls,
        choices_enum: Type[_I],
        *args: Any,
        null: Literal[False] = ...,
        **kwargs: Any,
    ) -> IntegerChoicesField[_I]: ...
    @overload
    def __new__(
        cls,
        choices_enum: Type[_I],
        *args: Any,
        null: Literal[True],
        **kwargs: Any,
    ) -> IntegerChoicesField[Optional[_I]]: ...
