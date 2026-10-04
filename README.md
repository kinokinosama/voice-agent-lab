# 中文语音 Agent 学习项目

目标：用 LiveKit Agents 实现麦克风输入、连续对话、语音回答，再替换为自己的音色。

## 运行方式

Agent 在本机运行，LiveKit Cloud 负责浏览器音频连接及 Inference 模型调用。
这不是完全本地推理；模型调用可能计费。第一轮先使用现成音色。

```text
浏览器麦克风 → LiveKit → STT → LLM → TTS → LiveKit → 浏览器扬声器
```

## 第一步：环境与配置

本项目将包管理器放在 `.tools/uv`，依赖放在 `.venv`，不修改系统 Python。

```bash
cd /home/huang/桌面/codex/voice-agent-lab
./.tools/uv --cache-dir .cache/uv sync --locked
```

在 https://cloud.livekit.io/ 注册并创建项目，将该项目的 URL、API Key、API Secret
填进 `.env.local`。该文件已被 `.gitignore` 排除，不要把密钥发到聊天里。

```bash
./.venv/bin/python check_config.py
```

字段检查通过仅代表填写完整，不代表真实服务已连通。

## 第二步：启动

```bash
./.venv/bin/python src/agent.py dev
```

终端需保持运行。到同一 LiveKit Cloud 项目的 Agent Console，选择或派发
名为 `my-agent` 的 agent，开始会话并允许麦克风。若界面不支持该操作，
后续再配置官方 Playground 或本地前端；不能只凭启动日志判定语音已跑通。

## 第三步：验收

- 听到开场白。
- 说“你好，请用一句话解释什么是 harness”，看到识别文字并听到中文回答。
- 接着说“再说得简单一点”，确认能延续上下文。
- 说话时尝试打断，记录表现与延迟。
- 结束浏览器会话，在终端按 Ctrl+C 停止 agent。

## 修改位置

- `src/agent.py`：人设、语音会话组装、未来添加工具。
- `.env.local`：STT、LLM、TTS 的模型配置和音色 ID。
- 自定义声音需先在所选服务创建音色，确认权限及模型兼容后再替换；不能任意跨服务使用音色 ID。

## 当前验证状态

- 已安装 LiveKit Agents 1.8.4，依赖版本记录在 `uv.lock`。
- `src/agent.py --help` 成功，程序入口和框架导入正常。
- 配置检查器正常工作，目前缺少三个 LiveKit 项目凭据。
- 尚未连接云端，也尚未验证麦克风、扬声器、连续对话或自定义音色。

## 发布到 GitHub

应该提交：`src/`、`pyproject.toml`、`uv.lock`、`check_config.py`、
`.env.example`、`.gitignore` 和本说明。

`.env.local`、`.venv/`、`.tools/`、`.cache/`、录音和日志不提交。
远程仓库：https://github.com/kinokinosama/voice-agent-lab

其他电脑拉取代码后，需要先准备 Python 3.10+ 和 uv。在项目目录运行：

```bash
uv sync --locked
cp .env.example .env.local
# 在编辑器中填写 .env.local 中的三个项目凭据。
uv run --locked python check_config.py
uv run --locked python src/agent.py dev
```

GitHub 保存代码与历史，不能靠上传代码就启动实时语音服务。

## 资料

- https://docs.livekit.io/agents/start/voice-ai/
- https://docs.livekit.io/agents/models/stt/
- https://docs.livekit.io/agents/models/tts/
- https://github.com/livekit/agents
