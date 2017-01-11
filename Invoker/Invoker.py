from PIL import ImageGrab
import cv2
import os
import win32api, win32con
import pythoncom, pyHook

threshold = 100

def read_templates():
    templates = {}
    for file in os.listdir(os.curdir):
        if file.endswith('.png'):
            img = cv2.imread(file)
            img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            ret, img = cv2.threshold(img, threshold, 255, cv2.THRESH_BINARY)
            templates[file[0:-4]] = img
    return templates

def recognize_letter(region, templates):
    img = ImageGrab.grab(bbox=region)
    return 'x'
    

class AbilityDetector:
    def __init__(self):
        self.ability1 = ''
        self.ability2 = ''

    def detect(self):
        self.ability1 = ''
        self.ability2 = ''


class Hook:
    def __init__(self):
        self.detector = AbilityDetector()
        self.short_cuts = {'t':'eeerwww', 'y':'qqqrwww', 'd':'eewrww', 'f':'qeerwww', 'g':'qqerwww', 'z':'ewwrw', 'x':'qwwrw', 'c':'wwwr', 'v':'qqwrww', 'b':'qewrww'}
        self.vkey = {'q':0x51, 'w':0x57, 'e':0x45, 'r':0x52}
        self.type_mode = False
        self.manager = pyHook.HookManager()
        self.manager.KeyDown = self.on_keyboard_event
        self.manager.HookKeyboard()

    def on_keyboard_event(self, event):
        key = event.Key.lower()
        if key == 'return':
            self.type_mode = not self.type_mode
            return True
        
        if (not self.type_mode) and self.short_cuts.has_key(key):
            self.detector.detect()
            if (self.detector.ability1 != key and self.detector.ability2 != key):
                self.trigger_keys(self.short_cuts[key])
                return False
        
        return True
            
    def trigger_keys(self, keys):
        self.manager.UnhookKeyboard();
        for key in keys:
            win32api.keybd_event(self.vkey[key], 0, 0, 0)
            win32api.keybd_event(self.vkey[key], 0, win32con.KEYEVENTF_KEYUP, 0)
        self.manager.HookKeyboard()


if __name__ == '__main__':
    hook = Hook()
    pythoncom.PumpMessages()
