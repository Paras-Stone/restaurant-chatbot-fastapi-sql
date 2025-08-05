"""
import mysql.connector
global cnx

cnx = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Paras@123",
    database="pandeyji_eatery"
)
print(cnx)

def insert_order_item(food_item, quantity, order_id):   #stored procedure
    try:
        cursor = cnx.cursor()
        cursor.callproc("insert_order_item", (food_item, quantity, order_id))
        cnx.commit()
        cursor.close()

        print("Order item inserted successfully!")

        return 1

    except mysql.connector.Error as err:
        print(f"Error inserting order item: {err}")

        cnx.rollback()
        return -1

    except Exception as e:
        print(f"An error occurred : {e}")

        cnx.rollback()

        return -1

def insert_order_tracking(order_id, status):
    cursor = cnx.cursor()

    insert_query = "INSERT INTO order_tracking (order_id, status) VALUES (%s, %s)"
    cursor.execute(insert_query, (order_id, status))
    cnx.commit()
    cursor.close()

def get_total_order_price(order_id):    #stored procedure
    cursor = cnx.cursor()

    query = f"SELECT get_total_order_price({order_id})"
    cursor.execute(query)
    result = cursor.fetchone()[0]
    cursor.close()

    return result

def get_next_order_id():
    cursor = cnx.cursor()

    query = "SELECT MAX(order_id) FROM orders"
    cursor.execute(query)
    result = cursor.fetchone()[0]
    cursor.close()

    if result is None:
        return 1
    else:
        return result + 1

def get_order_status(order_id : int):

    cursor = cnx.cursor()

    query = f"SELECT status FROM order_tracking where order_id = {order_id}"
    cursor.execute(query)
    result = cursor.fetchone()
    cursor.close()

    if result:
        #(testing) print(result[0])
        return result[0]
    else:
        return None

if __name__ == "__main__":
    pass
    #working #print(get_total_order_price(4))
    #working # insert_order_item('samosas', 2, 56)
    #working # insert_order_tracking(99, "in progress")
    #working # get_order_status(4)
    #working # print(get_next_order_id())
    #all working
"""

import mysql.connector
global cnx

cnx = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Paras@123",
    database="pandeyji_eatery"
)
print("✅ Connected to MySQL:", cnx)

def insert_order_item(food_item, quantity, order_id):  # stored procedure
    try:
        cursor = cnx.cursor()
        cursor.callproc("insert_order_item", (food_item, quantity, order_id))
        cnx.commit()
        cursor.close()

        print(f"✅ Inserted: {quantity}x {food_item} into order {order_id}")
        return 1

    except mysql.connector.Error as err:
        print(f"❌ MySQL Error inserting order item: {err}")
        cnx.rollback()
        return -1

    except Exception as e:
        print(f"❌ General error inserting order item: {e}")
        cnx.rollback()
        return -1

def insert_order_tracking(order_id, status):
    try:
        cursor = cnx.cursor()
        insert_query = "INSERT INTO order_tracking (order_id, status) VALUES (%s, %s)"
        cursor.execute(insert_query, (order_id, status))
        cnx.commit()
        cursor.close()
        print(f"✅ Order tracking added: {order_id} - {status}")
    except Exception as e:
        print(f"❌ Failed to insert into order_tracking: {e}")
        cnx.rollback()

def get_total_order_price(order_id):  # stored procedure
    cursor = cnx.cursor()
    try:
        query = f"SELECT get_total_order_price({order_id})"
        cursor.execute(query)
        result = cursor.fetchone()[0]
        return result
    except Exception as e:
        print(f"❌ Failed to get total price: {e}")
        return None
    finally:
        cursor.close()

def get_next_order_id():
    cursor = cnx.cursor()
    query = "SELECT MAX(order_id) FROM orders"
    cursor.execute(query)
    result = cursor.fetchone()[0]
    cursor.close()
    return 1 if result is None else result + 1

def get_order_status(order_id: int):
    cursor = cnx.cursor()
    try:
        query = f"SELECT status FROM order_tracking WHERE order_id = {order_id}"
        cursor.execute(query)
        result = cursor.fetchone()
        return result[0] if result else None
    except Exception as e:
        print(f"❌ Error fetching order status: {e}")
        return None
    finally:
        cursor.close()


print(get_order_status(34))
