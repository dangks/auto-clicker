import tkinter as tk
from tkinter import ttk

class Settings(tk.Toplevel):
    def __init__(self, parent, mouse_controller, keyboard_controller):
        super().__init__(parent)
        self.mouse_controller = mouse_controller
        self.keyboard_controller = keyboard_controller
        
        self.title("自动连点器")
        self.geometry("400x350")
        self.resizable(False, False)
        
        # 确保窗口在任务栏显示
        self.attributes('-toolwindow', 0)  # 移除工具窗口属性
        self.transient(None)  # 移除transient属性使窗口独立
        
        # 更改默认热键
        self.hotkey_var = tk.StringVar(value="F9")
        
        self.create_widgets()
        self.center_window()
        
        # 设置窗口关闭按钮行为
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        
    def on_closing(self):
        """窗口关闭时的处理"""
        self.iconify()  # 最小化窗口而不是隐藏

    def create_widgets(self):
        # 间隔设置框架
        interval_frame = ttk.LabelFrame(self, text="点击设置", padding=10)
        interval_frame.pack(fill="x", padx=10, pady=5)
        
        # 间隔输入区域
        interval_input_frame = ttk.Frame(interval_frame)
        interval_input_frame.pack(fill="x", pady=5)
        
        ttk.Label(interval_input_frame, text="点击间隔(秒):").pack(side="left", padx=5)
        self.interval_var = tk.StringVar(value="1.0")
        self.interval_entry = ttk.Entry(
            interval_input_frame, 
            textvariable=self.interval_var,
            width=10
        )
        self.interval_entry.pack(side="left", padx=5)
        
        # 频率显示
        self.frequency_var = tk.StringVar(value="频率: 1次/秒")
        ttk.Label(
            interval_input_frame,
            textvariable=self.frequency_var,
            width=20  # 增加标签宽度
        ).pack(side="left", padx=5)
        
        # 持续时间设置框架
        duration_frame = ttk.LabelFrame(self, text="持续时间(秒) [0=无限]", padding=10)
        duration_frame.pack(fill="x", padx=10, pady=5)
        
        duration_input_frame = ttk.Frame(duration_frame)
        duration_input_frame.pack(fill="x", pady=5)
        
        ttk.Label(duration_input_frame, text="持续时间:").pack(side="left", padx=5)
        self.duration_var = tk.StringVar(value="0")
        self.duration_entry = ttk.Entry(
            duration_input_frame,
            textvariable=self.duration_var,
            width=10
        )
        self.duration_entry.pack(side="left", padx=5)
        
        # 热键设置框架
        hotkey_frame = ttk.LabelFrame(self, text="热键设置", padding=10)
        hotkey_frame.pack(fill="x", padx=10, pady=5)
        
        self.hotkey_var = tk.StringVar(value="F9")
        hotkey_label = ttk.Label(hotkey_frame, text="开始/停止热键:")
        hotkey_label.pack(side="left", padx=5)
        
        self.hotkey_entry = ttk.Entry(
            hotkey_frame,
            textvariable=self.hotkey_var,
            width=10
        )
        self.hotkey_entry.pack(side="left", padx=5)
        
        # 按钮区域
        button_frame = ttk.Frame(self)
        button_frame.pack(fill="x", padx=10, pady=10)
        
        self.start_button = ttk.Button(
            button_frame,
            text="开始运行",
            command=self.start_clicking
        )
        self.start_button.pack(side="right", padx=5)

        # 移除应用按钮，因为现在是实时应用
        
        # 绑定输入框更新事件并设置立即应用
        self.interval_var.trace_add("write", self.on_interval_change_and_apply)
        self.duration_var.trace_add("write", self.on_duration_change_and_apply)
        self.hotkey_var.trace_add("write", self.on_hotkey_change_and_apply)

    def on_interval_change_and_apply(self, *args):
        """输入框改变时更新频率显示并应用设置"""
        try:
            interval = float(self.interval_var.get())
            if interval <= 0:
                return
            self.update_frequency_display(interval)
            self.mouse_controller.set_interval(interval)
        except ValueError:
            pass

    def on_duration_change_and_apply(self, *args):
        """持续时间输入框改变时的回调并应用设置"""
        try:
            duration = float(self.duration_var.get())
            if duration < 0:
                self.duration_var.set("0")
                duration = 0
            self.mouse_controller.set_duration(duration)
        except ValueError:
            pass

    def on_hotkey_change_and_apply(self, *args):
        """热键改变时立即应用"""
        try:
            hotkey = self.hotkey_var.get()
            self.keyboard_controller.set_hotkey(hotkey)
        except:
            pass

    def update_frequency_display(self, interval):
        """更新频率显示，统一格式为'每X秒/X次'"""
        if interval <= 0:
            return
            
        if interval <= 1:  # 间隔小于等于1秒，显示每秒多少次
            frequency = 1 / interval
            if frequency >= 100:
                self.frequency_var.set(f"每秒/{frequency:.0f}次")
            else:
                self.frequency_var.set(f"每秒/{frequency:.1f}次")
        else:  # 间隔大于1秒，显示每隔多久1次
            if interval >= 3600:  # 大于等于1小时
                hours = int(interval // 3600)
                remaining = interval % 3600
                minutes = int(remaining // 60)
                seconds = remaining % 60
                
                time_str = f"{hours}小时"
                if minutes > 0 or seconds > 0:  # 如果有余下的分秒
                    if seconds == 0:  # 只有分钟
                        time_str += f"{minutes}分"
                    else:  # 有秒
                        if minutes > 0:  # 有分有秒
                            time_str += f"{minutes}分{seconds:.0f}秒"
                        else:  # 只有秒
                            time_str += f"{seconds:.0f}秒"
                self.frequency_var.set(f"每{time_str}/次")
            else:  # 小于1小时，精确到分秒
                minutes = int(interval // 60)
                seconds = interval % 60
                if minutes > 0:
                    if seconds == 0:
                        self.frequency_var.set(f"每{minutes}分钟/次")
                    else:
                        self.frequency_var.set(f"每{minutes}分{seconds:.0f}秒/次")
                else:
                    self.frequency_var.set(f"每{seconds:.1f}秒/次")

    def start_clicking(self):
        """开始点击"""
        try:
            interval = float(self.interval_var.get())
            duration = float(self.duration_var.get())
            
            if interval <= 0:
                raise ValueError("点击间隔必须大于0")
            if duration < 0:
                duration = 0
                
            self.iconify()  # 最小化窗口而不是隐藏
            self.mouse_controller.start_clicking()
            
        except ValueError as e:
            tk.messagebox.showerror("错误", f"请输入有效的数值!\n{str(e)}")

    def show(self):
        """显示设置窗口"""
        self.deiconify()

    def center_window(self):
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f'{width}x{height}+{x}+{y}')