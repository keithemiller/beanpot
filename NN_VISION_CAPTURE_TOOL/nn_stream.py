"""
Streams an example of our face detection, recognition, and tracking algorithms
"""

from subprocess import call, Popen, PIPE
import cv2, os, sys, logging
from image_processing import (show_image, process_image, box_faces, draw_text,
draw_label)


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("MDR")

class nn_capture(object):
    """
    Takes pictures and stores them until there are enough
    """

    def __init__(self, docker_container_name="9155f23a7f10"):
        self.container = docker_container_name

    def _send_to_openface(self, roi_name):
        command = "docker cp " + roi_name + " 82a6cfcf38b5:/root/openface/PIX"
        call(command.split())
        command2 = "docker exec 82a6cfcf38b5  /root/openface/demos/classifier.py infer /classifier.pkl /root/openface/PIX"
        #ans = call(command2.split())
        p = Popen(command2.split(), stdin=PIPE, stdout=PIPE, stderr=PIPE)
        output, err = p.communicate()
        spl = output.split()
        if len(spl) > 5:
            ret = spl[4]
        else:
            ret = "???"
        return ret

    def preview(self, capture_device=cv2.VideoCapture(0), boxes=True):
        logger.debug("Preview")
        counter = 0
        #for x in range(15):
        while(capture_device.isOpened()):
            ret, frame = capture_device.read()
            logger.debug(ret)

            if frame is None:
                break

            img, faces, rois = process_image(frame)
            if len(rois) == 1:
                counter += 1

            if boxes:
                img = box_faces(img, faces)

            roi_num = 0
            labels = []
            for roi in rois:
                roi_name = "roi" + str(roi_num) + ".png"
                cv2.imwrite(roi_name, roi)
                label = self._send_to_openface(roi_name)
                print "LABLE:", label
                labels.append(label)

            label_num = 0
            print "LABELS: ", labels
            right = True
            up = True
            print
            for (x,y,w,h) in faces:
                img = draw_label(img, labels[label_num], x, y-10)
                label_num += 1
                #if (x + (w/2))> len(img) / 2:
                horiz = (x+w/2.0) - (len(img) /2.0)
                if horiz > 0:
                    right = False
                if (y+ (h/2)) < len(img[0]) / 2:
                    up = False

            if right:
                text = "TURN RIGHT"
            else:
                text = "TURN LEFT"
            if up:
                text += "|TURN UP"
            else:
                text += "|TURN DOWN"

            #img = draw_text(img, text)


            cv2.imshow("Video Processing Demo", img)


            if cv2.waitKey(1) & 0xFF == ord('q'):
                break


if __name__=='__main__':

    cappy = nn_capture()
    #import profile
    #profile.run("cappy.preview()")
    cappy.preview()

    # Load the video
    #cappy.preview(capture_device=cv2.VideoCapture("../MDR/tracking_test.mov"))
