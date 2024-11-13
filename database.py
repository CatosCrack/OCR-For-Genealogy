import firebase_admin
from firebase_admin import credentials, firestore

class Database:

    def __init__(self) -> None:
        # Create an instance of the app
        cred = credentials.Certificate("secrets/firebase_credentials.json")
        self.__app = firebase_admin.initialize_app(cred)

        # Check if app was initialized  
        if (self.__app):
            print("App initialized")

        # Access the firestore service
        self.__store = firestore.client()

    ## Prints all collection data
    def get_collection_data(self):
        # Get a list with all documents in the collection
        # Returns a generator with DocumentReference objects
        collection = self.__store.collection("Documents").list_documents()

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

            # Get the subcollection in the documents
            subcollection = doc_ref.collection("Person").list_documents()
            for sub in subcollection:
                person = sub.get()
                person_id = person.id
                print(f"Person ID: {person_id}")
                person_fields = person.to_dict()
                print(f"Person Fields: {person_fields}")

    def upload_document(self, collectionData, subcollectionData):
        # This adds a new document to the Documents collection
        # [1] retrieves the DocumentReference of the added document
        collection = self.__store.collection("Documents").add(collectionData)[1]
        for person in subcollectionData:
            subcollection = collection.collection("Person").add(person)