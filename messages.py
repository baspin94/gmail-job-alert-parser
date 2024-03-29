import os.path
import base64
from bs4 import BeautifulSoup
import ipdb

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]

def main():
  """Complete authorization flow if needed.
  Retrieve messages from mailbox labeled 'Indeed'.
  """
  creds = None
  # The file token.json stores the user's access and refresh tokens, and is
  # created automatically when the authorization flow completes for the first
  # time.
  if os.path.exists("token.json"):
    creds = Credentials.from_authorized_user_file("token.json", SCOPES)
  # If there are no (valid) credentials available, let the user log in.
  if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
      creds.refresh(Request())
    else:
      flow = InstalledAppFlow.from_client_secrets_file(
          "credentials.json", SCOPES
      )
      creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open("token.json", "w") as token:
      token.write(creds.to_json())

  try:
    # Call the Gmail API
    service = build("gmail", "v1", credentials=creds)
    list_results = service.users().messages().list(userId="me", labelIds='Label_6775883955527461764').execute()
    messages = list_results.get("messages", [])

    if not messages:
      print("No messages found.")
      return
    print("Message IDs:")
    ids = []
    for message in messages:
      ids.append(message['id'])
    print(ids)

    msg_results = service.users().messages().get(userId="me", id=ids[0], format="full").execute()
    msg = msg_results["payload"]["parts"][1]["body"]["data"]
    decoded_msg = base64.urlsafe_b64decode(msg)
    
    doc = BeautifulSoup(decoded_msg, 'html.parser')
    ipdb.set_trace()

  except HttpError as error:
    # TODO(developer) - Handle errors from gmail API.
    print(f"An error occurred: {error}")

if __name__ == "__main__":
  main()


