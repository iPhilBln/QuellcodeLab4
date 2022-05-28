#!/usr/bin/env python3

#copy all code files from host to client:
#scp -r "/Users/philippmielke/Documents/Hochschule/Modulunterlagen/6. Semester/ES/Embedded Systems 1/UE/Labor 4/Quellcode/"* uniprojekt:/home/phil/Uniprojekte/Lab4/

import sys, time
from src.camera import *
from src.pir import *

def main():
    """
        1. Initialisierung des PIR Sensors
        2. Initialisierung der Objektliste
    """
    pinNumberPIR : int  = 4
    init_pir(pinNumberPIR)

    init_objList()

    """
        3. Initialisierung der Objekte mit den jeweiligen
           Kameraeinstellungen
            - mögliche Einstellungen:
                name : str
                path : str
                width : int
                hight : int
                rotation : int
                effect : str
            - Camerasettings.print_effects() gibt alle möglichen Effekte aus
    """
    name : str = "telegram"
    path : str = "/home/phil/Uniprojekte/Lab4/Applications"
    telegram: Camerasettings = Camerasettings(name, path)
    set_objListValue(telegram)

    name : str = "browser"
    path : str = "/home/phil/Uniprojekte/Lab4/Applications"
    width : int = 640
    hight : int = 480
    browser : Camerasettings = Camerasettings(name, path, width, hight)
    set_objListValue(browser)

    list = get_objList()
    for obj in list:
        print()
        print(obj)

    telegram.get_picture(0.75)
    browser.start_stream()

    while True:
        try:
            timeInSeconds = 60
            #enable_motionDetector(timeInSeconds)
            time.sleep(timeInSeconds)
        except KeyboardInterrupt:
            print("Auf Wiedersehen...")
            exit_pir()
            sys.exit()

if __name__ == "__main__":
    main()
