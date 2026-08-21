import asyncio
import json
import time
import datetime
import random
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from services import AIService
from memory import MemorySystem
from tools import ToolBox
app = FastAPI()

class NeuroBrain:
    def __init__(self):
        # 状态机
        self.state = "idle"          # idle, thinking, speaking
        self.last_interaction = time.time() #自己上次发言的时间
        self.last_user_input_time = time.time()  # 专门记录用户上次理我是什么时候
        self.boredom_threshold = 40  # 40秒无操作触发主动发言
        self.is_dnd_mode = False     # 勿扰模式
        self.current_threshold = 40              # 当前的等待阈值（会变大）
        self.max_threshold = 3600                # 上限（比如1小时）
        self.memory = MemorySystem()
        self.history = []            # 短期对话历史 (滑动窗口)

    def update_activity(self):

        self.last_interaction = time.time()
    def reset_boredom_time(self):
        self.last_user_input_time=time.time()
        self.current_threshold=self.boredom_threshold
        self.update_activity()
    def increase_boredom_time(self):
        self.current_threshold=self.current_threshold*2
        if(self.current_threshold>self.max_threshold):
            self.current_threshold=self.max_threshold
        print(f"下次主动对话将在{self.current_threshold}s后进行")

    async def build_system_prompt(self,user_input:str=None):
        now_str = datetime.datetime.now().strftime("%Y年%m月%d日 %H:%M")
        known_facts = self.memory.get_fact_context()
        longmemory=await self.memory.get_longmemory_context(user_input)

        return {
            "role": "system",
            "content": f"""
            你叫 Neuro，一个可爱毒舌的 AI 桌宠。
            当前时间: {now_str}。
            
            【记忆权限已授权】
            已知用户事实: {known_facts}
            {longmemory}
            请针对用户的输入，返回一个 JSON 对象（严格遵守 JSON 格式）：
            {{
                "thought": "内心独白。分析用户意图，检查是否与已知事实冲突。",
                "reply": "给用户的回复。口语化，符合人设。",
                "emotion": "happy/neutral/bored/angry",
                "memory_operation": {{
                    "new_facts": {{ "key": "value" }} 或 null, 
                    "new_episode": "事件摘要" 或 null,
                    "is_silence_requested": true/false
                }}
            }}
            
            规则：
            1. 除非用户明确陈述新的事实，否则不要瞎编 `new_facts`。
            2. 如果用户说胡话（如我是秦始皇），在 reply 里拆穿，不要更新记忆。
            """
        }

brain = NeuroBrain()

# === WebSocket 路由 ===
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    print("⚡ 连接建立")
    
    # 定义发送助手
    async def send_to_frontend(type_str, payload):
        try:
            # 检查连接状态
            if not hasattr(websocket, 'client_state') or websocket.client_state.name != "CONNECTED":
                print(f"⚠️ WebSocket 已断开 ({websocket.client_state.name if hasattr(websocket, 'client_state') else 'unknown'})，无法发送: {type_str}")
                return
            await websocket.send_json({"type": type_str, "payload": payload})
            print(f"📤 已发送: {type_str}")
        except Exception as e:
            print(f"❌ 发送消息失败 ({type_str}): {e}")
            # 不要 raise，避免主循环崩溃

    # 启动主动意识循环 (后台任务)
    loop_task = asyncio.create_task(game_loop(websocket, send_to_frontend))

    try:
        while True:
            data = await websocket.receive_text()
            packet = json.loads(data)
            
            # 收到消息第一件事：刷新活跃时间
            brain.update_activity()

            if packet["type"] == "text_input":
                text = packet["payload"]["text"]
                # 把发送函数传进去
                await handle_user_input(text, send_to_frontend)

            elif packet["type"] == "audio_input":
                # 语音 -> 文字
                audio_b64 = packet["payload"]["audio_base64"]
                text = await AIService.speech_to_text_local(audio_b64)
                if text:
                    # 回显给前端看
                    await send_to_frontend("text_input", {"text": text})
                    await handle_user_input(text, send_to_frontend)

            elif packet["type"] == "interrupt":
                print("🛑 用户打断")
                brain.state = "idle"
                # 这里不处理逻辑，单纯重置状态，等待下一次输入

    except WebSocketDisconnect:
        print("🔌 连接断开")
        loop_task.cancel()
    except Exception as e:
        print(f"❌ Main Loop Error: {e}")

# === 核心逻辑 ===

