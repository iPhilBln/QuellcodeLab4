from picamera import PiCamera
from time import sleep
import os

wd = os.getcwd()

class Camerasettings(PiCamera):
    """Objekte zum erstellen verschiedener Kameraoptionen"""

    #Klassenattribute
    camera: PiCamera = PiCamera()
    _name: str = "unknown"
    _path: str = wd + "/" + _name
    _widht: int = 1024
    _hight: int = 768
    _rotation: int = 180
    _effect: str = "none"

    #Standardkonstruktor: Intialisiert die Attribute des Objekts
    def __init__(self,  name: str = None,
                        path: str = None,
                        width: int = None,
                        hight: int = None,
                        rotation: int = None,
                        effect: str = None):

        if type(name) is str:
            self._name = name

        if type(path) is str:
            self._path = path

        if type(width) is int:
            self._width = widht

        if type(hight) is int:
            self._hight = hight

        if type(rotation) is int:
            self._rotation = rotation

        if type(effect) is str:
            self._effect = effect

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
        if path[-1] == "/":
            self._path = path[:-1] + "/" + self._name
        else:
            self._path = path + "/" + self._name
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
    def __str__(self):
        return  "Name: " + str(self._name) + "\n" +\
                "Path: " + str(self._path) + "\n" +\
                "Width: " + str(self._widht) + "\n" +\
                "Hight: " + str(self._hight) + "\n" +\
                "Rotation: " + str(self._rotation) + "\n" +\
                "Effect: " + str(self._effect)

#Klassenmethoden definieren um die Kamera der Klasse
#zugänglich zu machen
    #alle möglichen Kameraeffekte ausgeben
    @staticmethod
    def print_effects():
        print("Diese Effekte stehen zur Auswahl:")
        for effectName in Camerasettings.camera.IMAGE_EFFECTS:
            print("\t" + effectName)

    @staticmethod
    def init():
        Camerasettings.camera.start_preview()
        sleep(2)

    @staticmethod
    def exit():
        Camerasettings.camera.close()

#Kamerafunktionen
    def get_picture(self):
        try:
            Camerasettings.camera.resolution = (self._width, self._hight)
            Camerasettings.camera.rotation = self._rotation
            Camerasettings.camera.image_effect = self._effect
            Camerasettings.camera.capture(self._path + ".jpg")
        except PiCameraError as err:
            print("unexpectet error: " + str(err))
            return
        except KeyboardInterrupt:
            Camerasettings.camera.close()
        finally:
            print("Foto wurde unter " + self._path + ".jpg" + " gespeichert.")
