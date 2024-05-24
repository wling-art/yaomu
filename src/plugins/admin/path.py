from pathlib import Path
from nonebot import get_driver


config_path = Path() / 'admin'
config_config = config_path / 'config'
config_group = config_config / 'group'
config_group_obscenity_group = config_group / 'obscenity_group.json'