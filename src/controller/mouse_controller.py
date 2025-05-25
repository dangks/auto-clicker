import pyautogui
import time
import threading
import win32api
import win32con
from ctypes import windll, byref, c_ulonglong
import atexit

class MouseController:
    def __init__(self):
        self._clicking = False
        self.click_thread = None
        self.interval = 1.0  # 默认点击间隔(秒)
        self.duration = 0  # 默认持续时间(0表示无限)
        
        # 提高Windows时间精度到0.5ms
        windll.winmm.timeBeginPeriod(1)
        atexit.register(self._cleanup)
        
        # 禁用pyautogui的所有安全限制和延迟
        pyautogui.MINIMUM_DURATION = 0
        pyautogui.MINIMUM_SLEEP = 0
        pyautogui.PAUSE = 0
        
        # 初始化性能计数器频率
        self.perf_freq = c_ulonglong()
        windll.kernel32.QueryPerformanceFrequency(byref(self.perf_freq))
    
    def _cleanup(self):
        """清理时间精度设置"""
        windll.winmm.timeEndPeriod(1)
    
    def _get_precise_time(self):
        """获取高精度时间戳"""
        current = c_ulonglong()
        windll.kernel32.QueryPerformanceCounter(byref(current))
        return current.value / self.perf_freq.value
    
    def start_clicking(self):
        """开始连续点击"""
        if not self._clicking:
            self._clicking = True
            self.click_thread = threading.Thread(target=self._click_loop)
            self.click_thread.daemon = True
            self.click_thread.start()

    def stop_clicking(self):
        """停止连续点击"""
        self._clicking = False
        if self.click_thread:
            self.click_thread.join(timeout=1.0)

    def is_clicking(self):
        """返回当前是否正在点击"""
        return self._clicking

    def set_interval(self, interval):
        """设置点击间隔"""
        # 移除最小间隔限制，允许更快的点击
        self.interval = max(0.001, float(interval))  # 最小间隔改为1ms

    def set_duration(self, duration):
        """设置持续时间"""
        self.duration = max(0, float(duration))

    def _direct_click(self):
        """优化的快速点击方法，减少函数调用"""
        try:
            x, y = win32api.GetCursorPos()
            # 合并按下和抬起为一次调用，减少API调用次数
            win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN | win32con.MOUSEEVENTF_LEFTUP, x, y, 0, 0)
        except:
            pass  # 忽略可能的错误以保持高速运行

    def _click_loop(self):
        """高性能点击循环"""
        start_time = self._get_precise_time()
        interval = max(0.0005, self.interval)  # 将最小间隔降低到0.5ms
        
        while self._clicking:
            current_time = self._get_precise_time()
            
            # 检查持续时间
            if self.duration > 0 and (current_time - start_time) > self.duration:
                self._clicking = False
                break

            # 快速点击
            self._direct_click()
            
            # 精确休眠控制
            if interval > 0:
                target_time = current_time + interval
                while self._clicking:
                    now = self._get_precise_time()
                    if now >= target_time:
                        break
                    remaining = target_time - now
                    if remaining > 0.0005:  # 只在间隔较大时休眠
                        time.sleep(0.0001)  # 使用最小休眠时间