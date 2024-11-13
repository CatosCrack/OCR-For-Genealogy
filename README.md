## Database
The database uses a Firestore Databases No-SQL technology to save the information indexed in the documents. Since No-SQL uses collections, the database has the foloowing structure:
  - Documents (Main Collection)
    - Document ID (Auto-generated)
    - Municipality (String)
    - Department (String)
    - URL (String)
    - Person (Sub-collection)
      - Document ID (Auto-generated)
      - First Name (String)
      - Last Name (String)
      - Bounds (Array)
        - Index 0: Left (Number)
        - Index 1: Top (Number)
        - Index 2: Width (Number)
        - Index 3: Height (Number)

In the Person sub-collection, the bounds array specifies the coordinates and dimensions of a bounding box containing the text that was recognized. Left and Top give the coordinates
in the image for the top-left corner of the bounding box. Width and height give the dimensions of the box to be able to display it.

### Methods
#### .upload_document(dict collectionData, list subcollectionData)
This method takes two lists to create a new document in the Documents collection and the Person subcollection. 

collectionData will contain 3 values:
  - Municipality (string): Municipality where the document originated
  - Department (string): Department (Colombian equivalent of state/province) where the document originiated
  - URL: URL of document hosted in Google Drive

subcollectionData will contain dictionaries with the data of each person identified in a document. Each dictionary will be formated using the following key-value pairs:
  - First Name (string): First name of the identified individual
  - Last Name (string): Last name of the identified person
  - Bounds (array):
    - Left (integer): X-coordinate of the top-left corner of the bounding box
    - Top (integer): Y-coordinate of the top-left corner of the bounding box
    - Width (integer): Width of the bounding box
    - Height (integer): Height of the bounding box
