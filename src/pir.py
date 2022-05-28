import RPi.GPIO as GPIO
import time

from src.camera import get_objList

def init_pir(pinNumberPIR):
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(pinNumberPIR, GPIO.IN)
    GPIO.add_event_detect(pinNumberPIR , GPIO.RISING, callback=pir_callback)

def exit_pir():
    GPIO.cleanup()

def pir_callback(channel):
    print("Bewegung erkannt.")
    cameraWarmup : float = 0.75
    objList = get_objList()
    for app in objList:
        app.get_picture(cameraWarmup)
        time.sleep(cameraWarmup)
    return
