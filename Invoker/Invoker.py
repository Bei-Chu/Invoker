from PIL import ImageGrab
import cv2
import os
from matplotlib import pyplot

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
    
def write_to_file(letter1, letter2):
    file = open('cur_ability.txt', 'w')
    file.write(letter1)
    file.write(letter2)
    file.close()

if __name__ == '__main__':
    templates = read_templates()
    region1 = ()
    region2 = ()
    letter1 = recognize_letter(region1, templates)
    letter2 = recognize_letter(region2, templates)
    write_to_file(letter1, letter2)
