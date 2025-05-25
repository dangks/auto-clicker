import keyboard


class KeyboardController:
    def __init__(self):
        self.hotkey = 'f9'  # 默认热键为F9
        self.window = None
        self.mouse_controller = None

    def start_listening(self, mouse_controller):
        """开始监听键盘热键"""
        self.mouse_controller = mouse_controller
        keyboard.on_press_key(self.hotkey, self._toggle_clicking)

    def stop_listening(self):
        """停止监听键盘热键"""
        keyboard.unhook_all()

    def _toggle_clicking(self, event):
        """切换点击状态"""
        if not self.mouse_controller:
            return
        
        if self.mouse_controller.is_clicking():
            self.mouse_controller.stop_clicking()
            if self.window:
                self.window.deiconify()  # 从最小化恢复窗口
        else:
            if self.window:
                self.window.iconify()  # 最小化窗口
            self.mouse_controller.start_clicking()

    def set_hotkey(self, new_hotkey):
        """设置新的热键"""
        keyboard.unhook_all()
        self.hotkey = new_hotkey
        if self.mouse_controller:
            keyboard.on_press_key(self.hotkey, self._toggle_clicking)