async def handle_user_input(text: str, send_func):
    """处理用户输入的主流程"""
    brain.state = "thinking"
    await send_func("state_update", {"state": "thinking"})
    brain.reset_boredom_time()
    user_time_str = datetime.datetime.now().strftime("[%H:%M:%S]")
    current_image_b64 = None
    vision_keywords = ["看看", "截图", "什么样", "屏幕", "image", "photo"]
    if any(k in text for k in vision_keywords):
        print("📸 检测到视觉关键词，正在截图...")
        current_image_b64 = ToolBox.capture_screen_base64()
    try:
       
        sys_prompt = await brain.build_system_prompt(text)
        current_msg_block = {
            "role": "user", 
            "content": f"{user_time_str} {text}"
        }
        
   
        if current_image_b64:
             current_msg_block["content"] += "\n(系统附图：当前屏幕截图)"

        messages = [sys_prompt] + brain.history + [current_msg_block]
        
        
        print("🧠 主脑思考中...")
        result_json = await AIService.chat_with_neuro_brain(messages, image_base64=current_image_b64)
        
     
        reply = result_json.get("reply", "（发呆中...）")
        emotion = result_json.get("emotion", "neutral")
        mem_op = result_json.get("memory_operation", {})
        thought = result_json.get("thought", "无想法")
        
        print(f"💭 {thought}")

        # 记忆更新
        if mem_op:
            await brain.memory.execute_updates(mem_op)
            if mem_op.get("is_silence_requested"):
                brain.is_dnd_mode = True
                print("🔕 进入勿扰模式")

        if brain.is_dnd_mode and not mem_op.get("is_silence_requested"):
            # 如果用户主动说话，自动解除勿扰
            brain.is_dnd_mode = False

        # 更新历史
        if current_image_b64:
            text += " [已发送截图]"
        ai_time_str = datetime.datetime.now().strftime("[%H:%M:%S]")
        brain.history.append({
            "role": "user", 
            "content": f"{user_time_str} {text}" 
        })
        
        
        if reply:
            brain.history.append({
                "role": "assistant", 
                "content": f"{ai_time_str} {reply}"
            })
            
        brain.history = brain.history[-10:] # 滑动窗口

        # 说话
        await send_reply(reply, emotion, send_func)

    except Exception as e:
        print(f"❌ Handle Error: {e}")
        await send_func("state_update", {"state": "idle"})
    finally:
        brain.state = "idle"
        brain.update_activity()

async def send_reply(text: str, emotion: str, send_func):
    # 更新状态
    brain.state = "speaking"
    estimated_duration = (len(text) * 0.8) + 1.0
    brain.last_interact = time.time()  # 记录当前时间
    brain.last_interact_duration = estimated_duration  # 新增一个属性

    # --- 核心修改：尝试合成语音，失败则只发文本 ---
    audio_b64 = None
    try:
        # 只在语音客户端存在时尝试合成
        if AIService.client_audio is not None:
            audio_b64 = await AIService.text_to_speech(text, emotion)
        else:
            print("语音服务未配置，跳过语音合成")
    except Exception as e:
        print(f"语音合成失败: {e}，将继续发送文字")

    # 发送消息（无论是否有音频）
    await send_func("audio_chunk", {
        "text": text,
        "audio_base64": audio_b64,  # 如果为 None，前端应该只显示文字
        "expression": emotion
    })

async def game_loop(ws, send_func):
    """自主意识循环"""
    print("🔄 自主意识启动")

    while True:
        await asyncio.sleep(1)
        now = time.time()
        
        if (not brain.is_dnd_mode) and \
           (brain.state == "idle") and \
           (now - brain.last_interaction > brain.boredom_threshold):
            
            print("🥱 触发主动发言")
            brain.increase_boredom_time()
            brain.state = "thinking"
            await send_func("state_update", {"state": "thinking"})
            brain.update_activity() 
            
            try:
                sys_prompt = await brain.build_system_prompt() 
                last_active_str = datetime.datetime.fromtimestamp(brain.last_user_input_time).strftime("%H:%M:%S")
                trigger_content = f"""
                (系统自动触发指令：
                1. 用户当前处于静默状态。
                2. 用户最后一次发言时间是：{last_active_str}。
                3. 请对比【当前系统时间】与【最后发言时间】：
                   - 如果时间差很短（连续对话）：请顺着上文继续聊，不要打断话题。或者如果当前话题无聊，可以主动找话题
                   - 如果时间差很长（长久冷落）：可以参考【记忆信息】里的随机往事，或者吐槽太安静了，或者主动找话题聊天。
                
                必须返回 JSON。)
                """

                msgs = [sys_prompt] + brain.history + [{
                    "role": "user", 
                    "content": trigger_content
                }]
                
                # 调用主脑
                print("🧠 主脑主动思考中...")
                result_json = await AIService.chat_with_neuro_brain(msgs)
                
                reply = result_json.get("reply")
                emotion = result_json.get("emotion", "neutral")
                
                if reply:
                    print(f"💡 主动生成: {reply}")
                    
                
                    ai_time_str = datetime.datetime.now().strftime("[%H:%M:%S]")
                    
                    brain.history.append({
                        "role": "assistant", 
                        "content": f"{ai_time_str} {reply}"
                    })
                 
                    brain.history = brain.history[-10:] 
                    # ==========================================

                    await send_reply(reply, emotion, send_func)
                    brain.state = "idle"
                    await send_func("state_update", {"state": "idle"})
                else:
                    print("⚠️ 主动发言生成了空内容")
                    brain.state = "idle"
                    await send_func("state_update", {"state": "idle"})

            except Exception as e:
                print(f"❌ 主动发言失败: {e}")
                brain.state = "idle"
                await send_func("state_update", {"state": "idle"})
if __name__ == "__main__":
    import uvicorn
    # 启动服务器，监听 8000 端口
    uvicorn.run(app, host="0.0.0.0", port=8000)