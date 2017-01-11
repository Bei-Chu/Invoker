from PIL import ImageGrab, Image, ImageChops
import os
import win32api, win32con
import pythoncom, pyHook
import numpy as np

threshold = 100

def recognize_letter(region, templates):
    img = ImageGrab.grab(bbox=region)
    return 'x'
    

class AbilityDetector:
    def __init__(self):
        self.region1 = (927, 955, 939, 968)
        self.region2 = (985, 955, 997, 968)
        self.ability1 = ''
        self.ability2 = ''
        self.templates = {}
        for file in os.listdir(os.curdir):
            if file.endswith('.png'):
                img = Image.open(file)
                self.templates[file[0:-4]] = img

    def match_templates(self, img):
        errors = {}
        for name, template in self.templates.items():
            diff = ImageChops.subtract(template, img)
            diff = np.array(diff)
            errors[name] = np.sum(np.abs(diff))
        return min(errors, key=errors.get)

    def detect(self):
        img = ImageGrab.grab()
        self.ability1 = self.match_templates(img.crop(self.region1))
        self.ability2 = self.match_templates(img.crop(self.region2))

    def save_ability_icon(self):
        img = ImageGrab.grab()
        icon1 = img.crop(self.region1)
        icon1.save('icon1.png')
        icon2 = img.crop(self.region2)
        icon2.save('icon2.png')


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

        if self.vkey.has_key(key):
            self.trigger_keys(key)
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
