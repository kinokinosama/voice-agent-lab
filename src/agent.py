"""中文语音入门：STT → LLM → TTS，运行逻辑由 LiveKit Agents 管理。"""

import os
from pathlib import Path

from dotenv import load_dotenv
from livekit.agents import (
    Agent,
    AgentServer,
    AgentSession,
    JobContext,
    TurnHandlingOptions,
    cli,
    inference,
)

ROOT = Path(__file__).resolve().parents[1]
load_dotenv(ROOT / ".env.local")

server = AgentServer()


@server.rtc_session(agent_name=os.getenv("AGENT_NAME", "my-agent"))
async def entrypoint(ctx: JobContext):
    # 三个部件可分别替换。使用 Inference 时共用 LiveKit 项目凭据。
    session = AgentSession(
        stt=inference.STT(
            model=os.getenv("STT_MODEL", "deepgram/nova-3"),
            language=os.getenv("STT_LANGUAGE", "zh"),
        ),
        llm=inference.LLM(model=os.getenv("LLM_MODEL", "google/gemma-4-31b-it")),
        tts=inference.TTS(
            model=os.getenv("TTS_MODEL", "fishaudio/s2.1-pro"),
            voice=os.getenv("TTS_VOICE", "fa4c9eb3dccc4806b382b40d61c6b10a"),
            language=os.getenv("TTS_LANGUAGE", "zh"),
        ),
        turn_handling=TurnHandlingOptions(
            turn_detection=inference.TurnDetector(),
        ),
    )
    await session.start(
        room=ctx.room,
        agent=Agent(
            instructions=(
                "你是一个友好的中文语音助手。默认用普通话回答。"
                "每次回答一到三句，适合直接朗读，不使用 Markdown 或表格。"
                "听不清时请用户重复，不编造用户的话。"
                "这是语音框架学习项目；你没有接入文件、天气或搜索工具，"
                "不要声称已经执行这些操作。"
            ),
        ),
    )
    await ctx.connect()
    await session.generate_reply(instructions="用中文简短打招呼，告诉用户现在可以开始语音对话。")


if __name__ == "__main__":
    cli.run_app(server)
