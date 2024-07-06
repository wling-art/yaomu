"刷屏检测"

import ujson as json
from nonebot import logger, on_message
from .path import config_data_brush
from nonebot.adapters.onebot.v11 import Bot, GroupMessageEvent
from .utils import isnot_op, is_bot_op
from nonebot.rule import Rule


brush_up = on_message(rule=Rule(is_bot_op, isnot_op), priority=10, block=False)

record_time = 5
record_limit = 3


@brush_up.handle()
async def _(bot: Bot, event: GroupMessageEvent):
    # 记录发言时间
    a1 = await isnot_op(bot, event)
    a2 = await is_bot_op(bot, event)
    logger.info(f"{a1=},{a2=}")
    group_id: int = event.group_id
    user_id: int = event.user_id
    if isinstance(user_id, type(None)):
        logger.error(f"user_id类型错误:{user_id}")
        return False
    with open(config_data_brush, "r") as f:
        brush_dict = json.load(f)
    if str(group_id) not in brush_dict:
        brush_dict[str(group_id)] = {}
    if str(user_id) not in brush_dict[str(group_id)]:
        brush_dict[str(group_id)][str(user_id)] = []
    brush_dict[str(group_id)][str(user_id)].append(event.time)
    # 清理过期时间
    brush_dict[str(group_id)][str(user_id)] = [
        i
        for i in brush_dict[str(group_id)][str(user_id)]
        if i > event.time - record_time
    ]
    with open(config_data_brush, "w") as f:
        json.dump(brush_dict, f)
    # 判断是否刷屏
    if len(brush_dict[str(group_id)][str(user_id)]) > record_limit:
        await bot.set_group_ban(group_id=group_id, user_id=user_id, duration=60)
        await brush_up.finish("刷屏检测，禁言60s")
