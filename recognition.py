from google.cloud import documentai_v1 as documentai
from google.oauth2 import service_account
from database import Database
import spacy
from spacy.matcher import Matcher
import utils
import csv
import unicodedata
import re

db = Database()

# Base processor data
project_id = "genealogy-ocr-index"
location = "us"
processor_id = "4cb2ae40b145c48"

class ocr_engine:
    def __init__(self) -> None:

        # Create a client
        cred = service_account.Credentials.from_service_account_file("secrets/docai_credentials.json")
        self.__client = documentai.DocumentProcessorServiceClient(
            credentials=cred,
            client_options={"api_endpoint": f"{location}-documentai.googleapis.com"}
        )

        # Get the processor
        self.__processor = self.__client.processor_path(project=project_id, location=location, processor=processor_id)

    # Method to create a indexed map of Document AI tokens
    def get_map(self, doc):
        map = {}
        for page in doc.pages:
            for token in page.tokens:
                idx = token.layout.text_anchor.text_segments[0].start_index
                end = token.layout.text_anchor.text_segments[0].end_index
                # The vertices go clockwise, starting on the upper left corner
                vertices = [vertix for vertix in token.layout.bounding_poly.normalized_vertices]
                map[idx] = (idx, end, vertices)
        return map
    
    # Iterate over blocks to gather starting and ending indexes
    def get_indexes(doc):
        block_idx = []
    
        for page in doc.pages:
            for block in page.blocks:
                start = block.layout.text_anchor.text_segments[0].start_index
                end = block.layout.text_anchor.text_segments[0].end_index
                block_idx.append((start, end))

        return block_idx
    
    # Find names in text and get bounding boxes
    ## TODO: Finish this method
    def get_bounding_box(name, original_text, map):
        # Ensure the name is a string
        name = str(name)
    
        # Get initial and last index of text
        pattern = r"\b" + "".join(char + r"[\n-]*" if char != " " else r"[\s]*" for char in name ) + r"\b"
        match = re.search(pattern, original_text, re.IGNORECASE)
        if match:
            idx = match.span()[0]
            end = match.span()[1]+1 # Add one because Document AI considers whitespaces
            print("Indexes: ", idx, end, "String: ", repr(original_text[idx:end]))
        else:
            print("No matches")

    def process_documents(self):
        
        # Get image data from Could Storage
        bucket_data = db.storage_get_images()

        # Get image URIs
        uris = [group[0] for group in bucket_data]

        # Get image download URLs
        urls = [group[1] for group in bucket_data]

        # Iterate through each image fetched
        for uri, url in uris,urls:

            # Get extension of images to set correct mime type
            extension = uris[2][-3:]
            if "jpg" in extension:
                extension = "jpeg"
            elif "png" in extension:
                extension = "png"

            # Create a raw document object
            document = documentai.GcsDocument(gcs_uri=uri, mime_type=f"image/{extension}")

            # Create API request
            request = documentai.ProcessRequest(name=self.__processor, 
                                                gcs_document=document,
                                                process_options={"ocr_config": {
                                                    "hints": {"language_hints": "es"}
                                                    }
                                                })

            # Get result
            result = self.__client.process_document(request=request)
            document = result.document

            # Get text from document
            text = document.text

            # Get the year when the document was created
            doc_year = utils.extract_year(text)

            # Get map of tokens
            token_map = self.get_map(document)

            # Get indices of recognized blocks
            block_idx = self.get_indexes(document)

            # Get formatted text blocks
            text_blocks = []
            for idx in block_idx:
                text_block = utils.get_text(idx, text)
                print(f"Block: {text_block}")
                text_blocks.append(utils.formatting(text_block))

            # Recognize names
            name_recognition.recognize_names(text_block, text)


