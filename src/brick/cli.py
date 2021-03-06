import os
import sys
import json
from typing import Dict, List
import click
from brick import plugin_path, config_path_at_current_dir, config_path_at_home, alert_toast, error_toast, config_path_at_current_dir
from .plugin import PluginItem

plugins: List[PluginItem] = []

def load_config_if_could(config_path: str) -> Dict[str, str]:
    result: Dict[str, str] = {}
    if not os.path.exists(config_path):
        return result
    with open(config_path, mode="r", encoding="utf-8") as f:
        result = json.load(f)
    
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


def perpare_env() -> Dict[str, str]:
    # 准备环境变量，只负责读取规则内的文件变量
    curdir: str =  os.getcwd()
    splited: List[str] = curdir.split(os.sep)
    path: str = "/"
    config_dic: Dict[str, str] = {}
    for folder in splited:
        path = os.path.join(path, folder)
        config_path: str = config_path_at_current_dir(path)
        temp: Dict[str, str] = load_config_if_could(config_path)
        config_dic.update(temp)
    return config_dic
    

def echo_help():
    info: str = ""
    info += """
Brick Command Tool

目前可用插件：
    """
    for plugin in plugins:
        info += "\n"
        info += "\t".join([plugin.name or "", plugin.description or ""])
        info += "\n"
    alert_toast(info)

@click.group()
def cli():
    pass


def main() -> None:
    global plugins
    
    register_plugins()
    args = sys.argv
    if len(args) <= 1:
        echo_help()
        return
    command = args[1]
    target_plugins = [p for p in plugins if p.name == command]
    if len(target_plugins) == 0:
        cli()
        return
        
    # 优先加载本地配置
    config: Dict[str, str] = {}
    h_path = config_path_at_home()
    # 全局配置兜底
    config.update(load_config_if_could(h_path))
    cur_env = perpare_env()
    config.update(cur_env)
    target_plugins[0].redirect_command(args[2:], config)


if __name__ == "__main__":
    main()