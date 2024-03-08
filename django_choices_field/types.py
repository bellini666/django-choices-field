import enum
import sys
from typing import TYPE_CHECKING

from django.db import models
from typing_extensions import Self


class IntegerChoicesFlag(models.IntegerChoices, enum.Flag):
    """Enumerated integer choices."""

    if TYPE_CHECKING:

        def __or__(self, other: Self) -> Self: ...

        def __and__(self, other: Self) -> Self: ...

        def __xor__(self, other: Self) -> Self: ...

        def __invert__(self) -> Self: ...

        if sys.version_info >= (3, 11):
            __ror__ = __or__
            __rand__ = __and__
            __rxor__ = __xor__
