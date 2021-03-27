import gpiozero
import json, requests
from time import sleep

import RPi.GPIO as GPIO

def read_sudoku_line():
    request = requests.get('http://ainosudoku.com/test/simple_string.json')
    request_text = request.text
    my_dict = {}
    my_dict = json.loads(request_text)
    
    sudoku = my_dyct['sudoku_line']
    
    return sudoku

ser_in0 = gpiozero.LED(20)
rck = gpiozero.LED(23)
srck = gpiozero.LED(24)
srclr = gpiozero.LED(25)
g = gpiozero.LED(26)

srclr.on()

g.off()

def out(line, sudoku_string):
    global ser_in0
    global rck
    global srck
    global srclr
    global g
    g.on()
    for lamp_num in range(9):
        shift_lamp_index = 8 - lamp_num
        digit = 15 - int(sudoku_string[shift_lamp_index])
        
        d = {}
        d['0'] = ser_in0
        
        for i in range(16):
            if i == digit:
                d['0'].on()
            else:
                d['0'].off()
            srck.on()
            rck.on()
            sleep(0.0001)
            srck.off()
            rck.off()
    g.off()
    sleep(0.00001)
    
    
def main():
    while True:
        sudoku = read_sudoku_line()
        out(0,sudoku)
        sleep(0.3)
        
        
if __name__ == '__main__':
    main()