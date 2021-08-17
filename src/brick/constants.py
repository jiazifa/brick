import os
from typing import Union

def home_path() -> str:
    home: Union[str, None] = os.environ.get("HOME")
    if not home:
        return ''
    app_home = os.path.join(home, '.brick')
    return app_home


def plugin_path() -> str:
    home = home_path()
    plugin_path = os.path.join(home, 'plugins')
    return plugin_path

def hooks_path() -> str:
    home = home_path()
    p = os.path.join(home, "hooks")
    return p

def config_path_at_home() -> str:
    home = home_path()
    p = os.path.join(home, ".bk_config")
    return p

def config_path_at_current_dir(path: str) -> str:
    p = os.path.join(path, ".bk_config")
    return p