import sys
import numpy as np

class ImageVehicle:
    """docstring for ImageVehicle."""

    def __init__(self, image:str, pathVideo:str, apparitionTime:((int,int,int,int,int,int)),id:int ):

        self._image = image
        self._pathVideo = pathVideo
        self._descriptor = 0
        self._apparitionTime = apparitionTime
        self._id = id

    def _get_image(self)->str:
        return self._image

    def _set_image(self,image:str):
        sys.stderr.write("Write access forbidden for \"image\"\n")

    def _get_pathVideo(self)->str:
        return self._pathVideo

    def _set_pathVideo(self,path:str):
        sys.stderr.write("Write access forbidden for \"pathVideo\"\n")

    def _get_descriptor(self)->float:
        return self._descriptor

    def _set_descriptor(self,descriptor:float):
        self._descriptor = descriptor

    def _get_apparitionTime(self)->((int,int,int,int,int,int)):
        return self._apparitionTime

    def _set_apparitionTime(self,apparitionTime):
        sys.stderr.write("Write access forbidden for \"apparitionTime\"\n")

    def _get_id(self)->int:
        return self._id

    def _set_id(self,id):
        sys.stderr.write("Write access forbidden for \"id\"\n")

    def __str__(self):
        image = "Image: " + self.image + ", "
        path = "Path: " + self.pathVideo + ", "
        desc = "Descriptor: " + str(self.descriptor) + ", "
        apptime = "ApparitionTime: " + str(self.apparitionTime) + ", "
        id = "ID: " + str(self.id) + "\n"

        return image + path + desc + apptime + id

    image = property(_get_image, _set_image)
    pathVideo = property(_get_pathVideo, _set_pathVideo)
    descriptor = property(_get_descriptor, _set_descriptor)
    apparitionTime = property(_get_apparitionTime, _set_apparitionTime)
    id = property(_get_id, _set_id)



# Unit test here:
# python3 ImageVehicle.py
if __name__ == '__main__':

    # year, months, day, hour, minute, second
    time = ((2020,12,25,23,00,00))
    # build ImageVehicle
    iv = ImageVehicle("./img.png","/example",time,18)

    # set a descriptor (see _set_descriptor(self,descriptor:float))
    iv.descriptor = 42.4

    # Info about iv
    print(iv)

    # get Attributes
    print(iv.image)
    print(iv.pathVideo)
    print(iv.descriptor)
    print(iv.apparitionTime)
    print(iv.id)
