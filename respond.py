# Download the helper library from https://www.twilio.com/docs/python/install

from twilio.rest import Client


# Find your Account SID and Auth Token at twilio.com/console
# and set the environment variables. See http://twil.io/secure
account_sid = "ACa845ea0f7f6cde8dcd59940a00a20e05"
auth_token = 'f90957889f373603b14d63187171eb58'
client = Client(account_sid, auth_token)

message = client.messages.create(
                              from_='+1',
                              body='ㅎㅇ~',
                              to='+1'
                          )

print(f" SID: {message.sid} STATUS: {message.status}")
