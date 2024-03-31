from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.errors import HttpError
from googleapiclient.discovery import build

import pickle
import sys
import os

CLIENT_SECRETS_FILE = "../user_data/client_secrets.json"
SCOPES = ['https://www.googleapis.com/auth/youtube']
API_SERVICE_NAME = 'youtube'
API_VERSION = 'v3'
CREDENTIALS_DIR = "../user_data"
CREDENTIALS_FILE = os.path.join(CREDENTIALS_DIR, "credentials.pickle")

def get_authenticated_service():
    credentials = None
    # Check if the credentials file exists
    if os.path.exists(CREDENTIALS_FILE):
        with open(CREDENTIALS_FILE, 'rb') as token:
            credentials = pickle.load(token)

    # If there are no valid credentials available, let the user log in.
    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            credentials.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)
            credentials = flow.run_local_server(port=8082)
        # Create the directory if it does not exist
        os.makedirs(CREDENTIALS_DIR, exist_ok=True)
        # Save the credentials for the next run
        with open(CREDENTIALS_FILE, 'wb') as token:
            pickle.dump(credentials, token)

    return build(API_SERVICE_NAME, API_VERSION, credentials=credentials)

def update_broadcast_title_from_file(youtube):
    try:
        with open('../user_data/broadcast_id.txt', 'r') as file:
            broadcast_id = file.read().strip()
            #youtubelink = "https://www.youtube.com/watch?v=" + broadcast_id
    except FileNotFoundError:
        print("The file or directory does not exist. Please check the path and try again.")
        print("Try running the get_upcoming_stream_broadcast_id function to automatically create this id.")
        print("Aborting proccess - youtube_api.py Module - update_broadcast_title_from_file() Function.")
        return

    try:
        with open('../user_data/stream_title.txt', 'r') as file:
            new_title = file.read().strip()
    except FileNotFoundError:
        print("The file or directory does not exist. Please check the path and try again.")
        print("../user_data/stream_title.txt is missing, this file must be created for this function.")
        print("Aborting proccess - youtube_api.py Module - update_broadcast_title_from_file() Function.")
        return

    youtube.liveBroadcasts().update(
        part='snippet',
        body={
            'id': broadcast_id,
            'snippet': {
                'title': new_title
            }
        }
    ).execute()
    print(f"Updated title to: {new_title}")

def update_broadcast_title_from_input(youtube):
    try:
        with open('../user_data/broadcast_id.txt', 'r') as file:
            broadcast_id = file.read().strip()
            #youtubelink = "https://www.youtube.com/watch?v=" + broadcast_id
    except FileNotFoundError:
        print("The file or directory does not exist. Please check the path and try again.")
        print("Try running the get_upcoming_stream_broadcast_id function to automatically create this id.")
        print("Aborting proccess - youtube_api.py Module - update_broadcast_title_from_input() Function.")
        return

    new_title = input("Enter new title: ")

    youtube.liveBroadcasts().update(
        part='snippet',
        body={
            'id': broadcast_id,
            'snippet': {
                'title': new_title
            }
        }
    ).execute()
    print(f"Updated title to: {new_title}")

def end_broadcast(youtube):
    try:
        with open('../user_data/broadcast_id.txt', 'r') as file:
            broadcast_id = file.read().strip()
            #youtubelink = "https://www.youtube.com/watch?v=" + broadcast_id
    except FileNotFoundError:
        print("The file or directory does not exist. Please check the path and try again.")
        print("Try running the get_upcoming_stream_broadcast_id function to automatically create this id.")
        print("Aborting proccess - youtube_api.py Module - end_broadcast() Function.")
        return

    try:
        youtube.liveBroadcasts().transition(
            broadcastStatus='complete',
            id=broadcast_id,
            part='id,snippet'
        ).execute()
        print(f"Ended broadcast with ID: {broadcast_id}")
    except HttpError as e:
        if e.resp.status == 403 and 'redundantTransition' in str(e):
            print(f"Broadcast with ID: {broadcast_id} is already ended or not active.")
        else:
            raise


def list_upcoming_broadcasts(youtube):
    response = youtube.liveBroadcasts().list(
        part='id,snippet',
        broadcastStatus='upcoming',
        maxResults=50
    ).execute()

    for broadcast in response.get('items', []):
        print(f"Upcoming broadcast: {broadcast['snippet']['title']} (ID: {broadcast['id']})")


if __name__ == '__main__':
    youtube = get_authenticated_service()

    if len(sys.argv) > 1:
        command = sys.argv[1]
        if command == 'update_file':
            update_broadcast_title_from_file(youtube)
        elif command == 'update_input':
            update_broadcast_title_from_input(youtube)
        elif command == 'end':
            end_broadcast(youtube)
        elif command == 'list_upcoming':
            list_upcoming_broadcasts(youtube)
        elif command == 'authenticate':
            get_authenticated_service()
        else:
            print("Unknown command.")
    else:
        print("No command provided.")
