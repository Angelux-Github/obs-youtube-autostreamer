import json
from twilio.rest import Client

# Load the Twilio configuration from the JSON file
with open('twilio_config.json', 'r') as file:
    config = json.load(file)

account_sid = config['your_account_sid']
auth_token = config['auth_token']
twilio_sender_number = config['twilio_sender_number']
recipient_number = config['receipient_number']

# Initialize the Twilio client
client = Client(account_sid, auth_token)

# Send a WhatsApp message
message = client.messages.create(
    from_='whatsapp:+{}'.format(twilio_sender_number),
    body='Hello, this is a test message from WSL!',
    to='whatsapp:+{}'.format(recipient_number)
)

print('Message SID:', message.sid)
