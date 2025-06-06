import urllib.parse
from firebase_admin import credentials, firestore, initialize_app, storage
import urllib

class Database:

    def __init__(self) -> None:
        # Create an instance of the app
        cred = credentials.Certificate("secrets/firebase_credentials.json")
        self.__bucket = "genealogy-index.firebasestorage.app"
        self.__app = initialize_app(cred, {"storageBucket":self.__bucket})

        # Check if app was initialized  
        if (self.__app):
            print("App initialized")

        # Access the firestore service
        self.__store = firestore.client()

    ## Prints all collection data
    def get_collection_data(self):
        # Get a list with all documents in the collection
        # Returns a generator with DocumentReference objects
        collection = self.__store.collection("Document").list_documents()

        # Iterate the generator and gets DocumentReferences
        for doc_ref in collection:
            # Get a DocumentSnapshot from the DocumentRefeference
            # Documentation for Document Snapshot
            # https://cloud.google.com/python/docs/reference/firestore/latest/google.cloud.firestore_v1.base_document.DocumentSnapshot
            document = doc_ref.get()

            # Get the id of the document and the fields in the document
            doc_id = document.id
            print(f"Document ID: {doc_id}")
            document_fields = document.to_dict()
            print(f"Document Fields: {document_fields}")

    ## Returs a list of URIs and URLs for all files
    def storage_get_images(self):
        
        uris = []

        prefix = f"test_images/"
        bucket = storage.bucket()
        files = list(bucket.list_blobs(prefix=prefix, delimiter="/"))
        for file in files:
            if (file.name != prefix):
                url = file.metadata["firebaseStorageDownloadTokens"]
                file_name = urllib.parse.quote(file.name, safe="")
                url = f"https://firebasestorage.googleapis.com/v0/b/{self.__bucket}/o/{file_name}?alt=media&token={url}"
                uri = f"gs://{self.__bucket}/{file.name}"
                uris.append((uri,url))

        return uris
    
    # Upload an image to Document collection in Firestore
    # Returns automatically-generated document ID
    def create_document(self, year, department, municipality, url):
        data = {
            "year":year,
            "department":department,
            "municipality":municipality,
            "url":url
        }

        update_time, doc_ref = self.__store.collection("Document").add(data)
        id = doc_ref.id

        print("Document added. ID: ", id)

        return id
    
    # Upload a bounding box instance to Bounds collection in Firestore
    def create_bound(self, bounds, doc_id, first_name, last_name):

        data = {
            "bounds":bounds,
            "doc_id":doc_id,
            "first_name":first_name,
            "last_name":last_name
        }

        print("Bounds added. Data added: ")
        print(data)

        update_time, doc_ref = self.__store.collection("Bounds").add(data)

        print("ID: ", doc_ref.id)