#!/usr/bin/env python3

#copy all code files from host to client:
#scp -r "/Users/philippmielke/Documents/Hochschule/Modulunterlagen/6. Semester/ES/Embedded Systems 1/UE/Labor 4/Quellcode/"* phil@10.0.10.20:/home/phil/Uniprojekte/Lab4/

import sys, time
#from src.camera import Camerasettings, enable_motionDetector
from src.camera import *
from src.pir import *

def main():
    """
        1. Initialisierung des PIR Sensors
    """
    pinNumberPIR : int  = 2
    init_pir(pinNumberPIR)

    """
        2. Initialisierung der Objektliste
    """
    init_objList()

    """
        3. Initialisierung der Objekte mit den jeweiligen
           Kameraeinstellungen
            - mögliche Einstellungen:
                name : str
                path : str
                widht : int
                hight : int
                rotation : int
                effect : str
    """
    name : str = "telegram"
    path : str = "home/phil/Uniprojekte/Lab4/Applications"
    telegram: Camerasettings = Camerasettings(name, path)
    set_objListValue(telegram)

    name = "browser"
    path = "home/phil/Uniprojekte/Lab4/Applications"
    browser : Camerasettings = Camerasettings(name, path)
    set_objListValue(browser)

    try:
        while True:
            try:
                timeInSeconds = 60
                #enable_motionDetector(timeInSeconds)
                time.sleep(timeInSeconds)

            except KeyboardInterrupt:
                exit_pir()
                break
    finally:
        print("Auf Wiedersehen...")

if __name__ == "__main__":
    main()
