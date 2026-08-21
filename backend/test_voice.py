import librosa
import soundfile as sf
from funasr import AutoModel
import os

# 1. 音频预处理函数：把 48kHz 双声道 → 16kHz 单声道
def preprocess_audio(input_path, output_path):
    print(f"正在转换音频: {input_path}")
    # 加载音频，强制重采样到 16000Hz，转为单声道
    y, sr = librosa.load(input_path, sr=16000, mono=True)
    # 保存为临时文件
    sf.write(output_path, y, 16000, subtype='PCM_16')
    print(f"转换完成，保存至: {output_path}")
    return output_path

# 2. 使用 FunASR 加载模型
print("正在加载 FunASR 模型，首次加载可能需要几秒钟...")
model_path = 'C:/Users/Administrator/Qwen3-ASR-0.6B'

# 使用 FunASR 的 AutoModel 加载本地模型
try:
    model = AutoModel(
        model=model_path,  # 指向本地模型文件夹
        model_revision="master",
        device="cpu",      # 强制使用 CPU
        disable_updates=True,
    )
    print("FunASR 模型加载完成！")
except Exception as e:
    print(f"FunASR 加载失败: {e}")
    print("尝试使用模型名称加载...")
    # 备选方案：使用模型名称从魔搭加载
    model = AutoModel(
        model="Qwen/Qwen3-ASR-0.6B",
        device="cpu",
    )
    print("模型加载完成！")

# 3. 测试主流程
if __name__ == "__main__":
    raw_audio = "test_48k.wav"   # 替换成你的文件名
    processed_audio = "test_16k.wav"
    
    if not os.path.exists(raw_audio):
        print(f"错误: 找不到文件 {raw_audio}，请把音频文件放在 backend 目录下")
    else:
        # 转换格式
        preprocess_audio(raw_audio, processed_audio)
        
        print("正在识别语音...")
        # 调用 FunASR 模型进行识别
        result = model.generate(
            input=processed_audio,
            language="zh",  # 指定中文
            use_itn=True,   # 使用反文本正则化，让输出更自然
        )
        print(f"识别结果: {result[0]['text']}")