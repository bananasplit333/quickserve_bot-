import random
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
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
COST_ZPOD = 23.99
COST_FG = 22.99
COST_IV5 = 29.99
COST_IV7 = 32.99
COST_RM = 26.99
    

@app.route("/sms", methods=['GET', 'POST'])
def sms_reply():
    # Start our TwiML response
    resp = MessagingResponse()
    user_number = request.values['From']
    print(user_number)
    user_response = request.values['Body'].strip() #user response
    customer_id = database.get_customer_id(user_number)
    print(customer_id)
    global user_sessions
    global order_data
    global ordering
    
    curr_session = order_states.get(user_number, 'start')

    
    #if user is in new session, display intro message
    if curr_session == 'start':
        print(user_response)
        #Initialize session with order_started flag
        user_sessions[user_number] = {'order_started':False}
        if user_response in ["1", "2", "3", "4", "5"]:
            brand_mapping = {"1":"ZPODS", "2":"FGPODS", "3":"IVIDA5K", "4":"IVIDA7K", "5":"RM"}
            user_sessions[user_number]['brand'] = brand_mapping[user_response]
            order_states[user_number] = 'flavor_choice'
            if not order_data['ordered']:
                database.start_order(customer_id)
                order_data['ordered'] = True
            resp.message(list_items(user_response))
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
            if user_response.isnumeric():
                print(user_response)
                available_flavors = get_item_list(1)
                #user has chosen the right flavor
                if available_flavors[int(user_response)-1]:
                    user_sessions[user_number]['last_selected_flavor'] = available_flavors[int(user_response)-1]
                    resp.message("Please enter the number of " + available_flavors[int(user_response)-1] + " you would like to order")
                    order_data["zpods"][available_flavors[int(user_response)-1]] = 0 #add to order data list
                    print(f"updated order_data : {order_data['zpods']}")
                    order_states[user_number] = 'qty_choice' #change state to choose count
                    return str(resp)
                else:
                    print("error, please choose a flavor or text 'back' to go back to the previous menu.")
                    return str(resp)
            elif user_response == "back":
                print("back")
                del user_sessions[user_number]
                return intro_msg(user_number)
            else:
                print("error, please choose a flavor or text 'back' to go back to the previous menu.")
                return str(resp)
            
        #fgpods
        elif user_sessions[user_number]['brand'] == "FGPODS":
            print("fgpods")
            #user has chosen the right flavor
            if user_response.isnumeric():
                print(user_response)
                available_flavors = get_item_list(2)
                #user has chosen the right flavor
                if available_flavors[int(user_response)-1]:
                    user_sessions[user_number]['last_selected_flavor'] = available_flavors[int(user_response)-1]
                    resp.message("Please enter the number of " + available_flavors[int(user_response)-1] + " you would like to order")
                    order_data["fgpods"][available_flavors[int(user_response)-1]] = 0 #add to order data list
                    print(f"updated order_data : {order_data['fgpods']}")
                    order_states[user_number] = 'qty_choice' #change state to choose count
                    return str(resp)
                else:
                    print("error, please choose a flavor or text 'back' to go back to the previous menu.")
                    return str(resp)
            elif user_response == "back":
                print("back")
                del user_sessions[user_number]
                return intro_msg(user_number)
            else:
                print("error, please choose a flavor or text 'back' to go back to the previous menu.")
                return str(resp)
        
        #ivida5k
        elif user_sessions[user_number]['brand'] == "IVIDA5K":
            print("5k")
            #user has chosen the right flavor
            if user_response.isnumeric():
                print(user_response)
                available_flavors = get_item_list(3)
                #user has chosen the right flavor
                if available_flavors[int(user_response)-1]:
                    user_sessions[user_number]['last_selected_flavor'] = available_flavors[int(user_response)-1]
                    resp.message("Please enter the number of " + available_flavors[int(user_response)-1] + " you would like to order")
                    order_data["ivida5k"][available_flavors[int(user_response)-1]] = 0 #add to order data list
                    print(f"updated order_data : {order_data['ivida5k']}")
                    order_states[user_number] = 'qty_choice' #change state to choose count
                    return str(resp)
                else:
                    print("error, please choose a flavor or text 'back' to go back to the previous menu.")
                    return str(resp)
            elif user_response == "back":
                print("back")
                del user_sessions[user_number]
                return intro_msg(user_number)
            else:
                print("error, please choose a flavor or text 'back' to go back to the previous menu.")
                return str(resp)
        
        #ivida7k
        elif user_sessions[user_number]['brand'] == "IVIDA7K":
            print("7k")
            #user has chosen the right flavor
            if user_response.isnumeric():
                print(user_response)
                available_flavors = get_item_list(4)
                #user has chosen the right flavor
                if available_flavors[int(user_response)-1]:
                    user_sessions[user_number]['last_selected_flavor'] = available_flavors[int(user_response)-1]
                    resp.message("Please enter the number of " + available_flavors[int(user_response)-1] + " you would like to order")
                    order_data["ivida7k"][available_flavors[int(user_response)-1]] = 0 #add to order data list
                    print(f"updated order_data : {order_data['ivida7k']}")
                    order_states[user_number] = 'qty_choice' #change state to choose count
                    return str(resp)
                else:
                    print("error, please choose a flavor or text 'back' to go back to the previous menu.")
                    return str(resp)
            elif user_response == "back":
                print("back")
                del user_sessions[user_number]
                return intro_msg(user_number)
            else:
                print("error, please choose a flavor or text 'back' to go back to the previous menu.")
                return str(resp)
        
        #rm
        elif user_sessions[user_number]['brand'] == "RM":
            print("rm")
            #user has chosen the right flavor
            if user_response.isnumeric():
                print(user_response)
                available_flavors = get_item_list(5)
                #user has chosen the right flavor
                if available_flavors[int(user_response)-1]:
                    user_sessions[user_number]['last_selected_flavor'] = available_flavors[int(user_response)-1]
                    resp.message("Please enter the number of " + available_flavors[int(user_response)-1] + " you would like to order")
                    order_data["rm"][available_flavors[int(user_response)-1]] = 0 #add to order data list
                    print(f"updated order_data : {order_data['rm']}")
                    order_states[user_number] = 'qty_choice' #change state to choose count
                    return str(resp)
                else:
                    print("error, please choose a flavor or text 'back' to go back to the previous menu.")
                    return str(resp)
            elif user_response == "back":
                print("back")
                del user_sessions[user_number]
                return intro_msg(user_number)
            else:
                print("error, please choose a flavor or text 'back' to go back to the previous menu.")
                return str(resp)
        
        

    #User has chosen the category 
    elif curr_session == 'qty_choice':
        print("qty_choice")
        user_response = request.values['Body'].strip().lower()
        print("user response in qty_choice " + str(user_sessions[user_number]))
        
        #zpods
        if user_sessions[user_number]['brand'] == 'ZPODS':
            print(order_data['zpods'])
            res = user_sessions[user_number]['last_selected_flavor'] 
            ## if user responds with a number, then we can add it to the cart
            if user_response.isnumeric():
                ## make sure the order cannot be 0 or less
                if int(user_response) < 1 or int(user_response) > 10:
                    resp.message("Please enter a number between 1 and 10")
                    return str(resp)
                else: 
                    print(user_sessions)
                    if (database.add_to_cart(customer_id, res, 1, user_response)):
                        order_data["zpods"].update({res : int(user_response)})
                        resp.message("Added " + user_response + "." + "\n"  + "Would you like to keep shopping?" + "\n" + "Please text 'Y' to continue or 'N' to check out.")
                        order_states[user_number] = 'cart_choice'
                        return str(resp)
                    else:
                        remaining_stock = database.get_inventory_stock(res, 1)
                        resp.message(f"Error: not enough left in stock. \nREMAINING STOCK: {remaining_stock}\n\n{list_items(1)}")
                        order_states[user_number] = 'flavor_choice'    
                        return str(resp)
            else:
                resp.message("Please enter a number.")
                order_states[user_number] = 'qty_choice'
                return str(resp)
        
        #fgpods
        elif user_sessions[user_number]['brand'] == 'FGPODS':
            print(order_data['fgpods'])
            res = user_sessions[user_number]['last_selected_flavor'] 
            ## if user responds with a number, then we can add it to the cart
            if user_response.isnumeric():
                ## make sure the order cannot be 0 or less
                if int(user_response) < 1 or int(user_response) > 10:
                    resp.message("Please enter a number between 1 and 10")
                    return str(resp)
                else: 
                    print(user_sessions)
                    if (database.add_to_cart(customer_id, res, 2, user_response)):
                        order_data["fgpods"].update({res : int(user_response)})
                        resp.message("Added " + user_response + "." + "\n"  + "Would you like to keep shopping?" + "\n" + "Please text 'Y' to continue or 'N' to check out.")
                        order_states[user_number] = 'cart_choice'
                        return str(resp)
                    else:
                        remaining_stock = database.get_inventory_stock(res, 2)
                        resp.message(f"Error: not enough left in stock. \nREMAINING STOCK: {remaining_stock}\n\n{list_items(2)}")
                        order_states[user_number] = 'flavor_choice'    
                        return str(resp)
            else:
                resp.message("Please enter a number.")
                order_states[user_number] = 'qty_choice'
                return str(resp)
        
        #ivida5k
        elif user_sessions[user_number]['brand'] == 'IVIDA5K':
            print(order_data['ivida5k'])
            res = user_sessions[user_number]['last_selected_flavor'] 
            ## if user responds with a number, then we can add it to the cart
            if user_response.isnumeric():
                ## make sure the order cannot be 0 or less
                if int(user_response) < 1 or int(user_response) > 10:
                    resp.message("Please enter a number between 1 and 10")
                    return str(resp)
                else: 
                    print(user_sessions)
                    if (database.add_to_cart(customer_id, res, 3, user_response)):
                        order_data["zpods"].update({res : int(user_response)})
                        resp.message("Added " + user_response + "." + "\n"  + "Would you like to keep shopping?" + "\n" + "Please text 'Y' to continue or 'N' to check out.")
                        order_states[user_number] = 'cart_choice'
                        return str(resp)
                    else:
                        remaining_stock = database.get_inventory_stock(res, 3)
                        resp.message(f"Error: not enough left in stock. \nREMAINING STOCK: {remaining_stock}\n\n{list_items(3)}")
                        order_states[user_number] = 'flavor_choice'    
                        return str(resp)
            else:
                resp.message("Please enter a number.")
                order_states[user_number] = 'qty_choice'
                return str(resp)
        
        #ivida7k
        elif user_sessions[user_number]['brand'] == 'IVIDA7K':
            print(order_data['ivida7k'])
            res = user_sessions[user_number]['last_selected_flavor'] 
            ## if user responds with a number, then we can add it to the cart
            if user_response.isnumeric():
                ## make sure the order cannot be 0 or less
                if int(user_response) < 1 or int(user_response) > 10:
                    resp.message("Please enter a number between 1 and 10")
                    return str(resp)
                else: 
                    print(user_sessions)
                    if (database.add_to_cart(customer_id, res, 4, user_response)):
                        order_data["zpods"].update({res : int(user_response)})
                        resp.message("Added " + user_response + "." + "\n"  + "Would you like to keep shopping?" + "\n" + "Please text 'Y' to continue or 'N' to check out.")
                        order_states[user_number] = 'cart_choice'
                        return str(resp)
                    else:
                        remaining_stock = database.get_inventory_stock(res, 4)
                        resp.message(f"Error: not enough left in stock. \nREMAINING STOCK: {remaining_stock}\n\n{list_items(4)}")
                        order_states[user_number] = 'flavor_choice'    
                        return str(resp)
            else:
                resp.message("Please enter a number.")
                order_states[user_number] = 'qty_choice'
                return str(resp)
        #RM
        elif user_sessions[user_number]['brand'] == 'RM':
            print(order_data['rm'])
            res = user_sessions[user_number]['last_selected_flavor'] 
            ## if user responds with a number, then we can add it to the cart
            if user_response.isnumeric():
                ## make sure the order cannot be 0 or less
                if int(user_response) < 1 or int(user_response) > 10:
                    resp.message("Please enter a number between 1 and 10")
                    return str(resp)
                else: 
                    print(user_sessions)
                    if (database.add_to_cart(customer_id, res, 5, user_response)):
                        order_data["zpods"].update({res : int(user_response)})
                        resp.message("Added " + user_response + "." + "\n"  + "Would you like to keep shopping?" + "\n" + "Please text 'Y' to continue or 'N' to check out.")
                        order_states[user_number] = 'cart_choice'
                        return str(resp)
                    else:
                        remaining_stock = database.get_inventory_stock(res, 5)
                        resp.message(f"Error: not enough left in stock. \nREMAINING STOCK: {remaining_stock}\n\n{list_items(5)}")
                        order_states[user_number] = 'flavor_choice'    
                        return str(resp)
            else:
                resp.message("Please enter a number.")
                order_states[user_number] = 'qty_choice'
                return str(resp)
        else:
            resp.message("error")
            order_states[user_number] = 'qty_choice'
            return str(resp)

    #User choosing between checkout and continuing 
    elif curr_session == 'cart_choice':
        print("cart_choice")
        user_response = request.values['Body'].strip().lower()
        print("user response in cart_choice " + str(user_sessions[user_number]))
        print(user_response)
        if str(user_response).lower() == "y":
            order_states[user_number] = 'flavor_choice'
            category = get_current_category(str(user_sessions[user_number]['brand']))
            resp.message(list_items(category))
            return str(resp)
        elif str(user_response).lower() == "n":   #checking out
            total_cost = float(database.get_total_cost(customer_id)) # get total cost of order 
            confirmation_code = generate_confirmation_code() #confirmation code
            resp.message(f"ORDER SUMMARY: \n{list_order(customer_id)} \n\nThank you for your order.\nYour total is: ${total_cost}.\nYour confirmation code is: {confirmation_code}")

            del user_sessions[user_number] #change this soon!! 
            order_data['ordered'] = False #end order session 
            database.finalize_cart(customer_id, confirmation_code)
            clear_cart()
            
            print(f"cleared cart. order data: {user_sessions}")
            order_states[user_number] = 'start'
            return str(resp)
        else:
            resp.message("Error, please text 'Y' to continue shopping or 'N' to check out.")
            return str(resp)
    else:
        print("fringe else case entered")
        



