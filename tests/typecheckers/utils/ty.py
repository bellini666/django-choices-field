from __future__ import annotations

import os
import pathlib
import re
import subprocess
import tempfile
from typing import cast

from .result import Result, ResultType


def run_ty(code: str, strict: bool = True) -> list[Result]:
    args = [
        "ty",
        "check",
        "--output-format",
        "concise",
        "--ignore",
        "undefined-reveal",
        "--color",
        "never",
    ]

    with tempfile.TemporaryDirectory() as directory:
        module_path = pathlib.Path(directory) / "ty_test.py"
        module_path.write_text(code)

        process_result = subprocess.run(
            [*args, str(module_path)],
            check=False,
            capture_output=True,
            env={
                "PATH": os.environ["PATH"],
            },
        )

        full_output = (
            process_result.stdout.decode("utf-8") + "\n" + process_result.stderr.decode("utf-8")
        )
        full_output = full_output.strip()

        results: list[Result] = []

        pattern = re.compile(r"^.*?:(\d+):(\d+): (error|warning|info)\[[\w-]+\] (.+)$")

        for raw_line in full_output.split("\n"):
            line = raw_line.strip()
            if not line:
                continue

            match = pattern.match(line)
            if match:
                line_num = int(match.group(1))
                col_num = int(match.group(2))
                severity = match.group(3)
                message = match.group(4)

                type_mapping = {
                    "error": "error",
                    "warning": "error",
                    "info": "information",
                }
                result_type = type_mapping.get(severity, "note")

                results.append(
                    Result(
                        type=cast("ResultType", result_type),
                        message=message.strip(),
                        line=line_num,
                        column=col_num,
                    )
                )

        results.sort(key=lambda x: (x.line, x.column, x.message))

        return results
