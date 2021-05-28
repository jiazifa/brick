import os
import sys
from typing import Dict, List
import click
from brick import plugin_path, config_path, PluginItem

plugins: List[PluginItem] = []

def load_config_if_could(config_path: str) -> Dict[str, str]:
    result: Dict[str, str] = {}
    with open(config_path, mode="r", encoding="utf-8") as f:
        for line in f.readlines():
            items: List[str] = line.split("=")
            if len(items) <= 1: continue
            result.setdefault(items[0], "".join(items[1:]).strip())
    
    result.setdefault("bk.config.path", config_path)
    return result

def register_plugin_item(path: str) -> bool:
    for root, _, file_names in os.walk(path):
        for file_name in file_names:
            file_path: str = os.path.join(root, file_name)
            if file_name == "package.toml":
                item = PluginItem(root, file_path)
                plugins.append(item)
                continue
        break
    return True


def register_plugins():
    p_path: str = plugin_path()
    for root, dir_names, _ in os.walk(p_path, topdown=True):
        if root != p_path: continue
        for dir_name in dir_names:
            p_path_pwd: str = os.path.join(root, dir_name)
            register_plugin_item(p_path_pwd)
        break


@click.group()
def cli():
    pass


def main() -> None:
    global plugins
    register_plugins()
    args = sys.argv
    command = args[1]

    target_plugins = [p for p in plugins if p.name == command]
    if len(target_plugins) > 0:
        c_path = config_path()
        config = load_config_if_could(c_path)
        target_plugins[0].redirect_command(args[2:], config)
    else:
        cli()


if __name__ == "__main__":
    main()