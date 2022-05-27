import os
import time
import socket
import picamera
import picamera.array
import numpy as np
from src.webserver_stream import StreamingOutput, StreamingHandler, StreamingServer, set_page

wd = os.getcwd()

class Camerasettings(picamera.PiCamera):
    """
        Objekte zum Erstellen verschiedener Kameraoptionen
        Klassenattribute:   cameraInUse : bool
        Objektattribute:    name : str
                            path : str
                            widht : int
                            hight : int
                            rotation : int
                            effect : str
    """

    #Klassenattribute
    cameraInUse : bool = False

    #Standardkonstruktor: Intialisiert die Attribute des Objekts
    def __init__(self,  objName: str = None,
                        objPath: str = None,
                        objWidth: int = None,
                        objHight: int = None,
                        objRotation: int = None,
                        objEffect: str = None):

        if type(objName) is str:
            self.set_name(objName)
        else:
            self.set_name("unkown")

        if type(objPath) is str:
            self.set_path(objPath)
        else:
            self.set_path(wd)

        if type(width) is int: self.set_width(width)
        else: self.set_width(1024)

        if type(hight) is int: self.set_hight(hight)
        else: self.set_hight(768)

        if type(rotation) is int: self.set_rotation(rotation)
        else: self.set_rotation(180)

        if type(effect) is str: self.set_effect(effect)
        else: self.set_effect("none")

    #GETTER, SETTER, DELETER Methoden
    #Attribut: name
    def get_name(self):
        return self.name
    def set_name(self, objName: str):
        self.name = objName
    def del_name(self):
        del self.name
    name = property(get_name, set_name, del_name)

    #Attribut: path
    def get_path(self):
        return self.path
    def set_path(self, path: str):
        if path[-1] == "/":
            self.path = path[:-1] + "/" + self.name
        else:
            self.path = path + "/" + self.name
    def del_path(self):
        del self.path
    path = property(get_path, set_path, del_path)

    #Attribut: width
    def get_width(self):
        return self.width
    def set_width(self, width: int):
        self.width = width
    def del_width(seld):
        del self.width
    width = property(get_width, set_width, del_width)

    #Attribut: hight
    def get_hight(self):
        return self.hight
    def set_hight(self, hight: int):
        self.hight = hight
    def del_hight(self):
        del self.hight
    hight = property(get_hight, set_hight, del_hight)

    #Attribut: rotation
    def get_rotation(self):
        return self.rotation
    def set_rotation(self, rotation: int):
        self.rotation = rotation
    def del_rotation(self):
        del self.rotation
    rotation = property(get_rotation, set_rotation, del_rotation)

    #Attribut: effect
    def get_effect(self):
        return self.effect
    def set_effect(self, effect: str):
        self.effect = effect
    def del_effect(self):
        del self.effect
    effect = property(get_effect, set_effect, del_effect)

#Override Methoden
    def __str__(self):
        return  "Name: " + str(self.name) + "\n" +\
                "Path: " + str(self.path) + "\n" +\
                "Width: " + str(self.width) + "\n" +\
                "Hight: " + str(self.hight) + "\n" +\
                "Rotation: " + str(self.rotation) + "\n" +\
                "Effect: " + str(self.effect)

#Klassenmethoden definieren um die Kamera der Klasse
#zugänglich zu machen
    #alle möglichen Kameraeffekte ausgeben
    @staticmethod
    def print_effects():
        with picamera.PiCamera() as camera:
            print("Diese Effekte stehen zur Auswahl:")
            for effectName in camera.IMAGE_EFFECTS:
                print("\t" + effectName)
            camera.close()
    """
        @classmethod
        def init(cls):
            cls.Camerasettings.camera.start_preview()
            sleep(2)
            return "Kamera ist einsatzbereit"

        @classmethod
        def exit():
            cls.Camerasettings.camera.close()
    """

#Kamerafunktionen
    def get_picture(self, cameraWarmup):
        if not Camerasettings.cameraInUse:
            Camerasettings.cameraInUse = True
            with picamera.PiCamera(resolution = (self.width, self.hight)) as camera:
                camera.rotation = self.rotation
                camera.image_effect = self.effect
                try:
                    camera.start_preview()
                    time.sleep(cameraWarmup)
                    camera.capture(self.path + ".jpg")
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
                    print("Foto wurde unter " + self.path + ".jpg" + " gespeichert.")
        else:
            print("Die Kamera wird aktuell verwendet.")

    def start_stream(self):
        if not Camerasettings.cameraInUse:
            Camerasettings.cameraInUse = True
            with picamera.PiCamera(  resolution = (self.width, self.hight),
                            rotation = self.rotation,
                            effect = self.effect,
                            framerate = 24) as camera:
                output = StreamingOutput()
                camera.start_recording(output, format='mjpeg')
                try:
                    address = ('', 8000)
                    server = StreamingServer(address, StreamingHandler)
                    server.serve_forever()
                except KeyboardInterrupt:
                    camera.stop_recording()
                    camera.close()
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

def enable_motionDetector(timeInSeconds):
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

objList : list = []

def init_objList():
    print("Die Objekliste wird Intialisiert...")
    try:
        objList.clear()
    except Exception as err:
        print("Unerwarteter Fehler: " + err)
        return
    finally:
        print("Die Objektliste wurde  erfolgreich zurückgesetzt.")
        return

def get_objList():
    return objList

def set_objListValue(obj : Camerasettings) -> Camerasettings:
    try:
        objList.append(obj)
    except Exception as err:
        print("Unerwarteter Fehler: " + err)
    finally:
        print(obj.name + " wurde erfolgreich zur Objektliste hinzugefügt.")
        return

def del_objListValue(obj : Camerasettings) -> Camerasettings:
    try:
        objList.remove(obj)
    except Exception as err:
        print("Unerwarteter Fehler: " + err)
    finally:
        print(obj.name + " wurde erfolgreich von der Objektliste gelöscht.")
        return
