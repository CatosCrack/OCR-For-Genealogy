import cv2
from external_resources import Drive
from PIL import Image
import io
from image_correction import ImageCorrection
import numpy as np
from recognition import Recognition
import matplotlib.pyplot as plt
import pytesseract

rec = Recognition()
drive = Drive()
images = drive.get_drive_files()
correction = ImageCorrection()

# Main function of the ImageCorrection class that activates the image correction pipeline
def full_edit(path):
    correction.show_img(path, "original")

    correction.upsampling(path)
    correction.show_img(path, "upsampled")

    #correction.contrast(path)
    #correction.show_img(path, "contrast")

    correction.binarization(path)
    correction.show_img(path, "binarization")

    correction.denoise(path)
    correction.show_img(path, "denoise")

    correction.erode(path)
    correction.show_img(path, "erode")

    correction.dilation(path)
    correction.show_img(path, "dilation")

    correction.sharpening(path)
    correction.show_img(path, "sharpening")


for image in images:
    print("................................................")
    print(image)
    id = images[image]
    #for i in range (3, 200, 5):
        #try:
            #i = i/10
    img = Image.open(io.BytesIO(drive.download_image(id)))
    img.save(r"test/test1.tif")
    full_edit(r"test/test1.tif")
        #except:
            #pass

'''
for image in images:
    print("................................................")
    print(image)
    id = images[image]
    inferences = rec.extract_ocr_data(id)

    for inference in inferences:
        print(inference["text"])

    rec.plot_boxes(id, inferences)

    print("+++++++++++")

    inferences = rec.recognitionPipeline(id)

    for inference in inferences:
        print(inference["text"])
        
    rec.plot_boxes(id, inferences)
'''
    