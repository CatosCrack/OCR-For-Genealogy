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

    ## Returs a list of dowload URLs for all files
    def storage_get_images(self):
        
        urls = []

        prefix = f"test_images/"
        bucket = storage.bucket()
        files = list(bucket.list_blobs(prefix=prefix, delimiter="/"))
        for file in files:
            if (file.name != prefix):
                name = urllib.parse.quote(file.name, safe="")
                blob = bucket.get_blob(file.name)
                token = blob.metadata.get("firebaseStorageDownloadTokens")
                url = f"gs://{self.__bucket}/{file.name}"
                #url = f"https://firebasestorage.googleapis.com/v0/b/{self.__bucket}/o/{name}?alt=media&token={token}"
                urls.append(url)

        return urls
    
    ##TODO: Update function to use new database structure
    def upload_document(self, collectionData, subcollectionData):
        # This adds a new document to the Documents collection
        # [1] retrieves the DocumentReference of the added document
        collection = self.__store.collection("Documents").add(collectionData)[1]
        for person in subcollectionData:
            subcollection = collection.collection("Person").add(person)