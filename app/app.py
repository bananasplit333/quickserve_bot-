from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse, Message
from twilio.rest import Client
from dotenv import load_dotenv
import os 
load_dotenv()
app = Flask(__name__)

account_sid = os.getenv('TWILIO_ACCOUNT_SID')
auth_token = os.getenv('TWILIO_AUTH_TOKEN')
client = Client(account_sid, auth_token)

@app.route("/")
def hello():
    message = client.messages.create(
        body='Hello World!',
        from_=os.environ['TWILIO_NUMBER'],
        to=os.environ['MY_NUMBER']
    )
    print(message.sid)
    return "Hello World!"


@app.route("/sms", methods=['POST'])
def sms_reply():
    """Respond to incoming SMS with a simple text message."""
    # Start our TwiML response
    resp = MessagingResponse()

    # Add a message
    resp.message("The Robots are coming! Head for the hills!")

    return str(resp)

if __name__ == "__main__":
    app.run(debug=True)
