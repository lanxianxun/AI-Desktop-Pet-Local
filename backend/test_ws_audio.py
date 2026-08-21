import asyncio
import websockets
import json
import base64

async def test_audio():
    # 读取你的测试音频文件（必须是 WAV 格式）
    audio_path = "test_48k.wav"
    
    try:
        with open(audio_path, "rb") as f:
            audio_bytes = f.read()
    except FileNotFoundError:
        print(f"❌ 找不到音频文件: {audio_path}")
        print("💡 请用录音机录制一段语音，保存为 test_48k.wav 放在当前目录下")
        return
    
    audio_b64 = base64.b64encode(audio_bytes).decode()
    
    uri = "ws://localhost:8000/ws"
    try:
        async with websockets.connect(uri) as websocket:
            print("✅ WebSocket 连接成功")
            
            # 发送音频消息
            await websocket.send(json.dumps({
                "type": "audio_input",
                "payload": {"audio_base64": audio_b64}
            }))
            print("📤 已发送音频，等待识别和回复...")
            
            # 接收回复（可能会收到多条消息）
            try:
                while True:
                    response = await websocket.recv()  # 一直等到收到消息
                    data = json.loads(response)
                    msg_type = data.get("type")
                    payload = data.get("payload", {})
                    
                    if msg_type == "state_update":
                        print(f"📊 状态更新: {payload.get('state')}")
                    elif msg_type == "text_input":
                        print(f"📝 识别文字: {payload.get('text')}")
                    elif msg_type == "audio_chunk":
                        print(f"💬 回复: {payload.get('text')}")
                    else:
                        print(f"📥 收到: {data}")
                        
            except asyncio.TimeoutError:
                print("⏰ 接收超时，测试结束")
                
    except ConnectionRefusedError:
        print("❌ 连接失败，请确保后端已启动 (python main.py)")

if __name__ == "__main__":
    asyncio.run(test_audio())