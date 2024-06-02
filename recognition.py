import io
import pytesseract
import spacy
from PIL import Image
from external_resources import Drive
from image_correction import ImageCorrection
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

drive = Drive()
correction = ImageCorrection()

class Recognition:
    def __init__(self) -> None:
        pass
        
    def extract_ocr_data(self, id):
        
        file = Image.open(io.BytesIO(drive.download_image(id)))
        
        path = r"temp/image.jpg"
        file.save(path)
        correction.full_edit(path)
        file = Image.open(path)

        # For reference to use PyTesseract, visit https://pypi.org/project/pytesseract/
        '''
        image_to_data() returns a dict with keys left, top, width, height where:
            - left: distance from top-left corner of box to left border of the image
            - top: distance from top-left corner of box to top border of the image
        conf dictates whether the box is a block of text or a word. -1 means a block of text.
        '''
        inference = pytesseract.image_to_data(file, lang="spa", output_type="dict")
        #print(inference)
            
        ls = []
        for i in range(0, len(inference["left"])):
            if inference["conf"][i] != -1:
                dc = {}
                dc["text"] = inference["text"][i]
                dc["left"] = inference["left"][i]
                dc["top"] = inference["top"][i]
                dc["width"] = inference["width"][i]
                dc["height"] = inference["height"][i]
                ls.append(dc)

        return ls
    
    def identify_names(self, data):

        name_data = []

        nlp = spacy.load("es_core_news_lg")

        for word in data:
            doc = nlp(word["text"])
            for ent in doc.ents:
                if ent.label_ == "PER":
                    name_data.append(word)
        
        return name_data
    
    def plot_boxes(self, id, data):
        file = Image.open(io.BytesIO(drive.download_image(id)))
        fig_, ax = plt.subplots()
        ax.imshow(file, cmap="gray")

        for word in data:
            label = word["text"]
            left = word["left"]
            top = word["top"]
            width = word["width"]
            height = word["height"]

            rectangle = patches.Rectangle((left, top), width, height, linewidth=1, edgecolor="r", facecolor="none")
            ax.add_patch(rectangle)
            #TODO: Need to figure out a way to display the labels with the identified text
        plt.show()
    
    def recognitionPipeline(self, id):
        data = self.extract_ocr_data(id)
        return self.identify_names(data)
