# Auto Clicker (自动连点器)

这是一个自动连点器程序，支持高速点击和精确的时间控制。程序启动后会显示设置界面，可以精确控制点击频率和持续时间。

## 主要特性

- 高性能点击：支持近千次/秒的点击频率
- 精确的时间控制：可设置精确的点击间隔和持续时间
- 极简的界面：显示直观的频率/间隔提示
- 便捷的操作：
  - F9 快捷键控制开始/暂停
  - 实时更新参数设置

## 安装要求

- Python 3.6+
- Windows 操作系统（需要管理员权限）
- 依赖库：
  - tkinter
  - pyautogui
  - keyboard
  - win32api

## 完整目录结构

```
auto-clicker/
├── src/                               # 源代码目录
│   ├── controller/                    # 控制器目录
│   │   ├── mouse_controller.py        # 鼠标点击控制
│   │   └── keyboard_controller.py     # 键盘监听控制
│   ├── ui/                            # 界面目录
│   │   └── settings.py                # 设置窗口
│   └── main.py                        # 程序入口
├── requirements.txt                   # 依赖列表
└── README.md                          # 项目说明文档
```

## 安装步骤

1. 克隆仓库：
   ```bash
   git clone <repository-url>
   ```

2. 进入项目目录：
   ```bash
   cd auto-clicker
   ```

3. 安装依赖：
   ```bash
   pip install -r requirements.txt
   ```

## 使用说明

1. 以管理员权限运行程序：
   ```bash
   python src/main.py
   ```

2. 在设置界面中：
   - 设置点击间隔（秒）：支持 0.001-∞ 秒
   - 设置持续时间：0=无限，其他为指定秒数
   - 查看实时频率/间隔提示

3. 操作说明：
   - 点击"开始运行"启动连点器
   - 使用 F9 快捷键切换开始/暂停
   - 程序会自动最小化到任务栏
   - 暂停时自动显示设置窗口
   - 关闭窗口时程序最小化而不会退出

## 注意事项

- 需要管理员权限运行（用于全局键盘监听）
- 高频点击可能对某些程序造成负担
- 建议从低频率开始测试（如每秒10次）
- 在高频点击时可能会影响系统性能

## 开发计划

- [ ] 添加自定义快捷键设置
- [ ] 增加点击位置记录功能
- [ ] 支持多点位循环点击
- [ ] 添加点击模式选择（单击/双击/按住）
- [ ] 支持保存配置方案

## 致谢

本项目使用了以下开源项目：
- [PyAutoGUI](https://github.com/asweigart/pyautogui) - 用于模拟鼠标操作
- [keyboard](https://github.com/boppreh/keyboard) - 用于全局键盘监听
- [tkinter](https://docs.python.org/3/library/tkinter.html) - GUI界面开发
- [win32api](https://github.com/mhammond/pywin32) - Windows API 调用

## 许可证

本项目基于 MIT 许可证开源。