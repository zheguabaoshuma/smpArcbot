from .Matcher import arc
from .ArcbotHandler.handler import songinfo_handler
from .ArcbotHandler.handler import b30r10_handler
from .ArcbotHandler.handler import bind_handler
from .ArcbotHandler.handler import lookuphandler
from nonebot import logger
from nonebot.typing import T_State


arc.handle()(songinfo_handler)
arc.handle()(bind_handler)
arc.handle()(b30r10_handler)
arc.handle()(lookuphandler)
