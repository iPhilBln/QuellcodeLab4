import os
import sys
import time
import socket
import picamera
import picamera.array
import numpy as np
#import src.webserver_stream
from src.webserver_stream import StreamingOutput, StreamingHandler, StreamingServer, set_page, output

class Camerasettings(picamera.PiCamera):
    """
        Objekte zum Erstellen verschiedener Kameraoptionen
        Klassenattribute:   cameraInUse : bool
        Objektattribute:    name : str
                            path : str
                            width : int
                            hight : int
                            rotation : int
                            effect : str
    """

    #Klassenattribute
    cameraInUse : bool = False

    #Standardkonstruktor: Intialisiert die Attribute des Objekts
    def __init__(self,  name: str = None,
                        path: str = None,
                        width: int = None,
                        hight: int = None,
                        rotation: int = None,
                        effect: str = None):

        if type(name) is str: self.set_name(name)
        else: self.set_name("unkown")

        if type(path) is str: self.set_path(path)
        else: self.set_path(os.getcwd())

        if type(width) is int: self.set_width(width)
        else: self.set_width(2592)

        if type(hight) is int: self.set_hight(hight)
        else: self.set_hight(1944)

        if type(rotation) is int: self.set_rotation(rotation)
        else: self.set_rotation(180)

        if type(effect) is str: self.set_effect(effect)
        else: self.set_effect("none")

    #GETTER, SETTER, DELETER Methoden
    #Attribut: name
    def get_name(self):
        return self._name
    def set_name(self, name: str):
        self._name = name
    def del_name(self):
        del self._name
    name = property(get_name, set_name, del_name)

    #Attribut: path
    def get_path(self):
        return self._path
    def set_path(self, path: str):
        if path[-1] != "/":
            self._path = path + "/" + self._name + "/"
        else:
            self._path = path[:-1] + "/" + self._name + "/"
        if not os.path.exists(self._path):
            os.makedirs(self._path)
    def del_path(self):
        del self._path
    path = property(get_path, set_path, del_path)

    #Attribut: width
    def get_width(self):
        return self._width
    def set_width(self, width: int):
        self._width = width
    def del_width(seld):
        del self._width
    width = property(get_width, set_width, del_width)

    #Attribut: hight
    def get_hight(self):
        return self._hight
    def set_hight(self, hight: int):
        self._hight = hight
    def del_hight(self):
        del self._hight
    hight = property(get_hight, set_hight, del_hight)

    #Attribut: rotation
    def get_rotation(self):
        return self._rotation
    def set_rotation(self, rotation: int):
        self._rotation = rotation
    def del_rotation(self):
        del self._rotation
    rotation = property(get_rotation, set_rotation, del_rotation)

    #Attribut: effect
    def get_effect(self):
        return self._effect
    def set_effect(self, effect: str):
        self._effect = effect
    def del_effect(self):
        del self._effect
    effect = property(get_effect, set_effect, del_effect)

#Override Methoden
    #Ausgabemethode f??r das Objekt ??berschreiben
    def __str__(self):
        return  "Name: " + str(self._name) + "\n" +\
                "Path: " + str(self._path) + "\n" +\
                "Width: " + str(self._width) + "\n" +\
                "Hight: " + str(self._hight) + "\n" +\
                "Rotation: " + str(self._rotation) + "\n" +\
                "Effect: " + str(self._effect)

#Klassenmethoden
    #alle m??glichen Kameraeffekte ausgeben
    @staticmethod
    def print_effects() -> "Listet alle Effekte auf":
        with picamera.PiCamera() as camera:
            print("Diese Effekte stehen zur Auswahl:")
            for effectName in camera.IMAGE_EFFECTS:
                print("\t" + effectName)
            camera.close()

