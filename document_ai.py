from google.cloud import documentai_v1 as documentai
from google.oauth2 import service_account
from database import Database

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

    def process_documents(self):

        # Get image from URL
        uris = db.storage_get_images()

        # Get extension of images to set correct mime type
        extension = uris[2][-3:]
        if "jpg" in extension:
            extension = "jpeg"
        elif "png" in extension:
            extension = "png"

        # Create a raw document object
        document = documentai.GcsDocument(gcs_uri=uris[2], mime_type=f"image/{extension}")

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
        print(document)

        # Get text from document
        text = document.text