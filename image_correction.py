import cv2
import numpy as np

class ImageCorrection:
    def __init__(self) -> None:
        pass
        
    def show_img(self, image):
        img = cv2.imread(image)
        cv2.imshow("image", img)
        cv2.waitKey(0)

    # Binarization refers to the process of turning RGB or greyscale images into pure black and pure white pixels
    def binarization(self, image):
        img = cv2.imread(image)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        img = cv2.adaptiveThreshold(img, 250, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 21, 10)
        thr, img = cv2.threshold(img, 220, 250, cv2.THRESH_BINARY)
        cv2.imwrite("temp/image.jpg", img)

    def color_inversion(self, image):
        img = cv2.imread(image)
        img = cv2.bitwise_not(img)
        cv2.imwrite("temp/image.jpg", img)

    def denoise(self, image):
        kernel = np.ones((1,1), np.uint8)
        img = cv2.imread(image)
        img = cv2.dilate(img, kernel, iterations=1)
        img = cv2.erode(img, kernel, iterations=1)
        img = cv2.morphologyEx(img, cv2.MORPH_CLOSE, kernel)
        img = cv2.medianBlur(img, 3)
        cv2.imwrite("temp/image.jpg", img)

    def full_edit(self, image):
        self.binarization(image)
        self.denoise(image)