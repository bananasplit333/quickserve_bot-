import random
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import sqlite3
import database
import string 
import datetime


app = Flask(__name__)

# Create a dictionary to store the user's session information
order_states = {}
user_sessions = {}
order_data = {"ordered": False,
              "zpods": {},
              "fgpods": {},
              "ivida5k": {},
              "ivida7k": {},
              "rm": {}}
ordering = False
z_pod = {
    "acai berry": 30,
    "iced grape": 42,
    "banana": 22,
    "fruit punch": 0,
    "banana ice": 22,
    "skittle ice": 0,
    "chew": 40,
    "blue raspberry": 33,
}

fg_choice = {
    "pineapple banana orange ice": 12,
    "lemon mint": 5,
    "watermelon ice": 19,
    "blackberry lemon": 8,
    "banana freeze": 27,
    "banana mint": 3,
    "grape ice": 14,
    "strawberry watermelon": 21
}

ivida_5k = {
    "sktl ice": 20,
    "watermelon ice": 12,
    "fruit punch": 4,
    "sour apple" : 33,
    "watermelon strawberry kiwi": 8,
    "cherry berry": 19,
    "aloe grape ice": 10,
    "grape ice": 0,
    "gb ice": 0,
    "blue razz ice": 29,
    "cool mint": 34,
    "blue razz lemonade": 14,
    "peach ice": 13
}

ivida_7k = {
    "fruit punch": 10,
    "peach ice": 12,
    "blue razz ice": 13,
    "pineapple mango": 14
}

RM_choice = {
    "pineapple ice": 18,
    "lush ice": 7,
    "mixed berry": 29,
    "mango ice": 3,
    "aloe grape": 14
}


