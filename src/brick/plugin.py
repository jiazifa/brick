import os
from typing import Union, Any, Dict, List
from toml import load as toml_load
from brick import execute_command

class PluginItem:
    name: Union[str, None]
    description: Union[str, None]
    version: Union[str, None]
    author: Union[str, None]

    shell_command: Union[str, None]
    executed_file_path: Union[str, None]
    config: Any

    def __init__(self, dir_path: str, toml_path: str) -> None:
        toml_file = toml_load(toml_path)
        self.config = toml_file
        package_dict: Dict[str, Any] = toml_file.get("package") or {}
        self.name = package_dict.get("name")
        self.description = package_dict.get("description")
        self.version = package_dict.get("version")
        self.authors = package_dict.get("authors")

        shell_dict: Dict[str, Any] = toml_file.get("shell") or {}
        self.shell_command = shell_dict.get("command")
        executor_file = shell_dict.get("index")
        if executor_file:
            self.executed_file_path = os.path.join(dir_path, executor_file)

    def redirect_command(self, args: List[str], env: Union[Dict[str, str], None] = None) -> bool:
        command: str = ""
        if env:
            for k in env:
                os.environ.setdefault(k, env.get(k) or "")
        if self.shell_command:
            command += self.shell_command
            command += " "

        if self.executed_file_path:
            command += self.executed_file_path
            command += " "
        command += " ".join(args)

        print(command)
        execute_command(command)
        return True
