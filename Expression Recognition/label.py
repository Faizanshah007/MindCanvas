import label_image

import sys, os
import time

import atexit
import pickle
import cv2

# atexit.register(print, "Exiting label")
atexit.register(label_image.end)  # Safely Exit

@atexit.register
def release_switch():
    try:
        os.unlink(".\\..\\switch")

    except:
        pass

resize = 4  # For resizing the image

# We load the xml file
classifier = cv2.CascadeClassifier('haarcascade_frontalface_alt.xml')

while True:
    webcam = cv2.VideoCapture(0)  # Using default WebCam connected to the PC.

    if(webcam.isOpened()):
        break

    webcam.release()

atexit.register(webcam.release)  # Release webcam before exit

#Capturing a smaller image for speed purposes
webcam.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
webcam.set(cv2.CAP_PROP_FRAME_HEIGHT, 360)
webcam.set(cv2.CAP_PROP_FPS, 15)

while True:
    # Check for termination condition
    try:
        Cond_f = open(".\\..\\switch","rb")

        if(pickle.load(Cond_f) == "off"):
            Cond_f.close()
            break

        Cond_f.close()

    except:
        pass

    exprfile = open(".\\..\\expression_output", "wb")
    exprfile.truncate()
    exprfile.close()

    im = webcam.read()[1]  # Image data captured by webcam
    im = cv2.flip(im, 1, 0)  # Flip to act as a mirror

    # Resize the image to speed up detection
    mini = cv2.resize(im, (int(im.shape[1] / resize), int(im.shape[0] / resize)))

    # Detect MultiScale / faces
    faces = classifier.detectMultiScale(mini)

    # Naming the expression found
    text = ''

    # Draw rectangles around each face
    for f in faces:
        (x, y, w, h) = [v * resize for v in f]  #Scale the shapesize backup
        cv2.rectangle(im, (x, y), (x + w, y + h), (0, 255, 0), 4)
        sub_face = im[y : y + h, x : x + w]  #Save just the rectangle faces in SubRecFaces
        FaceFileName = "test.jpg"  #Saving the current image from the webcam for testing.
        cv2.imwrite(FaceFileName, sub_face)
        text = label_image.run()  # Getting the Result from the label_image file, i.e., Classification Result.
        ##text = text.title()# Title Case looks Stunning.
        ##font = cv2.FONT_HERSHEY_TRIPLEX
        ##cv2.putText(im, text,(x+w,y), font, 1, (0,0,255), 2)

    # Refreshing Display
    ##cv2.imshow('cApTuRe_window',   im)  # Open display
    ##key = cv2.waitKey(1)  # Close display after 1ms

    # if Esc key is press then break out of the loop
    ##if key == 27:  #The Esc key
    ##    sys.exit()
