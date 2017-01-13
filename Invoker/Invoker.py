from PIL import ImageGrab, Image, ImageChops
import os
import pythoncom, pyHook
import numpy as np
import SendInput
import time

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
        self.short_cuts = {
            't':list('eeerwww'), 
            'y':list('qqqrwww'), 
            'd':list('eewrww'), 
            'f':list('qeerwww'), 
            'g':list('qqerwww'), 
            'z':list('ewwrw'), 
            'x':list('qwwrw'), 
            'c':list('wwwr'), 
            'v':list('qqwrww'), 
            'b':list('qewrww')}
        self.type_mode = False
        self.manager = pyHook.HookManager()
        self.manager.KeyDown = self.on_keydown
        self.manager.HookKeyboard()
        self.triggering = False

    def on_keydown(self, event):
        if self.triggering:
            return True

        key = event.Key.lower()
        if key == 'return':
            self.type_mode = not self.type_mode
            return True
        
        if (not self.type_mode) and self.short_cuts.has_key(key):
            self.detector.detect()
            if (self.detector.ability1 != key and self.detector.ability2 != key):
                self.trigger_keys(self.short_cuts[key])
                return False
            elif (key == 'y'):
                self.trigger_keys('y')
                time.sleep(0.1)
                self.trigger_keys('a')
                return False
        
        return True
            
    def trigger_keys(self, keys):
        self.triggering = True
        SendInput.send_input(keys)
        self.triggering = False

if __name__ == '__main__':
    hook = Hook()
    pythoncom.PumpMessages()
