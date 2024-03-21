import json
from twilio.rest import Client

# Load the Twilio configuration from the JSON file
with open('twilio_config.json', 'r') as file:
    config = json.load(file)

account_sid = config['your_account_sid']
auth_token = config['auth_token']
twilio_sender_number = config['twilio_sender_number']

# Initialize the Twilio client
client = Client(account_sid, auth_token)

# Load the WhatsApp numbers from the JSON file
with open('whatsapp_numbers.json', 'r') as file:
    whatsapp_numbers = json.load(file)

# Send a WhatsApp message to each number
for name, number in whatsapp_numbers.items():
    message = client.messages.create(
        from_='whatsapp:+{}'.format(twilio_sender_number),
        body='Hello {}, this is a test message!'.format(name),
        to='whatsapp:+{}'.format(number)
    )
    print('Message sent to {}: {}'.format(name, message.sid))
