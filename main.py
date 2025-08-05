from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import db_helper
import generic_helper

app = FastAPI()
inprogress_orders = {}

@app.post("/")
async def handle_request(request: Request):
    payload = await request.json()
    intent = payload['queryResult']['intent']['displayName']
    parameters = payload['queryResult']['parameters']
    output_contexts = payload['queryResult']['outputContexts']
    session_id = generic_helper.extract_session_id(output_contexts[0]["name"])

    intent_handler_dict = {
        'order.add - context: ongoing-order': add_to_order,
        'order.remove - context: ongoing-order': remove_from_order,
        'order.complete - context: ongoing-order': complete_order,
        'track.order - context: ongoing-tracking': track_order
    }

    handler = intent_handler_dict.get(intent)
    if handler:
        return handler(parameters, session_id)
    else:
        return JSONResponse(content={"fulfillmentText": "Sorry, I didn't understand that request."})

def save_to_db(order: dict):
    next_order_id = db_helper.get_next_order_id()
    print(f"🗃 Saving order #{next_order_id}: {order}")

    for food_item, quantity in order.items():
        rcode = db_helper.insert_order_item(food_item, quantity, next_order_id)
        if rcode == -1:
            print("Insertion failed, rolling back entire order")
            return -1

    db_helper.insert_order_tracking(next_order_id, "in progress")
    return next_order_id

def complete_order(parameters: dict, session_id: str):
    if session_id not in inprogress_orders:
        return JSONResponse(content={
            "fulfillmentText": "I'm having a trouble finding your order. Sorry! Can you place a new order please?"
        })

    order = inprogress_orders[session_id]
    order_id = save_to_db(order)

    if order_id == -1:
        return JSONResponse(content={
            "fulfillmentText": "Sorry, I couldn't process your order due to a backend error. Please place a new order again"
        })

    order_total = db_helper.get_total_order_price(order_id)
    if order_total is None:
        return JSONResponse(content={
            "fulfillmentText": f"Your order #{order_id} was saved but we couldn't calculate the price. Please contact support."
        })

    del inprogress_orders[session_id]
    return JSONResponse(content={
        "fulfillmentText": f"Awesome. We have placed your order. "
                           f"Here is your order id # {order_id}. "
                           f"Your order total is {order_total} which you can pay at the time of delivery!"
    })

def add_to_order(parameters: dict, session_id: str):
    food_items = parameters["food-item"]
    quantities = parameters["number"]

    if isinstance(food_items, str):
        food_items = [food_items]
    if isinstance(quantities, int):
        quantities = [quantities]

    if len(food_items) != len(quantities):
        return JSONResponse(content={
            "fulfillmentText": "Sorry I didn't understand. Can you please specify food items and quantities clearly?"
        })

    new_food_dict = dict(zip(food_items, quantities))
    current_order = inprogress_orders.get(session_id, {})
    current_order.update(new_food_dict)
    inprogress_orders[session_id] = current_order

    order_str = generic_helper.get_str_from_food_dict(current_order)
    return JSONResponse(content={
        "fulfillmentText": f"So far you have: {order_str}. Do you need anything else?"
    })

def remove_from_order(parameters: dict, session_id: str):
    if session_id not in inprogress_orders:
        return JSONResponse(content={
            "fulfillmentText": "I'm having a trouble finding your order. Sorry! Can you place a new order please?"
        })

    food_items = parameters["food-item"]
    current_order = inprogress_orders[session_id]

    removed_items = []
    no_such_items = []

    for item in food_items:
        if item in current_order:
            removed_items.append(item)
            del current_order[item]
        else:
            no_such_items.append(item)

    fulfillment_text = ""
    if removed_items:
        fulfillment_text += f"Removed {', '.join(removed_items)} from your order!"
    if no_such_items:
        fulfillment_text += f" Your current order does not have {', '.join(no_such_items)}."
    if not current_order:
        fulfillment_text += " Your order is empty!"
    else:
        order_str = generic_helper.get_str_from_food_dict(current_order)
        fulfillment_text += f" Here is what is left in your order: {order_str}, Wanna add anything else?"

    return JSONResponse(content={"fulfillmentText": fulfillment_text})

def track_order(parameters: dict, session_id: str):
    try:
        order_id = int(parameters.get("order_id") or parameters.get("number", -1))
        if order_id == -1:
            return JSONResponse(content={
                "fulfillmentText": "Sorry, I couldn't understand the order ID you gave. Can you try again?"
            })

        order_status = db_helper.get_order_status(order_id)

        if order_status:
            fulfillment_text = f"The order status for order ID {order_id} is: {order_status}"
        else:
            fulfillment_text = f"No order found with order ID: {order_id}"

        return JSONResponse(content={"fulfillmentText": fulfillment_text})

    except Exception as e:
        print("Error in track_order:", e)
        return JSONResponse(content={
            "fulfillmentText": "Something went wrong while checking your order status. Please try again later."
        })
