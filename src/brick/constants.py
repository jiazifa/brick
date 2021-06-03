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

def config_path() -> str:
    home = home_path()
    p = os.path.join(home, "config")
    return p