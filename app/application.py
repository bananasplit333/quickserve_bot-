from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)

# Create a dictionary to store the user's session information
user_sessions = {}
stlth_choice = [
    "Acai Berry",
    "Iced Grape",
    "Banana",
    "Fruit Punch",
    "Banana Ice",
    "Skittle Ice",
    "Berry Mix",
    "Pink Lemon",
    "Bear Foot",
    "Peach Pomegranate",
    "Blue Lemon",
    "Peach Watermelon",
    "Blueberry",
    "Sour Mouth",
    "Blue Raspberry",
    "Strawana",
    "Chew",
    "Watermelon Ice",
    "Berry Gummy",
    "Pineapple Lemon",
    "Gummy Bear Ice",
    "Guava Lychee",
    "Honeydew Melon Ice",
    "Iced Apple",
    "Mango Pineapple"
]

fg_choice = [
    "Pineapple Banana Orange Ice",
    "Lemon Mint",
    "Watermelon Ice",
    "Blackberry Lemon",
    "Banana Freeze",
    "Banana Mint",
    "Grape Ice",  
    "Strawberry Watermelon"
]

ivida_5k = [
    "SKTL Ice",
    "Watermelon Ice",
    "Fruit Punch",
    "Sour Apple",
    "Watermelon Strawberry Kiwi",
    "Cherry Berry",
    "Aloe Grape Ice",
    "Grape Ice",
    "GB Ice",
    "Blue Razz Ice",
    "Cool Mint",
    "Blue Razz Lemonade",
    "Peach Ice"
]

ivida_7k = [
    "Fruit Punch",
    "Peach Ice",
    "Blue Razz Ice",
    "Pineapple Mango"
]

RM_choice = [
    "Pineapple Ice",
    "Lush Ice",
    "Mixed Berry",
    "Mango Ice",
    "Aloe Grape"
]

#

@app.route("/sms", methods=['GET', 'POST'])
def sms_reply():
    # Start our TwiML response
    resp = MessagingResponse()
    user_number = request.values['From']
    user_response = request.values['Body'].strip() #user response
    
    
    if user_number not in user_sessions:
        print(user_response)
        if user_response == "1":
            flavors = "\n".join(stlth_choice)
            resp.message("Please choose between our flavors: \n" + flavors)
            return str(resp)
        elif user_response == "2": 
            flavors = "\n".join(fg_choice)
            resp.message("Please choose between our flavors: \n" + flavors)
            return str(resp)
        elif user_response == "3": 
            flavors = "\n".join(ivida_5k)
            resp.message("Please choose between our flavors: \n" + flavors)
            return str(resp)
        elif user_response == "4": 
            flavors = "\n".join(ivida_7k)
            resp.message("Please choose between our flavors: \n" + flavors)
            return str(resp)
        elif user_response == "5": 
            flavors = "\n".join(RM_choice)
            resp.message("Please choose between our flavors: \n" + flavors)
            return str(resp)
        else:
            resp.message("""Welcome to our automated ordering system. Please reply with one of the following options: 
    1 - ZPODS (24.99)
    2 - FG PODS (22.99)
    3 - IVIDA 5k (29.99)
    4 - IVIDA 7K (32.99)
    5 - RM Puff Bars 3.6k (23.99)
                        """)
            return str(resp)

if __name__ == "__main__":
    app.run(debug=True)
