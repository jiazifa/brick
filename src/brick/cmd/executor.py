import os
import subprocess
from typing import List


def execute_command(command: str) -> int:
    return os.system(command)


def execute_want_one_line(command: str) -> str:
    r = execute_want_return_value(command)
    return r[0]


def execute_want_return_value(command: str) -> List[str]:
    res = subprocess.Popen(command,
                           shell=True,
                           stdout=subprocess.PIPE,
                           stderr=subprocess.PIPE,
                           close_fds=True)
    out = res.stdout
    if not out:
        return []
    result = out.readlines()
    return list(map(lambda r: str(r, encoding="utf-8").strip(), result))
