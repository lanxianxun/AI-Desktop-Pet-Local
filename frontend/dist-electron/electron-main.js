import s from "electron";
import "path";
function c(e) {
  return e && e.__esModule && Object.prototype.hasOwnProperty.call(e, "default") ? e.default : e;
}
var r = {}, t;
function u() {
  if (t) return r;
  t = 1;
  const { app: e, BrowserWindow: n, screen: a } = s;
  e.disableHardwareAcceleration(), e.commandLine.appendSwitch("disable-features", "OutOfBlinkCors");
  function o() {
    const { width: i, height: l } = a.getPrimaryDisplay().workAreaSize;
    new n({
      width: 450,
      // 稍微宽一点，防止按钮挤下去
      height: 650,
      x: i - 500,
      y: l - 700,
      // 【核心修复 3】窗口属性配置
      frame: !1,
      // 无边框
      transparent: !0,
      // 开启透明
      backgroundColor: "#00000000",
      // 关键！ARGB格式，前两位00代表完全透明
      alwaysOnTop: !0,
      // 置顶
      hasShadow: !1,
      // 去掉系统阴影
      resizable: !0,
      // 允许调整大小
      webPreferences: {
        nodeIntegration: !0,
        contextIsolation: !1
      }
    }).loadURL("http://localhost:5173");
  }
  return e.whenReady().then(() => {
    setTimeout(o, 200);
  }), e.on("window-all-closed", () => {
    process.platform !== "darwin" && e.quit();
  }), r;
}
var d = u();
const h = /* @__PURE__ */ c(d);
export {
  h as default
};
