# voice_service.py
import librosa
import soundfile as sf
import os
import tempfile
from funasr import AutoModel

# 全局模型（只加载一次）
_model = None

def get_model():
    global _model
    if _model is None:
        _model = AutoModel(
            model="Qwen/Qwen3-ASR-0.6B",
            device="cpu",
            use_onnx=True,
            vad_model="fsmn-vad",
            disable_update=True,
        )
    return _model

def transcribe_audio(audio_bytes: bytes) -> str:
    """
    接收音频字节流 (WAV格式)，返回识别出的文字
    """
    # 1. 保存临时文件
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
        tmp.write(audio_bytes)
        tmp_path = tmp.name
    
    try:
        # 2. 重采样到 16kHz 单声道
        y, sr = librosa.load(tmp_path, sr=16000, mono=True)
        processed_path = tmp_path.replace(".wav", "_16k.wav")
        sf.write(processed_path, y, 16000, subtype='PCM_16')
        
        # 3. 识别
        model = get_model()
        result = model.generate(input=processed_path, language="zh")
        text = result[0]['text']
        return text
    finally:
        # 4. 清理临时文件
        os.unlink(tmp_path)
        if os.path.exists(processed_path):
            os.unlink(processed_path)