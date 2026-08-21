import React, { useState, useRef, useEffect } from 'react';

export default function VoiceInput({ onAudioCaptured, onRecordStart, disabled }) {
  const [isRecording, setIsRecording] = useState(false);
  const [mode, setMode] = useState('push-to-talk'); // 'always-on' 或 'push-to-talk'
  const mediaRecorderRef = useRef(null);
  const audioChunksRef = useRef([]);
  const streamRef = useRef(null);
  const isRecordingRef = useRef(false); // 用于解决闭包问题

  // 监听 Electron 主进程的 IPC 消息
  useEffect(() => {
    // 检查是否在 Electron 环境中
    const ipcRenderer = window.require ? window.require('electron').ipcRenderer : null;
    if (!ipcRenderer) return;

    // 监听模式切换
    const handleModeChanged = (event, data) => {
      const newMode = data.isAlwaysOn ? 'always-on' : 'push-to-talk';
      setMode(newMode);
      
      // 如果切换到常开模式，自动开始录音
      if (newMode === 'always-on' && !isRecordingRef.current) {
        startRecording();
      }
      // 如果切换到按键说话模式，停止录音
      if (newMode === 'push-to-talk' && isRecordingRef.current) {
        stopRecording();
      }
    };

    // 监听开始录音（主进程 T 键按下）
    const handleStartRecording = () => {
      if (mode === 'push-to-talk' && !isRecordingRef.current) {
        startRecording();
      }
    };

    // 监听停止录音（主进程 T 键松开）
    const handleStopRecording = () => {
      if (mode === 'push-to-talk' && isRecordingRef.current) {
        stopRecording();
      }
    };

    ipcRenderer.on('mode-changed', handleModeChanged);
    ipcRenderer.on('start-recording', handleStartRecording);
    ipcRenderer.on('stop-recording', handleStopRecording);

    return () => {
      ipcRenderer.removeAllListeners('mode-changed');
      ipcRenderer.removeAllListeners('start-recording');
      ipcRenderer.removeAllListeners('stop-recording');
    };
  }, [mode]);

  // 安全清理
  useEffect(() => {
    return () => {
      if (streamRef.current) {
        streamRef.current.getTracks().forEach(track => track.stop());
      }
    };
  }, []);

  const startRecording = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      streamRef.current = stream;

      if (onRecordStart) {
        onRecordStart();
      }

      const mediaRecorder = new MediaRecorder(stream, { mimeType: 'audio/webm' });
      mediaRecorderRef.current = mediaRecorder;
      audioChunksRef.current = [];

      mediaRecorder.ondataavailable = (event) => {
        if (event.data.size > 0) {
          audioChunksRef.current.push(event.data);
        }
      };

      mediaRecorder.onstop = () => {
        const audioBlob = new Blob(audioChunksRef.current, { type: 'audio/webm' });
        onAudioCaptured(audioBlob);
        stream.getTracks().forEach(track => track.stop());
        streamRef.current = null;
      };

      mediaRecorder.start();
      setIsRecording(true);
      isRecordingRef.current = true;

    } catch (err) {
      console.error("无法启动麦克风:", err);
      alert("请允许麦克风权限，或检查麦克风设置");
    }
  };

  const stopRecording = () => {
    if (mediaRecorderRef.current && isRecordingRef.current) {
      mediaRecorderRef.current.stop();
      setIsRecording(false);
      isRecordingRef.current = false;
    }
  };

  // 常开模式下，组件挂载时自动开始录音
  useEffect(() => {
    if (mode === 'always-on' && !isRecordingRef.current) {
      startRecording();
    }
    // 切换回按键说话时，如果正在录音则停止
    if (mode === 'push-to-talk' && isRecordingRef.current) {
      stopRecording();
    }
  }, [mode]);

  // 点击按钮切换模式（仅当不在 Electron 环境中时作为备选）
  const handleClick = () => {
    if (isRecording) {
      stopRecording();
    } else {
      startRecording();
    }
  };

  // 显示当前模式
  const modeLabel = mode === 'always-on' ? '🎤 常开' : '🎙️ 按键(T)';
  const isRecordingDisplay = isRecording ? '🔴 录音中' : '⚪ 待命';

  return (
    <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
      <span style={{ fontSize: '12px', opacity: 0.7 }}>
        {modeLabel} · {isRecordingDisplay}
      </span>
      <button
        className={`icon-button ${isRecording ? 'recording' : ''}`}
        onClick={handleClick}
        disabled={disabled}
        title={isRecording ? "点击停止" : "点击说话"}
        style={{
          backgroundColor: isRecording ? '#ff4d4f' : 'transparent',
          color: isRecording ? 'white' : 'inherit',
          border: isRecording ? 'none' : '1px solid #ccc',
          transition: 'all 0.2s',
          minWidth: '40px',
          cursor: disabled ? 'not-allowed' : 'pointer'
        }}
      >
        {isRecording ? '⏹' : '🎤'}
      </button>
    </div>
  );
}