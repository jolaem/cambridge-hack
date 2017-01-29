#!/usr/bin/python

from __future__ import print_function
from multiprocessing import Process, Queue
from webcam import Capture

import time


foo = Capture()
video = foo.main()
print(len(video))

"""def get_vid():
    print("starting1")
    time.sleep(5)
    #foo.going = False
    #print(foo.video)
    print("end1")

def test():
    print("starting2")
    time.sleep(2)
    print("end2")
    print(len(foo.video))

capture_vid = Process(target=foo.main, name="capture_vid")
get_vid = Process(target=get_vid, name="get_vid")
testing = Process(target=test, name="test")

get_vid.start()
testing.start()
capture_vid.start()"""

#video = foo.main()
#print(len(video))