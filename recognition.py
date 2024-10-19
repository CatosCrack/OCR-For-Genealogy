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

    # extract_ocr_data takes the image ID and downloads the byte information. It then processes the image by calling
    # image_correction and executes tesseract OCR on the edited image and return a list of dictionaries with
    # the text and information about the bounding box of that text 
    def extract_ocr_data(self, id):
        
        # Downloads the byte data and opens the image using PIL
        file = Image.open(io.BytesIO(drive.download_image(id)))
        
        # Saves PIL image to the specified path and executes the image correction pipeline 
        path = r"temp/image.tif"
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

        # After the inference, it returns a list of dictionaries with the recognized text and the bounding box information  
        ls = []
        for i in range(0, len(inference["left"])):
            # TODO: Check if conf is the correct parameter to filter by. Some sources say conf is actually a confidence level
            # ["conf"][i] != -1 checks if the identified box is a character or a full word
            if inference["conf"][i] != -1:
                dc = {}
                dc["text"] = inference["text"][i]
                dc["left"] = inference["left"][i]
                dc["top"] = inference["top"][i]
                dc["width"] = inference["width"][i]
                dc["height"] = inference["height"][i]
                ls.append(dc)

        return ls
    
    # identify_names() uses the list from extract_ocr_data and filters the list to only keep names of people
    # It returns a list of dictionaries that contains names or last names of people
    def identify_names(self, data):

        name_data = []

        # Load the SpaCy Spanish Large model
        nlp = spacy.load("es_core_news_lg")

        # Iterates through each word in the input list and checks if the named entity corresponds to a person
        for word in data:
            doc = nlp(word["text"])
            for ent in doc.ents:
                if ent.label_ == "PER":
                    name_data.append(word)
        
        # Returns a list of dictionaries containing only people and the bounding box information
        return name_data
    
    # plot_boxes() is a helper function that downloads the original image and plots the bounding boxes of the recognized names
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
    
    # recognitionPipeline is the core function of the Recognition Class and activates the recognition pipeline for a given image
    def recognitionPipeline(self, id):
        data = self.extract_ocr_data(id)
        return self.identify_names(data)