def clear_cart():
    order_data["fgpods"] = {}
    order_data["ivida5k"] = {}
    order_data["ivida7k"] = {}
    order_data["rm"] = {}
    order_data["zpods"] = {}

def list_items(category_id):
    product_list = database.get_product_list(category_id)
    indexed_flavors = [f'{index}. {flavor.replace("_", " ")}' for index, (_, flavor, _, _, _) in enumerate(product_list, start=1)]
    flavors = "\n".join(indexed_flavors)
    message = "Please choose between our flavors: \n" + flavors +"\n" + "text 'back' to go back"
    return message

def intro_msg(user_number):
    resp = MessagingResponse()
    resp.message(f"""Welcome to our automated ordering system. Please reply with one of the following options: 
    \nSTLTH PODS
    1 - ZPODS ({COST_ZPOD})
    2 - FG PODS ({COST_FG})
    \nDISPOSABLES:
    3 - IVIDA 5k ({COST_IV5})
    4 - IVIDA 7K ({COST_IV7})
    5 - RM Puff Bars 3.6k ({COST_RM})
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

"""def get_total():
    for category, items in order_data.items():"""

def get_current_category(brand):
            if brand == "ZPODS":
                return 1
            elif brand == "FGPODS":
                return 2
            elif brand == "IVIDA5K":
                return 3
            elif brand == "IVIDA7K":
                return 4
            else:
                return 5
            
def list_order(customer_id):
    order_summary = database.get_order_summary(customer_id)
    indexed_order = [f'{name} - {qty}' for _, _, _, qty, _, name in order_summary]
    order_list = "\n".join(indexed_order)
    return order_list

def calculate_total():
    total_sum = 0
    for category, products in order_data.items():
        if category != "ordered":
            for _, qty in products.items():
                if category == "zpods":
                    total_sum += (qty * COST_ZPOD)
                elif category == "fgpods":
                    total_sum += (qty * COST_FG)
                elif category == "ivida5k":
                    total_sum += (qty * COST_IV5)
                elif category == "ivida7k":
                    total_sum += (qty * COST_IV7)
                else:
                    total_sum += (qty * COST_RM)
    return round(total_sum,2)

def get_item_list(category_id):
    product_list = database.get_product_list(category_id)
    indexed_flavors = [f'{flavor.replace("_", " ")}' for _, flavor, _, _, qty in product_list]
    return indexed_flavors

if __name__ == "__main__":
    app.run(debug=True)

