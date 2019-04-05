from PIL import Image
import os

for nm in os.listdir("temp1"):
    if(nm=='desktop.ini' or nm=='convert.py'):
        continue
    im = Image.open("temp1/"+nm)
    rgb_im = im.convert('RGB')
    extn = nm.split(".")[-1]
    rgb_im.save("/Users/faiza/Desktop/Facial-Expression-Detection-master/Temp/"+nm.replace(extn,"jpeg").rstrip())

## This program first ensures if the face of a person exists in the given image or not then if it exists, it crops
## the image of the face and saves to the given directory.

## Importing Modules
import cv2


#################################################################################

##Make changes to these lines for getting the desired results.

## DIRECTORY of the images

directory = os.path.join(os.getcwd(), "Temp" )

## directory where the images to be saved:
f_directory = os.path.join(os.getcwd(), "images" ,"final" )

################################################################################
            
def facecrop(image):
    ## Crops the face of a person from any image!

    ## OpenCV XML FILE for Frontal Facial Detection using HAAR CASCADES.
    facedata = "haarcascade_frontalface_alt.xml"
    cascade = cv2.CascadeClassifier(facedata)

    ## Reading the given Image with OpenCV
    img = cv2.imread(image, 1)

    try:
    ## Some downloaded images are of unsupported type and should be ignored while raising Exception, so for that
    ## I'm using the try/except functions.

        minisize = (img.shape[1],img.shape[0])
        miniframe = cv2.resize(img, minisize)

        faces = cascade.detectMultiScale(miniframe)
        
        for f in faces:
            x, y, w, h = [ v for v in f ]
            cv2.rectangle(img, (x,y), (x+w,y+h), (0,255,0), 2)

            sub_face = img[y:y+h, x:x+w]

            f_name = image.split('\\')
            f_name = f_name[-1]

            ## Change here the Desired directory.
            cv2.imwrite(os.path.join(f_directory , f_name) , sub_face)
            print ("Writing: " + image)
            os.remove("Temp/" + image.split('\\')[-1])

    except:
        pass

if __name__ == '__main__':
    images = os.listdir(directory)
    i = 0
    
    for img in images:
        file = os.path.join(directory , img)
        print (i)
        facecrop(file)
        i += 1

