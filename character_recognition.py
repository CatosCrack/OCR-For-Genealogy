from PIL import Image
import io
import pytesseract
from external_resources import Drive

class Recognition:
    def __init__(self) -> None:
        pass
        
    def extract_ocr_data(self):
        drive = Drive()
        images = drive.get_drive_files()

        # For reference to use PyTesseract, visit https://pypi.org/project/pytesseract/
        data = {}

        for image in images:
            print("................................................")
            print(image)
            id = images[image]
            file = Image.open(io.BytesIO(drive.download_image(id)))
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
                    ls.append([dc])
    
            data[id] = ls

        return data
    
    def identify_names(self):
        pass

rec = Recognition()
print(rec.extract_ocr_data())