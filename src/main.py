# src/main.py

import time
import tkinter as tk
from controller.mouse_controller import MouseController
from controller.keyboard_controller import KeyboardController
from ui.settings import Settings

class AutoClickerApp:
    def __init__(self):
        self.root = tk.Tk()  # 创建主窗口
        self.root.withdraw()  # 隐藏主窗口
        
        self.mouse_controller = MouseController()
        self.keyboard_controller = KeyboardController()
        
        # 创建合并后的窗口
        self.window = Settings(self.root, self.mouse_controller, self.keyboard_controller)
        # 传递窗口引用给键盘控制器
        self.keyboard_controller.window = self.window

    def run(self):
        try:
            self.keyboard_controller.start_listening(self.mouse_controller)
            self.window.show()  # 显示窗口
            self.root.mainloop()
        except KeyboardInterrupt:
            self.cleanup()
        finally:
            self.cleanup()
            
    def cleanup(self):
        if self.window:
            self.window.destroy()
        self.keyboard_controller.stop_listening()
        self.mouse_controller.stop_clicking()
        self.root.quit()

if __name__ == "__main__":
    app = AutoClickerApp()
    app.run()