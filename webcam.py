import pygame
import pygame.camera
import ctypes
from api import processRequest
import json as jjson
from multiprocessing import Process
from PIL import Image
import matplotlib.pyplot as plt
from pygame.locals import *

#Example Taken from http://www.pygame.org/docs/tut/camera/CameraIntro.html

pygame.init()
pygame.camera.init()

_url_face = 'https://api.projectoxford.ai/face/v1.0/detect'
_face_key = "576ef033c83d4dc2b27cd1480129ecae"

THRESH = 50

def get_faces_frame(img):

    headers = dict()
    headers['Ocp-Apim-Subscription-Key'] = _face_key
    headers['Content-Type'] = 'application/octet-stream'

    params = dict()
    params['returnFaceId'] = 'true'
    params['returnFaceLandmarks'] = 'true'
    params['returnFaceAttributes'] = 'age'

    json = None
    data = img

    result = processRequest(_url_face, json, data, headers, params)
    #print("RESULTS:")
    #print(jjson.dumps(result, indent=4))

    return result

def process_position(json):

    midx = 380
    midy = 230

    print(json)
    try:
        face = json[0]

        print(face["faceLandmarks"]["pupilLeft"]["x"])
        #print(face["faceLandmarks"]["pupilLeft"]["y"])
        print(face["faceLandmarks"]["pupilRight"]["x"])
        #print(face["faceLandmarks"]["pupilRight"]["y"])
        print(face["faceLandmarks"]["noseTip"]["x"])
        print(face["faceLandmarks"]["noseTip"]["y"])
        leftx = face["faceLandmarks"]["pupilLeft"]["x"]
        #lefty=face["faceLandmarks"]["pupilLeft"]["y"]
        rightx = face["faceLandmarks"]["pupilRight"]["x"]
        #righty=face["faceLandmarks"]["pupilRight"]["y"]
        x = face["faceLandmarks"]["noseTip"]["x"]
        y = face["faceLandmarks"]["noseTip"]["y"]

        print("MIDX:", midx)#, "MIDY:", midy)

        # left turn
        """if leftx > midx:
            print("LEFT TURN")
        if rightx < midx:
            print("RIGHT TURN")"""
        if x > midx:
            print("LEFT TURN")
        if x < midx:
            print("RIGHT TURN")
        if y > midy:
            print("DOWN TURN")
        if y < midy:
            print("UP TURN")

    except:
        pass

        #left pup: y more x less
        #right pup: y less x less
        # right turn
        #left pup: y less x more
        #right pup: y more x more


class Capture(object):
    def __init__(self):
        self.size = (640,480)
        # create a display surface. standard pygame stuff
        self.display = pygame.display.set_mode(self.size, 0)
        self.video = []
        self.going = True
        
        # this is the same as what we saw before
        self.clist = pygame.camera.list_cameras()
        if not self.clist:
            raise ValueError("Sorry, no cameras detected.")
        self.cam = pygame.camera.Camera(self.clist[0], self.size)
        self.cam.start()

        # create a surface to capture to.  for performance purposes
        # bit depth is the same as that of the display surface.
        self.snapshot = pygame.surface.Surface(self.size, 0, self.display)

    def get_and_flip(self):
        # if you don't want to tie the framerate to the camera, you can check 
        # if the camera has an image ready.  note that while this works
        # on most cameras, some will never return true.
        if self.cam.query_image():
            self.snapshot = self.cam.get_image(self.snapshot)
            self.video.append(self.snapshot)
            if len(self.video) % 10 == 0:
                i = len(self.video)
                vid = self.video[i-1]
                print(i)
                #v = pygame.surfarray.pixels2d(self.video[i-1])
                data = pygame.image.tostring(self.video[i-1], 'RGBA')
                pil_image = Image.frombytes("RGBA", self.size, data)
                from StringIO import StringIO
                zdata = StringIO()
                pil_image.save(zdata, 'JPEG')
                result = get_faces_frame(zdata.getvalue())
                process_position(result)


        # blit it to the display surface.  simple!
        self.display.blit(self.snapshot, (0,0))
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            pass
        #pygame.display.update()
        pygame.display.flip()

    def main(self):
        going = True
        while going:
            events = pygame.event.get()
            for e in events:
                if e.type == pygame.QUIT or (e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE):
                    # close the camera safely
                    self.cam.stop()
                    going = False

            self.get_and_flip()
        return self.video

