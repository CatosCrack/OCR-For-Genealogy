import os.path
import re
import io
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaIoBaseDownload

# For documentation about the Google Drive API, visit https://developers.google.com/drive/api/guides/about-sdk

class Drive:
    def __init__(self) -> None:
        pass

    def login(self):
        creds = None

        # The scopes as defined in the Google Cloud console
        SCOPES = ["openid", "https://www.googleapis.com/auth/userinfo.email", "https://www.googleapis.com/auth/docs", "https://www.googleapis.com/auth/drive"]

        # The tokens.json file is created automatically when the authorization is completed for the first time
        if os.path.exists("secrets/tokens.json"):
            creds = Credentials.from_authorized_user_file("secrets/tokens.json", SCOPES)

        # If tokens.json does not exist, then allow the user to login and save the tokens after user logs in
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file("secrets/credentials.json", SCOPES)
                creds = flow.run_local_server(port=0)

            with open("secrets/tokens.json", "w") as token:
                token.write(creds.to_json())

        return creds

    # This method returns a dictionary with key-value pair of file name and file id
    def get_drive_files(self):
        
        # Check if the autorization file exists, otherwise starts OAuth process
        if os.path.exists("secrets/tokens.json"):
            creds = Credentials.from_authorized_user_file("secrets/tokens.json")
        else:
            creds = self.login()

        try:
            service = build("drive", "v3", credentials=creds)

            # Create an API call
            results = (service.files()
                       .list(pageSize=10, fields="nextPageToken, files(id, name, mimeType)")
                       .execute()
                       )
            
            #print("Results:")
            #print(results)
            
            # Send API call (equivalent to GET method)
            items = results.get("files", [])
            image_ids = {}
            #print("Items:")
            #print(items)
                  
        except HttpError as error:
            print(f"An error occurred. {error}")

        # Return a dictionary with the image name and the image id
        if not items:
            print("No files found.")
        else:
            pattern = re.compile("image/.*")
            for item in items:
                if re.search(pattern, item["mimeType"]) != None:
                    image_ids[item["name"]] = item['id']

        return image_ids
    
    # This method downloads a byte sequence for the image from Google Drive using the specified ID
    def download_image(self, id):

        # Check if the autorization file exists, otherwise starts OAuth process
        if os.path.exists("secrets/tokens.json"):
            creds = Credentials.from_authorized_user_file("secrets/tokens.json")
        else:
            creds = self.login()

        try:
            service = build("drive", "v3", credentials=creds)

            # Create an API call
            request = service.files().get_media(fileId=id)

            # Creates an empty byte file
            file = io.BytesIO()

            # Download the image in byte format to the empty file
            downloader = MediaIoBaseDownload(file, request)
            done = False
            while done is False:
                status, done = downloader.next_chunk()
                print(f"Download {int(status.progress() * 100)}.")

            #Returns the bytes of the image
            return file.getvalue()
            
        except HttpError as error:
            print(f"An error occurred. {error}")