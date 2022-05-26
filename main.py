#!/usr/bin/env python3

#copy all code files from host to client:
#scp -r "/Users/philippmielke/Documents/Hochschule/Modulunterlagen/6. Semester/ES/Embedded Systems 1/UE/Labor 4/Quellcode/"* phil@10.0.10.20:/home/phil/Uniprojekte/Lab4/

import sys, time
from src.camera import Camerasettings

def main():
    try:
        telegram: Camerasettings = Camerasettings("phil")
#        telegram.path = "/home/phil/test/"

        name = "tg1"
        path = "/home/phil/test/"
        tg1: Camerasettings = Camerasettings(name, path)

        name = "tg2"
        path = "/home/phil/test/"
        tg2: Camerasettings = Camerasettings(name, path,None,None,None,"colorswap")


        print (telegram)
        print()
        print (tg1)
        print()
        print (tg2)

        Camerasettings.print_effects()


        #Camerasettings.print_effects()
        #Camerasettings.init()

        #print("Wir machen Foto 1...")
        #tg1.get_picture()
        #print("Wir machen Foto 2...")
        #tg2.get_picture()
        #Camerasettings.print_effects()
    except KeyboardInterrupt:
        print("Auf Wiedersehen...")
#        Camerasettings.exit()
#    finally:
#        Camerasettings.exit()

if __name__ == "__main__":
    main()