@app.route("/sms", methods=['GET', 'POST'])
def sms_reply():
    # Start our TwiML response
    resp = MessagingResponse()
    user_number = request.values['From']
    user_response = request.values['Body'].strip() #user response
    customer_id = database.get_customer_id(user_number)
    global user_sessions
    global order_data
    global ordering
    
    curr_session = order_states.get(user_number, 'start')

    #if user is in new session, display intro message
    if curr_session == 'start':
        print(user_response)
        user_sessions[user_number] = {}
        if user_response == "1":
            user_sessions[user_number]['brand'] = "ZPODS"
            order_states[user_number] = 'flavor_choice'
            resp.message(list_items(z_pod))
            return str(resp)
        elif user_response == "2":
            user_sessions[user_number]['brand'] = "FGPODS"
            order_states[user_number] = 'flavor_choice'
            resp.message(list_items(fg_choice))
            return str(resp)
        elif user_response == "3":
            user_sessions[user_number]['brand'] = "IVIDA5K"
            order_states[user_number] = 'flavor_choice'
            resp.message(list_items(ivida_5k))
            return str(resp)
        elif user_response == "4": 
            user_sessions[user_number]['brand'] = "IVIDA7K"
            order_states[user_number] = 'flavor_choice'
            resp.message(list_items(ivida_7k))
            return str(resp)
        elif user_response == "5":
            user_sessions[user_number]['brand'] = "RM"
            order_states[user_number] = 'flavor_choice'
            resp.message(list_items(RM_choice))
            return str(resp)
        else:
            return intro_msg(user_number)
    elif user_response == "back":
        return intro_msg(user_number)
        
    #user is in active session, is choosing a flavor
    elif curr_session == 'flavor_choice':
        user_response = request.values['Body'].strip().lower()
        print("user response in active session " + str(user_sessions[user_number]))

        #zpods
        if user_sessions[user_number]['brand'] == "ZPODS":
            print("ZPODS")
            print("ordered_data: " + str(order_data["ordered"]))
            print(user_response in z_pod)
            #user has chosen the right flavor
            if user_response in z_pod:
                print(user_response)
                resp.message("Please enter the number of " + user_response + " you would like to order")
                order_data["zpods"][user_response] = 0 #add to order data list
                print(f"updated order_data : {order_data['zpods']}")
                order_states[user_number] = 'qty_choice' #change state to choose count
                return str(resp)
            elif user_response == "back":
                print("back")
                del user_sessions[user_number]
                return intro_msg(user_number)
            else:
                print("error, please choose a flavor or send 'back' to go back to the previous menu.")
                return str(resp)
            
        #fgpods
        elif user_sessions[user_number]['brand'] == "FGPODS":
            print("fgpods")
            print("ordered_data: " + str(order_data["ordered"]))
            #user has chosen the right flavor
            if user_response in fg_choice:
                print(user_response)
                resp.message("Please enter the number of " + user_response + " you would like to order")
                order_data["fgpods"][user_response] = 0 #add to order data list
                print(f"updated order_data : {order_data['fgpods']}")
                order_states[user_number] = 'qty_choice' #change state to choose count
                return str(resp)
            elif user_response == "back":
                print("back")
                del user_sessions[user_number]
                return intro_msg(user_number)
            else:
                print("error, please choose a flavor or send 'back' to go back to the previous menu.")
                return str(resp)
        
        #ivida5k
        elif user_sessions[user_number]['brand'] == "IVIDA5K":
            print("5k")
            print("ordered_data: " + str(order_data["ordered"]))
            print(user_response in ivida_5k)
            #user has chosen the right flavor
            if user_response in ivida_5k:
                print(user_response)
                resp.message("Please enter the number of " + user_response + " you would like to order")
                order_data["ivida5k"][user_response] = 0 #add to order data list
                print(f"updated order_data : {order_data['ivida5k']}")
                order_states[user_number] = 'qty_choice' #change state to choose count
                return str(resp)
            elif user_response == "back":
                print("back")
                del user_sessions[user_number]
                return intro_msg(user_number)
            else:
                print("error, please choose a flavor or send 'back' to go back to the previous menu.")
                return str(resp)
        
        #ivida7k
        elif user_sessions[user_number]['brand'] == "IVIDA7K":
            print("7k")
            print("ordered_data: " + str(order_data["ordered"]))
            print(user_response in ivida_5k)
            #user has chosen the right flavor
            if user_response in ivida_7k:
                print(user_response)
                resp.message("Please enter the number of " + user_response + " you would like to order")
                order_data["ivida7k"][user_response] = 0 #add to order data list
                print(f"updated order_data : {order_data['ivida7k']}")
                order_states[user_number] = 'qty_choice' #change state to choose count
                return str(resp)
            elif user_response == "back":
                print("back")
                del user_sessions[user_number]
                return intro_msg(user_number)
            else:
                print("error, please choose a flavor or send 'back' to go back to the previous menu.")
                return str(resp)
        
        #rm
        elif user_sessions[user_number]['brand'] == "RM":
            print("rm")
            print("ordered_data: " + str(order_data["ordered"]))
            print(user_response in ivida_5k)
            #user has chosen the right flavor
            if user_response in RM_choice:
                print(user_response)
                resp.message("Please enter the number of " + user_response + " you would like to order")
                order_data["rm"][user_response] = 0 #add to order data list
                print(f"updated order_data : {order_data['rm']}")
                order_states[user_number] = 'qty_choice' #change state to choose count
                return str(resp)
            elif user_response == "back":
                print("back")
                del user_sessions[user_number]
                return intro_msg(user_number)
            else:
                print("error, please choose a flavor or send 'back' to go back to the previous menu.")
                return str(resp)
        
        

    #User has chosen the category 
    elif curr_session == 'qty_choice':
        print("qty_choice")
        user_response = request.values['Body'].strip().lower()
        print("user response in qty_choice " + str(user_sessions[user_number]))
        
        #zpods
        if user_sessions[user_number]['brand'] == 'ZPODS':
            print(order_data['zpods'])
            res = list(order_data["zpods"].keys())[-1]
            ## if user responds with a number, then we can add it to the cart
            if user_response.isnumeric():
                ## make sure the order cannot be 0 or less
                if int(user_response) < 1 or int(user_response) > 10:
                    resp.message("Please enter a number between 1 and 10")
                    return str(resp)
                else: 
                    current_date = datetime.date.today()
                    print(user_sessions)
                    amnt = float(user_response) * 23.99
                    order_data["zpods"].update({res : int(user_response)})
                    print(order_data)
                    resp.message("added " + user_response + ". Would you like anything else?")
                    order_states[user_number] = 'cart_choice'
                    return str(resp)
            else:
                resp.message("Please enter a number.")
                order_states[user_number] = 'qty_choice'
                return str(resp)
        
        #fgpods
        elif user_sessions[user_number]['brand'] == 'FGPODS':
            print(order_data['fgpods'])
            res = list(order_data['fgpods'].keys())[-1]
            ## if user responds with a number, then we can add it to the cart
            if user_response.isnumeric():
                ## make sure the order cannot be 0 or less
                if int(user_response) < 1 or int(user_response) > 10:
                    resp.message("Please enter a number between 1 and 10")
                    return str(resp)
                else: 
                    current_date = datetime.date.today()
                    print(user_sessions)
                    amnt = float(user_response) * 23.99
                    order_data["fgpods"].update({res : int(user_response)})
                    print(order_data)
                    resp.message("added " + user_response + ". Would you like anything else?")
                    order_states[user_number] = 'cart_choice'
                    return str(resp)
            else:
                resp.message("Please enter a number.")
                order_states[user_number] = 'qty_choice'
                return str(resp)
        
        #ivida5k
        elif user_sessions[user_number]['brand'] == 'IVIDA5K':
            print(order_data['ivida5k'])
            res = list(order_data['ivida5k'].keys())[-1]
            ## if user responds with a number, then we can add it to the cart
            if user_response.isnumeric():
                ## make sure the order cannot be 0 or less
                if int(user_response) < 1 or int(user_response) > 10:
                    resp.message("Please enter a number between 1 and 10")
                    return str(resp)
                else: 
                    current_date = datetime.date.today()
                    print(user_sessions)
                    amnt = float(user_response) * 23.99
                    order_data["ivida5k"].update({res : int(user_response)})
                    print(order_data)
                    resp.message("added " + user_response + ". Would you like anything else?")
                    order_states[user_number] = 'cart_choice'
                    return str(resp)
            else:
                resp.message("Please enter a number.")
                order_states[user_number] = 'qty_choice'
                return str(resp)
        
        #ivida7k
        elif user_sessions[user_number]['brand'] == 'IVIDA7K':
            print(order_data['ivida7k'])
            res = list(order_data['ivida7k'].keys())[-1]
            ## if user responds with a number, then we can add it to the cart
            if user_response.isnumeric():
                ## make sure the order cannot be 0 or less
                if int(user_response) < 1 or int(user_response) > 10:
                    resp.message("Please enter a number between 1 and 10")
                    return str(resp)
                else: 
                    current_date = datetime.date.today()
                    print(user_sessions)
                    amnt = float(user_response) * 23.99
                    order_data["ivida7k"].update({res : int(user_response)})
                    print(order_data)
                    resp.message("added " + user_response + ". Would you like anything else?")
                    order_states[user_number] = 'cart_choice'
                    return str(resp)
            else:
                resp.message("Please enter a number.")
                order_states[user_number] = 'qty_choice'
                return str(resp)
        #RM
        elif user_sessions[user_number]['brand'] == 'RM':
            print(order_data['rm'])
            res = list(order_data['rm'].keys())[-1]
            ## if user responds with a number, then we can add it to the cart
            if user_response.isnumeric():
                ## make sure the order cannot be 0 or less
                if int(user_response) < 1 or int(user_response) > 10:
                    resp.message("Please enter a number between 1 and 10")
                    return str(resp)
                else: 
                    current_date = datetime.date.today()
                    print(user_sessions)
                    amnt = float(user_response) * 23.99
                    order_data["rm"].update({res : int(user_response)})
                    print(order_data)
                    resp.message("added " + user_response + ". Would you like anything else?")
                    order_states[user_number] = 'cart_choice'
                    return str(resp)
            else:
                resp.message("Please enter a number.")
                order_states[user_number] = 'qty_choice'
                return str(resp)
        else:
            resp.message("error")
            order_states[user_number] = 'qty_choice'
            return str(resp)

    
    elif curr_session == 'cart_choice':
        print("cart_choice")
        user_response = request.values['Body'].strip().lower()
        print("user response in cart_choice " + str(user_sessions[user_number]))
        print(user_response)
        if str(user_response).lower() == "yes":
            order_states[user_number] = 'flavor_choice'
            category = get_current_category(str(user_sessions[user_number]['brand']))
            resp.message(list_items(category))
            return str(resp)
        elif str(user_response).lower() == "no":   #checking out 
            resp.message(f"checked out. thank you for your order. your order # is {generate_confirmation_code()}")
            for keys, values in order_data["zpods"].items():
                print(keys, values)
            del user_sessions[user_number]
            order_states[user_number] = 'start'
            clear_cart()
            print(f"cleared cart. order data: {user_sessions}")
            order_states[user_number] = 'start'
            return str(resp)
        else:
            resp.message("error, please enter yes to continue shopping or no to check out.")
            return str(resp)

    
