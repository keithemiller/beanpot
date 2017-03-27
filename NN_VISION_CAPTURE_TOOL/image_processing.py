import numpy as np
import cv2
import argparse, sys, os, logging

# Logging stuff
logging.basicConfig(level=logging.DEBUG)#INFO)#DEBUG)
logger = logging.getLogger("face_detector")

class img_processor(object):
    """
    Image processor object
    """
    def __init__(self):
        if os.path.isfile('haarcascade_frontalface_default.xml'):
            self.face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
            if self.face_cascade == "":
                logger.error("No Cascade Classifier Found")
                logger.error("Exiting")
                sys.exit(1)
            else:
                logger.debug("CascadeClassifier Loaded Properly")

    def _test_correct_face_classifier(self):
        #TODO build this
        pass

def process_image(img):
    """
    Processes an opencv color image array.
    """
    logger.debug("Processing Image")

    # Convert to grayscale
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    faces = face_detect(gray_img)
    face_message = "Faces: " + str(faces)
    logger.debug(face_message)

    rois = pull_rois(img, faces)

    return img, faces, rois


def face_detect(gray_img):
    """
    Takes in an opencv gray image matrix and returns faces
    """
    # Loads the classifier
    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    logger.debug(face_cascade)
    # Uses face_cascade to find the faces
    faces = face_cascade.detectMultiScale(gray_img, 1.3, 5, minSize=((100,100)))

    return faces

def box_faces(img, faces):
    """
    Draws boxes around all of the faces detected in img
    """
    for (x,y,w,h) in faces:
        cv2.rectangle(img,(x,y),(x+w,y+h), (255,0,0),2)
    return img

def draw_text(img, text):
    if type(text) == int:
        text = str(text)

    cv2.putText(img,text,(50,100), cv2.FONT_HERSHEY_SIMPLEX, 1,(255,255,255),2)
    return img

def draw_label(img, label, x, y):
    label = str(label)
    cv2.putText(img,label,(x,y), cv2.FONT_HERSHEY_SIMPLEX, 1,(255,255,255),2)
    return img

def pull_rois(img, faces):
    """
    Cuts out each of the faces from the frame
    """
    rois = []

    for (x,y,w,h) in faces:
        rois.append(img[y:y+h, x:x+w])
    return rois

def show_image(img):
    """
    Creates a window and shows the image. Press 0 to close the window and
    continue executing the program
    """
    win = cv2.namedWindow('img', cv2.WINDOW_AUTOSIZE)
    cv2.imshow('img', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def process_image_file(img_file):
    """
    Process an image file.

    This Function returns the image with the faces boxed. It also contains the
    rois (the cutouts of the faces from the image).
    """
    # Debug Message
    logger.debug("Processing Image")

    # Load the image in as a numpy array
    img = cv2.imread(img_file)


    # When loading an image file Macs will have the image rotated.
    # This block will rotate the image to its correct position
    """
    if sys.platform == "darwin":
        logger.info("Using mac, rotating image")
        rows,cols,depth = img.shape
        M = cv2.getRotationMatrix2D((cols/2,rows/2),270,1)
        img = cv2.warpAffine(img,M,(cols,rows))
    """

    # We process the image, log where they are, and then box them
    img, faces, rois = process_image(img)
    face_message = "Faces: " + str(faces)
    logger.debug(face_message)
    img = box_faces(img, faces)

    #show_image(img)


    return img, faces, rois

def process_video_file(vid_file):
    """
    Processes a video frame by frame
    """
    # Treats the video as a capture device
    while(cap.isOpened()):
        ret, frame = cap.read()

        # Exits if there are no more frames (aka video ended)
        if frame is None:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        if sys.platform == "darwin":
            logger.debug("rotating image for Mac platform")
            rows,cols = gray.shape
            M = cv2.getRotationMatrix2D((cols/2,rows/2),270,1)
            gray = cv2.warpAffine(gray,M,(cols,rows))

        faces = face_detect(gray)
        if len(faces) is not 0:
            logger.debug(len(faces))
            cv2.imshow('frame',box_faces(gray, faces))
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    cap.release()
    cv2.destroyAllWindows()
