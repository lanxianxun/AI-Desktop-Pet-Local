const { app, BrowserWindow, screen, globalShortcut, Notification } = require('electron');
const path = require('path');

// 设置 AppUserModelId（Windows 通知必须）
app.setAppUserModelId('com.yourcompany.ai-desktop-pet');

// 全局状态
let mainWindow = null;
let isAlwaysOn = false; // false: 按键说话, true: 常开
let isRecording = false;

// 通知辅助函数
function sendNotification(title, body, silent = false) {
  if (process.platform === 'win32') {
    new Notification({ 
      title, 
      body, 
      silent, 
      icon: null 
    }).show();
  }
}

// 【核心修复 1】禁用硬件加速，否则 Windows 上透明窗口会变黑
app.disableHardwareAcceleration();

// 【核心修复 2】允许延迟创建，防止黑屏闪烁
app.commandLine.appendSwitch('disable-features', 'OutOfBlinkCors');

function createWindow() {
  const { width, height } = screen.getPrimaryDisplay().workAreaSize;

  mainWindow = new BrowserWindow({
    width: 450,
    height: 650,
    x: width - 500,
    y: height - 700,
    
    frame: false,
    transparent: true,
    backgroundColor: '#00000000',
    alwaysOnTop: true,
    hasShadow: false,
    resizable: true,
    
    webPreferences: {
      nodeIntegration: true,
      contextIsolation: false,
    }
  });

  mainWindow.loadURL('http://localhost:8080');
}

// 注册全局快捷键
function registerShortcuts() {
  // Alt+T: 切换模式
  globalShortcut.register('Alt+T', () => {
    isAlwaysOn = !isAlwaysOn;
    const mode = isAlwaysOn ? '常开' : '按键说话';
    const emoji = isAlwaysOn ? '🎤' : '🎙️';
    sendNotification(`${emoji} 麦克风${mode}模式`, `已切换到${mode}模式${isAlwaysOn ? '，将持续监听' : '，按住 T 键说话'}`);
    
    // 通知前端切换模式
    if (mainWindow) {
      mainWindow.webContents.send('mode-changed', { isAlwaysOn });
    }
  });

  // T 键按下（仅按键说话模式有效）
  globalShortcut.register('T', () => {
    if (!isAlwaysOn && !isRecording) {
      isRecording = true;
      sendNotification('🎙️ 录音中', '按住 T 键说话，松开后自动发送', true);
      
      // 通知前端开始录音
      if (mainWindow) {
        mainWindow.webContents.send('start-recording');
      }
    }
  });

  // 注意：globalShortcut 不支持 keyup，所以 T 键松开需要在前端监听
  // 我们通过前端发送 'stop-recording' 事件来通知主进程
}

// 监听前端发送的停止录音事件
app.on('stop-recording', () => {
  if (isRecording) {
    isRecording = false;
    sendNotification('📤 已发送', '语音正在识别中...', true);
    
    // 通知前端停止录音
    if (mainWindow) {
      mainWindow.webContents.send('stop-recording');
    }
  }
});

// 这里的延时是为了让 GPU 状态稳定后再创建窗口
app.whenReady().then(() => {
  setTimeout(() => {
    createWindow();
    registerShortcuts();
  }, 200);
});

app.on('window-all-closed', () => {
  // 注销所有快捷键
  globalShortcut.unregisterAll();
  if (process.platform !== 'darwin') app.quit();
});