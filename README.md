### AI-Desktop-Pet-Local — 你的 AI 桌面小伙伴
 
“她不是工具，是住在你电脑里的小灵魂。”

AI-Desktop-Pet-Local 是一个基于 Electron + FastAPI + DeepSeek V4 的 AI 桌面宠物项目。
她可以听懂你说话（本地语音识别）、记住你的事情（记忆系统）、主动找你聊天（自主意识），还能看屏幕截图（多模态预留接口）。

这个项目受 Vedal / Neuro-sama 启发，但完全由个人独立开发，是一个用于学习、实验和陪伴的 AI 桌宠原型。

### ✨ 功能特性
- 🎤 语音交互（本地识别）

支持两种模式：麦克风常开（实时监听）和 按键说话（长按录音），语音识别由本地 Qwen3-ASR 模型完成，无需联网。

- 🧠 DeepSeek V4 驱动

  使用 DeepSeek V4 作为“大脑”，支持情绪识别、记忆读写、主动发言和角色人设。

- 💾 记忆系统

  短期对话历史 + 长期事实记忆，她会记得你说过的重要事情。

- 🖥️ 桌面透明窗口

  基于 Electron 的透明、置顶、无边框窗口，像真正的“桌面精灵”。

- 🔔 系统通知联动

  切换模式 / 录音状态会通过 Windows 原生通知提示，沉浸感更强。

- 主动意识循环

  闲置一段时间后，她会主动找话题，不会冷场。

- 视觉能力预留

  已预留屏幕截图接口，可接入多模态模型（如 Gemini / Gemma）实现“看图说话”。

### 🛠️ 技术栈

| 模块 | 技术 |
|------|------|
| 前端桌面 |	`Electron + React + Vite`|
| 后端服务 |	`FastAPI + WebSocket` |
| LLM 大脑 |	`DeepSeek V4（兼容 OpenAI 格式）` |
| 语音识别 | `(STT)	Qwen3-ASR-0.6B（本地 ONNX + FunASR）` |
| 语音合成 (TTS) |	`预留接口（支持 Edge TTS / SiliconFlow）` |
| 记忆系统 |	`JSON 本地存储 + 向量检索（预留）` |
| 实时通信 |	`WebSocket（双向）` |
### 📦 快速开始
1. 克隆项
```bash
git clone https://github.com/lanxianxun/AI-Desktop-Pet-Local.git
cd AI-Desktop-Pet-Local
```
3. 后端配置与启动
```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
复制 .env.example 为 .env，填入你的 DeepSeek API Key：

env
LLM_BASE_URL="https://api.deepseek.com/v1"
LLM_API_KEY="sk-你的key"
LLM_MODEL="deepseek-v4-flash"
```
启动后端：

```bash
python main.py
3. 语音模型配置（可选）
本项目使用本地语音识别，首次运行时会自动下载模型（约 1.8GB）：

模型源：魔搭社区 Qwen/Qwen3-ASR-0.6B

缓存路径：~/.cache/modelscope/

如需离线使用，可手动下载模型文件并修改 services.py 中的 model 路径为本地文件夹地址。
```

4. 前端启动
```bash
cd frontend
npm install
npm run dev
```
5. 桌面应用打包
```bash
npm run build
npm run electron
```
### 📁 项目结构
```text
AI-Desktop-Pet-Local/
├── backend/
│   ├── main.py              # FastAPI 主程序
│   ├── services.py          # AI 服务（LLM + STT）
│   ├── memory.py            # 记忆系统
│   ├── tools.py             # 截图等工具
│   └── voice_service.py     # 本地语音识别封装
├── frontend/
│   ├── src/
│   │   ├── components/      # React 组件
│   │   ├── hooks/           # WebSocket / 音频
│   │   └── pages/           # 主界面
│   ├── electron-main.cjs    # Electron 主进程
│   └── package.json
└── README.md
```
### 🎮 交互方式
操作	说明
Alt + T	切换模式（常开 / 按键说话）
Alt + P	按键说话（按住录音，松开发送）
点击 🎤 按钮	手动控制录音开始/停止
文字输入框	支持文字聊天（备用）
### 🙏 致谢
Vedal & Neuro-sama — 给了这个项目最初的灵感和方向

DeepSeek — 提供强大又实惠的 AI 大脑

魔搭社区 (ModelScope) — 提供本地语音模型支持

Electron & FastAPI — 让桌面 AI 应用变得可能

### 🌟 最后
如果你喜欢这个项目，欢迎 ⭐ Star，也欢迎 Fork 和 PR。
如果你有好的想法或建议，可以提 Issue，或者直接邮件联系我（联系方式见 GitHub Profile）。

“她不是完美的，但她是我亲手创造的。”
