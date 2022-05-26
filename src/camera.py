from picamera import PiCamera
from time import sleep
import os

wd = os.getcwd()

class Camerasettings():
#Standardkonstruktor
    def __init__(self):
        self._name = "unknown"
        self._path = wd + "/" + self._name
        self._width = 1024
        self._hight = 768
        self._rotation = 180
        self._effect = "none"

#SETTER, GETTER, DELETER Methoden
    #Attribut: name
    def set_user(self, name):
        self._name = name
    def get_name(self):
        return self._name
    def del_name(self):
        del self._name
    name = property(set_name, get_name, del_name)

    #Attribut: path
    def set_path(self, path):
        self._path = path
    def get_path(self):
        return self._path
    def del_path(self):
        del self._path
    path = property(set_path, get_path, del_path)

    #Attribut: width
    def set_width(self, width):
        self._width = width
    def get_width(self):
        return self._width
    def del_width(seld):
        del self._width
    width = property(set_width, get_width, del_width)

    #Attribut: hight
    def set_hight(self, hight):
        self._hight = hight
    def get_hight(self):
        return self._hight
    def del_hight(self):
        del self._hight
    hight = property(set_hight, get_hight, del_hight)

    #Attribut: rotation
    def set_rotation(self, rotation):
        self._rotation = rotation
    def get_rotation(self):
        return self._rotation
    def del_rotation(self):
        del self._rotation
    rotation = property(set_rotation, get_rotation, del_rotation)

    #Attribut: effect
    def set_effect(self, effect):
        self._effect = effect
    def get_effect(self):
        return self._effect
    def del_effect(self):
        del self._effect
    effect = property(set_effect, get_effect, del_effect)
