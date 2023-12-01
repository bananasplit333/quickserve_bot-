import random
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import sqlite3
import database
import string 
import datetime


app = Flask(__name__)

# Create a dictionary to store the user's session information
user_sessions = {}
order_data = []
ordering = False
z_pod = {
    "acai_berry": 30,
    "iced grape": 42,
    "banana": 22,
    "fruit punch": 0,
    "banana ice": 22,
    "skittle ice": 0,
    "chew": 40,
    "blue raspberry": 33,
}

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

ivida_5k = {
    "SKTL Ice": 20,
    "Watermelon Ice": 12,
    "Fruit Punch": 4,
    "Sour Apple" : 33,
    "Watermelon Strawberry Kiwi": 8 ,
    "Cherry Berry": 19,
    "Aloe Grape Ice": 10,
    "Grape Ice": 0,
    "GB Ice": 0,
    "Blue Razz Ice": 29,
    "Cool Mint": 34,
    "Blue Razz Lemonade": 14,
    "Peach Ice": 13
}

ivida_7k = {
    "Fruit Punch": 10,
    "Peach Ice": 12,
    "Blue Razz Ice": 13,
    "Pineapple Mango": 14
}

RM_choice = [
    "Pineapple Ice",
    "Lush Ice",
    "Mixed Berry",
    "Mango Ice",
    "Aloe Grape"
]

ordering = False
@app.route("/sms", methods=['GET', 'POST'])
def sms_reply():
    # Start our TwiML response
    resp = MessagingResponse()
    user_number = request.values['From']
    user_response = request.values['Body'].strip() #user response
    customer_id = database.get_customer_id(user_number)
    
    
    if user_number not in user_sessions:
        print(user_response)
        if user_response == "1":
            user_sessions[user_number] = {}
            user_sessions[user_number]['brand'] = "ZPODS"
            resp.message(list_items(z_pod))
            return str(resp)
        elif user_response == "2":
            user_sessions[user_number]['brand'] = "FGPODS"
            resp.message(list_items(fg_choice))
            return str(resp)
        elif user_response == "3":
            user_sessions[user_number]['brand'] = "IVIDA5K"
            resp.message(list_items(ivida_5k))
            return str(resp)
        elif user_response == "4": 
            user_sessions[user_number]['brand'] = "IVIDA7K"
            resp.message(list_items(ivida_7k))
            return str(resp)
        elif user_response == "5":
            user_sessions[user_number]['brand'] = "RM"
            resp.message(list_items(RM_choice))
            return str(resp)
        else:
            return intro_msg()
        
    elif user_sessions[user_number]:
        user_response = request.values['Body'].strip().lower()
        print("user response in active session " + str(user_sessions[user_number]))
        if user_sessions[user_number]['brand'] == "ZPODS":
            print("ZPODS")
            #customer orders zpods, with count
            if user_response in z_pod:
                print(user_response)
                resp.message("Please enter the number of " + user_response + " you would like to order")
                order_data.append(user_response)
                return str(resp)
            elif len(order_data) > 0:
                print("selecting qty")
                res = order_data[-1]
                if user_response.isnumeric():
                    user_sessions[user_number] = []
                    order_data.append(user_response)
                    print(user_sessions)
                    current_date = datetime.date.today()
                    database.insert_order(customer_id, 1, current_date, int(user_response))
                    dict_order = {
                        'brand':'ZPODS',
                        'flavor':res,
                        'qty': user_response
                    }
                    user_sessions[user_number].append(dict_order)
                    print(user_sessions)
                    amnt = float(user_response) * 23.99
                    resp.message("ordered " + user_response + " of " + res + " for a total of " + str(amnt))
                return str(resp)
            else: 
                print("order data new length " + str(len(order_data)))
                print("else message")
                resp.message("hi")
                return str(resp)
            """    
            elif user_response == "back":
                del user_sessions[user_number]
                print("user deleted")
                return intro_msg()
            else:
                resp.message("else message")
                return str(resp)
        elif user_sessions[user_number]['brand']: 
            print(user_sessions[user_number]['brand'])
            if (user_response) > 0:
                print("user response is greater than 0")
                print(user_response)
                user_sessions[user_number]['quantity'] = user_response
                resp.message("you have ordered " + user_response + " of "
    elif user_sessions[user_number] and ordering: 
        user_response = request.values['Body'].strip().lower()
        print("user response choosing qty")
        if user_response > 0: 
            print("user response is greater than 0")
            print(user_response)
            user_sessions[user_number]['quantity'] = user_response
            resp.message("you have ordered " + user_response + " of " + user_sessions[user_number]['brand'] + " for a total of " + str(user_sessions[user_number]['quantity']))
            return str(resp)
        else:
            resp.message("error, please input a number")
            return str(resp)
    else:
        return intro_msg()
"""

def list_items(type):
    keys = [key for key, value in type.items() if value > 0]
    flavors = "\n".join(keys)
    message = "Please choose between our flavors: \n" + flavors +  " with the amount. (ex. chew, 3)"  "\n" + "text 'back' to go back"
    return message

def intro_msg():
    resp = MessagingResponse()
    resp.message("""Welcome to our automated ordering system. Please reply with one of the following options: 
    1 - ZPODS (24.99)
    2 - FG PODS (22.99)
    3 - IVIDA 5k (29.99)
    4 - IVIDA 7K (32.99)
    5 - RM Puff Bars 3.6k (23.99)
                        """)
    return str(resp)

def handle_order(user_number, flavor, quantity, type):
    #this function should do an order summary : 
    user_sessions[user_number]['order_history'] = flavor
    type[flavor] -= quantity
    print("decremented item... new count for flavor..." + flavor + "... " + str(z_pod[flavor]))
    print(flavor + "added to cart")
    
def generate_confirmation_code():
    characters = string.ascii_letters + string.digits
    code_length = 6
    confirmation_code = ''.join(random.choice(characters) for _ in range(code_length))  
    return confirmation_code

if __name__ == "__main__":
    app.run(debug=True)

