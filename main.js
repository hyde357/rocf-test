const { app, BrowserWindow } = require('electron');
const path = require('path');
let mainWindow;
app.whenReady().then(() => {
  mainWindow = new BrowserWindow({
    width: 1400, height: 900,
    title: 'ROCF 电子测评系统',
    webPreferences: { nodeIntegration: false }
  });
  mainWindow.loadFile('index.html');
  mainWindow.setMenuBarVisibility(false);
});
