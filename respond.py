# Download the helper library from https://www.twilio.com/docs/python/install

from twilio.rest import Client
from dotenv import load_dotenv
import os 
load_dotenv()
# Find your Account SID and Auth Token at twilio.com/console
# and set the environment variables. See http://twil.io/secure
account_sid = os.environ['TWILIO_ACCOUNT_SID']
auth_token = os.environ['TWILIO_AUTH_TOKEN']
client = Client(account_sid, auth_token)

message = client.messages.create(
                              from_='+18194142309',
                              body='ㅎㅇ~',
                              to=os.environ['MY_NUMBER']'
                          )

print(f" SID: {message.sid} STATUS: {message.status}")
