"""
This script will capture photos until there are enough to train the neural net
"""

import cv2
import os, sys, logging
from image_processing import show_image, process_image, box_faces, draw_text

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("nn_capture")

class nn_capture(object):
    """
    Takes pictures and stores them until there are enough
    """

    path_to_pics = None

    def __init__(self, path_to_pics):
        self.path_to_pics = path_to_pics

    def preview(self, capture_device=cv2.VideoCapture(0), boxes=True):
        logger.debug("Preview")
        counter = 0
        while(capture_device.isOpened()):
            ret, frame = capture_device.read()
            print ret

            if frame is None:
                break

            img, faces, rois = process_image(frame)
            if len(rois) == 1:
                counter += 1

            if boxes:
                img = box_faces(img, faces)
            img = draw_text(img, counter)

            cv2.imshow("Preview", img)
            roi_num = 0
            for roi in rois:
                roi_name = "roi" + str(roi_num)
                cv2.imshow(roi_name, roi)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    def capture(self, name, capture_device=cv2.VideoCapture(0), boxes=True):
        logger.debug("Capture")

        path_original = os.path.join(self.path_to_pics, "original", name)
        path_rois = os.path.join(self.path_to_pics, "rois", name)
        try:
            os.mkdir(path_original)
            os.mkdir(path_rois)
        except OSError:
            logger.error("Capture directory already made")
            print path_original
            sys.exit(1)

        counter = 0
        while(capture_device.isOpened() and (counter < 100)):
            ret, frame = capture_device.read()
            print ret

            if frame is None:
                break

            img, faces, rois = process_image(frame)
            if len(rois) == 1:
                image_name = "image-" + str(counter) + ".jpg"
                image_path = os.path.join(path_original, image_name)
                roi_path = os.path.join(path_rois, image_name)
                print image_path
                cv2.imwrite(image_path, img)
                cv2.imwrite(roi_path, rois[0])
                counter += 1

            if boxes:
                img = box_faces(img, faces)

            text = "Make some faces! " + str(counter) + "/100"
            img = draw_text(img, text)

            cv2.imshow("Preview", img)
            roi_num = 0

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

if __name__=="__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Takes in the name of the user whose photos we are taking")
    parser.add_argument("name", type=str, help="Name of the user")
    args = parser.parse_args()

    logger.debug("Starting " + str(args))
    try:
        path_to_pics = os.environ.get('PICROOT')
        """if path_to_pics == "":
            raise KeyError"""
    except KeyError:
        print "Make sure to source the setup_env script"
        sys.exit(1)

    cappy = nn_capture(path_to_pics)
    cappy.capture(args.name)

    logger.debug("Done")
