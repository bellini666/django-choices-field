from __future__ import annotations

import concurrent.futures
import shutil
from dataclasses import dataclass

import pytest

from .mypy import run_mypy
from .pyright import run_pyright
from .result import Result
from .ty import run_ty

__all__ = [
    "Result",
    "TypecheckResult",
    "requires_mypy",
    "requires_pyright",
    "requires_ty",
    "typecheck",
]


def pyright_exist() -> bool:
    return shutil.which("pyright") is not None


def mypy_exists() -> bool:
    return shutil.which("mypy") is not None


def ty_exists() -> bool:
    return shutil.which("ty") is not None


requires_pyright = pytest.mark.skipif(
    not pyright_exist(),
    reason="These tests require pyright",
)

requires_mypy = pytest.mark.skipif(
    not mypy_exists(),
    reason="These tests require mypy",
)

requires_ty = pytest.mark.skipif(
    not ty_exists(),
    reason="These tests require ty",
)


@dataclass
class TypecheckResult:
    pyright: list[Result]
    mypy: list[Result]
    ty: list[Result]


def typecheck(code: str, strict: bool = True) -> TypecheckResult:
    with concurrent.futures.ThreadPoolExecutor() as executor:
        pyright_future = executor.submit(run_pyright, code, strict=strict)
        mypy_future = executor.submit(run_mypy, code, strict=strict)
        ty_future = executor.submit(run_ty, code, strict=strict)

        pyright_results = pyright_future.result()
        mypy_results = mypy_future.result()
        ty_results = ty_future.result()

    return TypecheckResult(pyright=pyright_results, mypy=mypy_results, ty=ty_results)
