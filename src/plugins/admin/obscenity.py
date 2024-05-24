import re
import json
from nonebot import logger, on_command, on_message
from nonebot.adapters.onebot.v11.exception import ActionFailed
from nonebot.adapters.onebot.v11 import Bot, GroupMessageEvent
from nonebot.adapters.onebot.v11.permission import GROUP_ADMIN, GROUP_OWNER
from nonebot.permission import SUPERUSER
from .utils import isnot_op, is_bot_op
from .path import config_path, config_group_obscenity_group

removeObscenityWord = on_command('违禁词删除', priority=10, block=True,
                            permission=GROUP_ADMIN | GROUP_OWNER | SUPERUSER)
addObscenityWord = on_command('违禁词添加', priority=10, block=True,
                         permission=GROUP_ADMIN | GROUP_OWNER | SUPERUSER)
f_word = on_message(rule=isnot_op and is_bot_op, priority=20, block=False)

@addObscenityWord.handle()
async def _(event: GroupMessageEvent):
    "违禁词添加"
    str_key: str = event.get_plaintext().strip().replace('违禁词添加', '').lower()
    with open(config_group_obscenity_group, 'r') as f:
        obs_dict: dict = json.load(f)
    group_id: int = event.group_id
    if str(group_id) not in obs_dict:
        with open(config_path/'res'/'obscenity.json', 'r') as f:
            obs_dict[str(group_id)] = json.load(f)
    obs_dict[str(group_id)].append(str_key)
    with open(config_group_obscenity_group, 'w') as f:
        json.dump(obs_dict, f)
    await addObscenityWord.finish(f'添加成功:{str_key}')


@removeObscenityWord.handle()
async def _(event: GroupMessageEvent):
    "违禁词删除"
    str_key: str = event.get_plaintext().strip().replace('违禁词删除', '').lower()
    with open(config_group_obscenity_group, 'r') as f:
        obs_dict: dict = json.load(f)
    group_id: int = event.group_id
    if str(group_id) not in obs_dict:
        with open(config_path/'res'/'obscenity.json', 'r') as f:
            obs_dict[str(group_id)] = json.load(f)
    #删关键词，如果没有就不删
    try:
        obs_dict[str(group_id)].remove(str_key)
    except ValueError:
        await removeObscenityWord.finish(f'未找到关键词:{str_key}')
    with open(config_group_obscenity_group, 'w') as f:
        json.dump(obs_dict, f)
    await removeObscenityWord.finish(f'删除成功:{str_key}')


@f_word.handle()
async def _(bot: Bot, event: GroupMessageEvent):
    # 读取群组的敏感词
    group_id: int = event.group_id
    # 读取群组的敏感词，没有创建字典
    with open(config_group_obscenity_group, 'r') as f:
        obs_dict = json.load(f)
    if str(group_id) not in obs_dict:
        with open(config_path/'res'/'obscenity.json', 'r') as f:
            obs_dict[str(group_id)] = json.load(f)
        with open(config_group_obscenity_group, 'w') as f:
            json.dump(obs_dict, f)
    # 生成re正则,匹配敏感词
    obs_list = obs_dict[str(group_id)]
    obs_re = '|'.join(obs_list)
    # 匹配敏感词
    sender: int | None = event.sender.user_id
    if isinstance(sender, type(None)):
        logger.error(f"sender类型错误:{sender}")
        return
    if re.search(obs_re, event.message.extract_plain_text()):
        try:
            await bot.set_group_ban(group_id=group_id, user_id=sender, duration=60)
            await bot.delete_msg(message_id=event.message_id)
        except ActionFailed as e:
            logger.error(f"禁言失败:{e}")
        else:
            logger.info(f"禁言{event.sender.nickname}成功")
            await f_word.finish(f'检测到敏感词，已撤回，已禁言"{event.sender.nickname}" 60s')
