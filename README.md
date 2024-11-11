## Database
The database uses a Firestore Databases No-SQL technology to save the information indexed in the documents. Since No-SQL uses collections, the database has the foloowing structure:
  - Documents (Main Collection)
    - Document ID (Auto-generated)
    - Location (String)
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

