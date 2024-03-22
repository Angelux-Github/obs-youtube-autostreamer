from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from datetime import datetime, timezone

CLIENT_SECRETS_FILE = "client_secrets.json"
SCOPES = ['https://www.googleapis.com/auth/youtube']
API_SERVICE_NAME = 'youtube'
API_VERSION = 'v3'

def get_authenticated_service():
    flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)
    credentials = flow.run_local_server(port=8082)
    return build(API_SERVICE_NAME, API_VERSION, credentials=credentials)

def create_live_broadcast(youtube, title, scheduled_start_time):
    insert_broadcast_response = youtube.liveBroadcasts().insert(
        part="snippet,status",
        body=dict(
            snippet=dict(
                title=title,
                scheduledStartTime=scheduled_start_time
            ),
            status=dict(
                privacyStatus="unlisted"
            )
        )
    ).execute()

    return insert_broadcast_response["id"]

def create_dummy_broadcast(youtube):
    broadcast_body = {
        'snippet': {
            'title': 'default',
            'scheduledStartTime': '2024-12-31T23:59:00Z'
        },
        'status': {
            'privacyStatus': 'unlisted'
        },
        'contentDetails': {
            'monitorStream': {
                'enableMonitorStream': False
            }
        }
    }

    response = youtube.liveBroadcasts().insert(
        part='snippet,status,contentDetails',
        body=broadcast_body
    ).execute()

    

    broadcast_id = response['id']
    print(f"Created dummy broadcast with ID: {broadcast_id}")

    with open('broadcast_id.txt', 'w') as file:
        file.write(broadcast_id)

    return broadcast_id



def update_broadcast_title(youtube, broadcast_id):
    if broadcast_id is None:
        print("No broadcast ID provided. Cannot update title.")
        return

    with open('stream_title.txt', 'r') as file:
        new_title = file.read().strip()

    broadcasts = youtube.liveBroadcasts().list(
        part='snippet',
        id=broadcast_id
    ).execute()

    if broadcasts['items']:
        broadcast = broadcasts['items'][0]
        broadcast['snippet']['title'] = new_title
        youtube.liveBroadcasts().update(
            part='snippet',
            body=broadcast
        ).execute()
        print(f"Updated title to: {new_title}")
    else:
        print("Broadcast not found.")

def end_broadcast(youtube, broadcast_id):
    if broadcast_id is None:
        print("No broadcast ID provided. Cannot end stream.")
        return

    try:
        youtube.liveBroadcasts().transition(
            broadcastStatus='complete',
            id=broadcast_id,
            part='id,snippet'
        ).execute()
        print(f"Ended broadcast with ID: {broadcast_id}")
    except Exception as e:
        print(f"An error occurred: {e}")

def get_most_recent_active_broadcast_id(youtube):
    response = youtube.liveBroadcasts().list(
        part='snippet',
        broadcastStatus='active',
        broadcastType='all',
        maxResults=1,
        fields='items(id,snippet(title))'
    ).execute()

    if response['items']:
        most_recent_broadcast = response['items'][0]
        broadcast_id = most_recent_broadcast['id']
        broadcast_title = most_recent_broadcast['snippet']['title']
        print(f"Most recent active broadcast: {broadcast_title} (ID: {broadcast_id})")

        with open('broadcast_id.txt', 'w') as file:
            file.write(broadcast_id)

        return broadcast_id
    else:
        print("None")

        with open('broadcast_id.txt', 'w') as file:
            file.write("No active broadcasts found.")

        return None

def get_broadcast_id_by_title(youtube, broadcast_title):
    response = youtube.liveBroadcasts().list(
        part='snippet',
        broadcastStatus='all',
        maxResults=50
    ).execute()

    for broadcast in response.get('items', []):
        if broadcast['snippet']['title'] == broadcast_title:
            return broadcast['id']

    print(f"No broadcast found with title: {broadcast_title}")
    return None

if __name__ == '__main__':
    youtube = get_authenticated_service()

    import sys
    if len(sys.argv) > 1:
        if sys.argv[1] == 'end':
            broadcast_id = get_most_recent_active_broadcast_id(youtube)
            end_broadcast(youtube, broadcast_id)
        elif sys.argv[1] == 'create':
            broadcast_title = "Test Broadcast"
            now = datetime.now(timezone.utc).isoformat() + "Z"
            create_live_broadcast(youtube, broadcast_title, now)
        elif sys.argv[1] == 'default':
            create_dummy_broadcast(youtube)

        elif sys.argv[1] == 'stream_file_input':
            if len(sys.argv) > 2:
                print("ERROR - Somehow you got here? line 162 when arguments have already been specified via powershell.exe")
            else:    
                print("getting input from stream_title.txt")
                with open('stream_title.txt', 'r') as file:
                    title = file.read().strip()
                print("Title in stream_title.txt is: "+title)
                broadcast_id = get_broadcast_id_by_title(youtube, title)
            if broadcast_id:
                print(f"Broadcast ID for '{title}': {broadcast_id}")
                with open('broadcast_id.txt', 'w') as file:
                    file.write(broadcast_id)
            else:
                print("Please provide a title to search for.")
        
        elif sys.argv[1] == 'getid_input':
            if len(sys.argv) > 2:
                title = sys.argv[2]
            else:
                title = input("Please provide a title to search for: ")
    
                broadcast_id = get_broadcast_id_by_title(youtube, title)
            if broadcast_id:
                print(f"Broadcast ID for '{title}': {broadcast_id}")
                with open('broadcast_id.txt', 'w') as file:
                    file.write(broadcast_id)
            else:
                print(f"No broadcast found for title '{title}'.")

        elif sys.argv[1] == 'update':

            with open('broadcast_id.txt', 'r') as file:
                broadcast_id = file.read().strip()
            update_broadcast_title(youtube, broadcast_id)
        else:
            print("Unknown command.")






