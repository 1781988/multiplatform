from .bilibili_adapter import BilibiliAdapter
from .wechat_adapter import WeChatAdapter
from .xiaohongshu_adapter import XiaohongshuAdapter
from .zhihu_adapter import ZhihuAdapter

ADAPTER_REGISTRY = {
    "wechat": WeChatAdapter(),
    "zhihu": ZhihuAdapter(),
    "bilibili": BilibiliAdapter(),
    "xiaohongshu": XiaohongshuAdapter(),
}
