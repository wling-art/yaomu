import os

import nonebot
from .path import config_path,config_group_obscenity_group
from nonebot.adapters.onebot.v11 import Bot, GroupMessageEvent
from nonebot import logger
async def init():
    "初始化插件"
    config_path.mkdir(parents=True, exist_ok=True)
    # 检测是否有这个文件，没有就创建
    if not os.path.exists(config_group_obscenity_group):
        with open(config_group_obscenity_group, 'w') as f:
            f.write('{}')



async def isnot_op(bot: Bot, event: GroupMessageEvent) -> bool:
    # 判断是否是管理员
    group_id: int = event.group_id
    user_id = event.sender.user_id
    if isinstance(user_id, type(None)):
        logger.error(f"user_id类型错误:{user_id}")
        return False
    member_info = await bot.get_group_member_info(group_id=group_id, user_id=user_id)
    return member_info.get('role') not in ['owner', 'admin']


# 判断机器人是否为管理
async def is_bot_op(bot: Bot, event: GroupMessageEvent) -> bool:
    # 判断是否是管理员
    group_id: int = event.group_id
    user_id = event.self_id
    if isinstance(user_id, type(None)):
        logger.error(f"user_id类型错误:{user_id}")
        return False
    member_info = await bot.get_group_member_info(group_id=group_id, user_id=user_id)
    return member_info.get('role') in ['owner', 'admin']