#Kamerafunktionen
    def get_picture(self) -> "Fotoaufnahme":
        if not Camerasettings.cameraInUse:
            Camerasettings.cameraInUse = True
            with picamera.PiCamera(resolution = (self._width, self._hight)) as camera:
                camera.rotation = self._rotation
                camera.image_effect = self._effect
                try:
                    camera.start_preview()
                    time.sleep(0.75)
                    camera.capture(self._path + self._name + ".jpg")
                except PiCameraError as err:
                    print("unerwarteter Fehler: " + str(err))
                    camera.stop_preview()
                    camera.close()
                except KeyboardInterrupt:
                    camera.stop_preview()
                    camera.close()
                finally:
                    camera.stop_preview()
                    camera.close()
                    Camerasettings.cameraInUse = False
                    print("Foto wurde unter " + self._path + self._name + ".jpg" + " gespeichert.")
        else:
            print("Die Kamera wird aktuell verwendet.")

    def start_stream_funktioniert(self) -> "Webstream einschalten":
        stream(self._width, self._hight, self._rotation)

    def start_stream(self) -> "Webstream einschalten":
        if not Camerasettings.cameraInUse:
            Camerasettings.cameraInUse = True
            with picamera.PiCamera( resolution = (self._width, self._hight),
                                    framerate = 24) as camera:
                camera.rotation = self._rotation
                camera.image_effect = self._effect
                set_page(self._width, self._width)
                camera.start_recording(output, format='mjpeg')
                try:
                    address = ('', 8000)
                    server = StreamingServer(address, StreamingHandler)
                    server.serve_forever()
                    time.sleep(30)
                    server.shutdown()
                except KeyboardInterrupt:
                    camera.stop_recording()
                    camera.close()
                    server.shutdown()
                finally:
                    camera.stop_recording()
                    camera.close()

"""
with picamera.PiCamera(resolution='640x480', framerate=24) as camera:
    output = StreamingOutput()
    #Uncomment the next line to change your Pi's Camera rotation (in degrees)
    #camera.rotation = 90
    camera.start_recording(output, format='mjpeg')
    try:
        address = ('', 8000)
        server = StreamingServer(address, StreamingHandler)
        server.serve_forever()
    finally:
        camera.stop_recording()
"""

class MyMotionDetector(picamera.array.PiMotionAnalysis):

    motionDetectionEnable : bool = True

    def analyse(self, a):
        a = np.sqrt(
            np.square(a['x'].astype(np.float)) +
            np.square(a['y'].astype(np.float))
            ).clip(0, 255).astype(np.uint8)
        # If there're more than 10 vectors with a magnitude greater
        # than 60, then say we've detected motion
        if (a > 60).sum() > 10 and MyMotionDetector.motionDetectionEnable:
            print('Motion detected!')

def enable_motionDetector(timeInSeconds : int):
    with picamera.PiCamera( resolution = (640, 480),
                            framerate = 30) as camera:
        try:
            camera.start_recording(
            '/dev/null', format = 'h264',
            motion_output = MyMotionDetector(camera)
            )
            camera.wait_recording(timeInSeconds)
        except KeyboardInterrupt:
            camera.stop_recording()

"""
    alle angelegten Kameraeinstellungen werden in einer Liste gespeichert,
    Funktionen um die Liste zu bearbeiten:
        init_objList : Initialisierung  der Liste
        get_objList : Holen der Liste
        set_objListValue : Objekt zur Liste hinzuf??gen
        del_objListValue : Objekt aus der Liste l??schen
"""

objList : list = []

def init_objList():
    print("Die Objekliste wird Intialisiert...")
    try:
        objList.clear()
    except Exception as err:
        print("Unerwarteter Fehler: " + err)
        sys.exit()
    finally:
        print("Die Objektliste wurde  erfolgreich zur??ckgesetzt.")
        return

def get_objList() -> tuple:
    return objList

def set_objListValue(obj : Camerasettings):
    try:
        objList.append(obj)
    except Exception as err:
        print("Unerwarteter Fehler: " + err)
        return
    finally:
        print(obj._name + " wurde erfolgreich zur Objektliste hinzugef??gt.")
        return

def del_objListValue(obj : Camerasettings):
    try:
        objList.remove(obj)
    except Exception as err:
        print("Unerwarteter Fehler: " + err)
        return
    finally:
        print(obj._name + " wurde erfolgreich von der Objektliste gel??scht.")
        return
