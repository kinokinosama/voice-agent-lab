"""只报告配置是否齐全，不打印凭据，也不调用付费服务。"""

from pathlib import Path
from importlib.metadata import version
from urllib.parse import urlparse

from dotenv import dotenv_values

root = Path(__file__).resolve().parent
config = dotenv_values(root / ".env.local")
print("LiveKit Agents:", version("livekit-agents"))
missing = [k for k in ("LIVEKIT_URL", "LIVEKIT_API_KEY", "LIVEKIT_API_SECRET") if not config.get(k)]
if missing:
    print("尚未填写：", ", ".join(missing))
    raise SystemExit(1)
url = urlparse(config["LIVEKIT_URL"])
if url.scheme != "wss" or not url.hostname:
    print("LIVEKIT_URL 应是项目提供的 wss:// 地址。")
    raise SystemExit(1)
print("配置字段完整；尚未验证凭据有效性、额度、联网或麦克风。")
