import cv2
from PIL import Image
import numpy as np

# This class defines image correction methods to improve the quality of the input image and creates a method to
# execute a series of corrections that generally yield the best OCR results.
class ImageCorrection:
    def __init__(self) -> None:
        pass
    
    # This method creates a window and displays the image
    def show_img(self, path, title="image"):
        img = cv2.imread(path)
        cv2.imshow(title, img)
        cv2.waitKey(0)

    # Main function of the ImageCorrection class that activates the image correction pipeline
    def full_edit(self, path):
       
        # INCREASE CONTRAST
            
        # Opens the image twice. img will be used to create a mask, 
        # while img_original will be the image the mask is applied on
        img = cv2.imread(path)
        img_original = cv2.imread(path)

        # Convert the images to grayscale
        print("Converting images to grayscale")
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        img_original = cv2.cvtColor(img_original, cv2.COLOR_BGR2GRAY)

        # Creates a mask for the white and black values
        print("Creating white and black masks")
        mask = cv2.adaptiveThreshold(img_original, 250, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 101, 10)
        cv2.imshow("mask", mask)
        cv2.waitKey(0)
        mask_inv = cv2.bitwise_not(mask)
        cv2.imshow("mask_inv", mask_inv)
        cv2.waitKey(0)

        # Apply histogram equalization to increase contrast
        print("Increasing contrast")
        clahe = cv2.createCLAHE(clipLimit=4.1, tileGridSize=(20, 20))
        img_contrast = clahe.apply(img)

        # Merges the original image with the contrasted image to preserve white values 
        # from original and black values from contrasted image
        print("Merging images and masks")
        img = cv2.bitwise_and(img_original, img_original, mask=mask_inv)
        img = cv2.add(img, img_contrast, mask=mask)
        cv2.imshow("Contrast", img)
        cv2.waitKey(0)


        #BINARIZARION
        # Binarization refers to the process of turning RGB 
        # or greyscale images into pure black and pure white pixels

        # threshold takes the image and intensifies the contrast between black and white
        thr, img = cv2.threshold(img, 220, 250, cv2.THRESH_BINARY)
        cv2.imshow("Binarization", img)
        cv2.waitKey(0)

        # ERODE
        # This process makes the white regions smaller and white pixels in black areas disappear

        # Creates a 2x2 kernel full of ones
        kernel = np.ones((2,2), np.uint8)

        # Inverts the color of pixels in the image by inverting the bytes (black becomes white, etc.)
        # For binary images, this is done to apply the operations only to the text (which would become white)
        img = cv2.bitwise_not(img)

        # Since the kernel is a 2x2 matrix, then we are considering a 2x2 region around a pixel
        # The erosion operation finds the minimum value in the area covered by the kernel
        # And changes all the pixels in the area to this minimum value
        img = cv2.erode(img, kernel, iterations=1)

        cv2.imshow("Erosion", img)
        cv2.waitKey(0)

        #DILATION
        # Dilation makes white areas get larger and black pixels in white regions disappear
        
        # Since the kerner is a 2x2 matrix, then we are considering a 2x2 region around a pixel
        # The dilate operation finds the maximum value in the area covered by the kernel
        # And changes all the pixels in the area to this maximum value
        img = cv2.dilate(img, kernel, iterations=1)

        cv2.imshow("Dilation", img)
        cv2.waitKey(0)

        # Invert the colors to their original byte values
        img = cv2.bitwise_not(img)

        #DENOISING

        # MorphologyEx applies a closing operation (MORPH_CLOSE) to the area covered by the kernel
        # A closing operation fills black holes in white regions on binary images
        # The opposite operation (MORPH_OPEN) removes white dots in black regions on binary images
        img = cv2.morphologyEx(img, cv2.MORPH_CLOSE, kernel)

        # medianBlur calculates the median of a 3x3 region around each pixel and sets the pixel value to that median
        img = cv2.medianBlur(img, 3)
        cv2.imshow("Denoise", img)
        cv2.waitKey(0)

        #SHARPENING
        
        laplacian = np.uint8(np.absolute(cv2.Laplacian(img, cv2.CV_64F, ksize=3)))
        img = cv2.addWeighted(img, 1.5, laplacian, -0.4, 0)
        cv2.imshow("Sharpening", img)
        cv2.waitKey(0)

        # Save image and display result
        cv2.imwrite(path, img)
        self.show_img(path, "Final Result")
        cv2.waitKey(0)