def clear_cart():
    order_data["fgpods"] = {}
    order_data["ivida5k"] = {}
    order_data["ivida7k"] = {}
    order_data["rm"] = {}
    order_data["zpods"] = {}

def list_items(type):
    keys = [key for key, value in type.items() if value > 0]
    flavors = "\n".join(keys)
    message = "Please choose between our flavors: \n" + flavors +  " with the amount. (ex. chew, 3)"  "\n" + "text 'back' to go back"
    return message

def intro_msg(user_number):
    resp = MessagingResponse()
    resp.message("""Welcome to our automated ordering system. Please reply with one of the following options: 
    1 - ZPODS (24.99)
    2 - FG PODS (22.99)
    3 - IVIDA 5k (29.99)
    4 - IVIDA 7K (32.99)
    5 - RM Puff Bars 3.6k (23.99)
                        """)
    order_states[user_number] = 'start'
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
    confirmation_code.upper()
    return confirmation_code

def get_current_category(brand):
            if brand == "ZPODS":
                return z_pod
            elif brand == "FGPODS":
                return fg_choice
            elif brand == "IVIDA5K":
                return ivida_5k
            elif brand == "IVIDA7K":
                return ivida_7k
            else: 
                return RM_choice

if __name__ == "__main__":
    app.run(debug=True)

