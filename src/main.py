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
        
        # 绑定Windows关闭事件
        self.root.protocol("WM_DELETE_WINDOW", self.cleanup)
        
        self.mouse_controller = MouseController()
        self.keyboard_controller = KeyboardController()
        
        # 创建设置窗口
        self.window = Settings(self.root, self.mouse_controller, self.keyboard_controller)
        self.keyboard_controller.window = self.window
        
        # 传递cleanup方法给Settings窗口
        self.window.set_quit_callback(self.cleanup)

    def run(self):
        try:
            self.keyboard_controller.start_listening(self.mouse_controller)
            self.window.show()
            self.root.mainloop()
        except KeyboardInterrupt:
            self.cleanup()
        except Exception as e:
            print(f"发生错误: {str(e)}")
            self.cleanup()
            
    def cleanup(self):
        """程序清理和退出"""
        try:
            if self.window:
                self.window.destroy()
            self.keyboard_controller.stop_listening()
            self.mouse_controller.stop_clicking()
            self.root.quit()
            self.root.destroy()  # 确保主窗口被销毁
        except:
            pass  # 忽略清理过程中的错误
        finally:
            import sys
            sys.exit(0)  # 强制退出程序

if __name__ == "__main__":
    app = AutoClickerApp()
    app.run()