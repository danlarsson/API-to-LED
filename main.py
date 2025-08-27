## 
#  API server that can enable GPIO ports
#

## Settings
# GPIO PORTS
led1 = 23   # GPIO 23 Relay 1
led2 = 24   # GPIO 24 Relay 2
button = 25 # GPIO 25 Button
############

from typing import Union
from fastapi import FastAPI
from sys import exit
import RPi.GPIO as GPIO
import uvicorn
import signal


app = FastAPI()
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO.setup(led1,GPIO.OUT)
GPIO.setup(led2,GPIO.OUT)
GPIO.setup(button, GPIO.IN, GPIO.PUD_UP) # Pull UP Resistor

def led_on(led):
   if led == 1:
      GPIO.output(led1, GPIO.HIGH)
   elif led == 2:
      GPIO.output(led2, GPIO.HIGH)

def led_off(led):
   if led == 1:
      GPIO.output(led1, GPIO.LOW)
   elif led == 2:
      GPIO.output(led2, GPIO.LOW)

def led_status(led):
   if led == 1:
      ret = GPIO.input(led1)
   elif led == 2:
      ret = GPIO.input(led2)
   return(ret)

def button_pressed(channel):
   print("Button pressed")
   led_off(1)
   led_off(2)

def signal_handler(sig, frame): # In use??
   GPIO.cleanup()
   exit()

### FastAPI ###

@app.put("/alarm/{alarm_id}")
def activate_alarm(alarm_id: int):
    if alarm_id == 1 or alarm_id == 2:
	    led_on(alarm_id)
    return{"alarm": alarm_id}


@app.put("/reset/{alarm_id}")
def reset_alarm(alarm_id: int):
    led_off(alarm_id)
    return{"alarm": alarm_id}


@app.get("/")
def read_root():
    return {"alarm_1": led_status(1), "alarm_2": led_status(2)}


## RUN ##
if __name__ == "__main__":
    GPIO.add_event_detect(button, GPIO.FALLING, callback=button_pressed, bouncetime=100)
    signal.signal(signal.SIGINT, signal_handler)

    uvicorn.run("main:app", host="0.0.0.0", port=8073, reload=True, log_level="debug")
