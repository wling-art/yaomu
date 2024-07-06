import asyncio
from pathlib import Path

import nonebot
from nonebot import get_driver

from .utils import init
from . import obscenity, brush_up

__all__ = ["obscenity", "brush_up"]
global_config = get_driver().config

sub_plugins = nonebot.load_plugins(
    str(Path(__file__).parent.joinpath("plugins").resolve())
)

asyncio.run(init())