class name_recognition:
    def __init__(self):
        # Load pre-trained and custom NER models for extraction
        self.__nlp_es = spacy.load("es_core_news_lg")
        self.__nlp_custom = spacy.load("ner_model/model/model-best")

        # Create a matcher to improve accuracy 
        self.__matcher = Matcher(self.__nlp_es.vocab)

        # Load list of names
        names = []
        last_names = []

        with open('ner_model/data/processed/first_names_processed.csv', 'r', newline="") as file:
            reader = csv.reader(file, delimiter=",")
            for row in reader:
                names.append(row[0])

        with open('ner_model/data/processed/last_names_processed.csv', 'r', newline='') as file:
            reader = csv.reader(file, delimiter=",")
            for row in reader:
                last_names.append(row[0])

        # Add names and last names to entity ruler
        ruler = self.__nlp_custom.add_pipe("entity_ruler", after="ner", config={"overwrite_ents":True})

        # Create patterns
        patterns = []
        match_patterns = []
        for name in names:
            patterns.append({
                "label":"FIRST_NAME",
                "pattern": [{"LOWER":name.lower()}]
            })
            match_patterns.append([{"LOWER":name.lower()}])
    
        # Add patterns to matcher
        self.__matcher.add("FIRST_NAME", match_patterns)

        match_patterns = []
        for name in last_names:
            patterns.append({
                "label":"LAST_NAME",
                "pattern": [{"LOWER":name.lower()}]
            })
            match_patterns.append([{"LOWER":name.lower()}])

        # Add patterns to pipeline and matcher
        self.__matcher.add("LAST_NAME", match_patterns)
        ruler.add_patterns(patterns)
    
    def recognize_names(self, text_blocks, original_text):
        ## TODO: Need to find a way to be a bit more flexible with the choice 
        ## TODO: Create a function to push names and bounding box data to database
        for block in text_blocks:
            # Extract names
            print("---------- New Block ----------")
            doc = self.__nlp_es(block)
            for ent in doc.ents:
                if ent.label_ == "PER":
                    print("## Default model results: ", ent, ent.label_)
            
                    # Get bounding boxes for the entire entity
                    bounds = ocr_engine.get_bounding_box(ent.text, original_text, map)

                    # Split entity to clasiffy in first name and last name
                    tokens = ent.text.split(" ")
            

                    # Gather first names and last names
                    first_names = []
                    last_names = []

                    # Identify names in the entity
                    for token in tokens:
                        name = self.__nlp_custom(utils.remove_accent(token))
                        matches = self.__matcher(name)
                        for name_ent in name.ents:
                            if len(matches) > 0 and name_ent.label_ == self.__nlp_es.vocab[matches[0][0]].text:
                                # Add to corresponding name list
                                if name_ent.label_ == "FIRST_NAME":
                                    first_names.append(name_ent.text)
                                elif name_ent.label_ == "LAST_NAME":
                                    last_names.append(name_ent.text)
                        
                                # Print recognition data
                                print("     -- MATCHES MATCHER. Custom model results: ", 
                                    name_ent, 
                                    name_ent.label_, 
                                    "/ Matcher results: ", 
                                    name[matches[0][1]:matches[0][2]],
                                    self.__nlp_es.vocab[matches[0][0]].text)
                        
                            elif len(matches) == 0:
                                continue

                            else:
                                print("     -- DISCREPANCY WITH MATCHER. Custom model results: ", 
                                    name_ent, name_ent.label_, 
                                    name[matches[0][1]:matches[0][2]], 
                                    self.__nlp_es.vocab[matches[0][0]].text)
            
                    # Process names separated by a space
                    for i in range(len(tokens)):
                        if i+1 < len(tokens):
                            combined = self.__nlp_custom(tokens[i]+tokens[i+1])
                            match = self.__matcher(combined)
                            if match and combined.ents[0].label_ == self.__nlp_es.vocab[match[0][0]].text:
                                # Add to corresponding name list
                                if combined.ents[0].label_ == "FIRST_NAME":
                                    first_names.append(combined.ents[0].text)
                                elif combined.ents[0].label_ == "LAST_NAME":
                                    last_names.append(combined.ents[0].text)
            
                    # Add first and last names to name list
                    if first_names:
                        print("     -- First Names: ", " ".join(first_names))
                    if last_names:
                        print("     -- Last Names: ", " ".join(last_names))