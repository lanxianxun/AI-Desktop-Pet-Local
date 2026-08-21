# 启动女儿_智能桌面切换.ps1
Write-Host "Lunching Virtual Desktop Switcher..." -ForegroundColor Green

# 获取当前桌面编号（Windows 11 虚拟桌面 API）
Add-Type -TypeDefinition @"
using System;
using System.Runtime.InteropServices;
public class VirtualDesktopAPI {
    [DllImport("user32.dll")]
    public static extern void keybd_event(byte bVk, byte bScan, uint dwFlags, UIntPtr dwExtraInfo);
}
"@

# 模拟 Ctrl+Win+→ 切换到下一个桌面
function Next-VirtualDesktop {
    [VirtualDesktopAPI]::keybd_event(0x5B, 0, 0, [System.UIntPtr]::Zero) # Win
    [VirtualDesktopAPI]::keybd_event(0x11, 0, 0, [System.UIntPtr]::Zero) # Ctrl
    [VirtualDesktopAPI]::keybd_event(0x27, 0, 0, [System.UIntPtr]::Zero) # 右箭头
    Start-Sleep -Milliseconds 200
    [VirtualDesktopAPI]::keybd_event(0x5B, 0, 2, [System.UIntPtr]::Zero)
    [VirtualDesktopAPI]::keybd_event(0x11, 0, 2, [System.UIntPtr]::Zero)
    [VirtualDesktopAPI]::keybd_event(0x27, 0, 2, [System.UIntPtr]::Zero)
    Start-Sleep -Milliseconds 500
}

# 模拟 Ctrl+Win+← 切换到上一个桌面
function Prev-VirtualDesktop {
    [VirtualDesktopAPI]::keybd_event(0x5B, 0, 0, [System.UIntPtr]::Zero) # Win
    [VirtualDesktopAPI]::keybd_event(0x11, 0, 0, [System.UIntPtr]::Zero) # Ctrl
    [VirtualDesktopAPI]::keybd_event(0x25, 0, 0, [System.UIntPtr]::Zero) # 左箭头
    Start-Sleep -Milliseconds 200
    [VirtualDesktopAPI]::keybd_event(0x5B, 0, 2, [System.UIntPtr]::Zero)
    [VirtualDesktopAPI]::keybd_event(0x11, 0, 2, [System.UIntPtr]::Zero)
    [VirtualDesktopAPI]::keybd_event(0x25, 0, 2, [System.UIntPtr]::Zero)
    Start-Sleep -Milliseconds 500
}

# 2. 切换到桌面2（用 Ctrl+Win+→ 确保当前在桌面2）
Write-Host "Changing to Virtual Desktop 2..." -ForegroundColor Yellow
Next-VirtualDesktop

# 3. 在桌面2启动所有服务
Write-Host "Starting backend services..." -ForegroundColor Yellow
Start-Process -WindowStyle Minimized -FilePath "cmd.exe" -ArgumentList "/k cd /d $PSScriptRoot\backend && venv\Scripts\activate && python main.py"

Start-Sleep -Seconds 3

Write-Host "Starting frontend static server..." -ForegroundColor Yellow
Start-Process -WindowStyle Minimized -FilePath "cmd.exe" -ArgumentList "/k cd /d $PSScriptRoot\frontend && http-server dist -p 8080"

Start-Sleep -Seconds 2

Write-Host "Starting Electron desktop window..." -ForegroundColor Yellow
Start-Process -FilePath "cmd.exe" -ArgumentList "/k cd /d $PSScriptRoot\frontend && node_modules\electron\dist\electron.exe ."

Start-Sleep -Seconds 1

# 4. 关键步骤：切回上一个桌面（桌面1），而桌宠窗口会留在桌面2
Write-Host "Changing back to Virtual Desktop 1..." -ForegroundColor Green
Prev-VirtualDesktop

Write-Host "All services started!" -ForegroundColor Green
Write-Host "Desktop 1: Normal operation | Desktop 2: Service logs (Ctrl+Win+→ to view)" -ForegroundColor Cyan