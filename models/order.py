import mysql.connector
from controllers.config import DB_CONFIG

class Order:
 #Create order
 def create_order(customer_id, customer_address_id, cart_id):
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()

        query = """
        INSERT INTO orders (customer_id, customer_address_id, order_status, cart_id)
        VALUES (%s, %s, %s, %s)
        """
        #Initially set to "Pending"
        cursor.execute(query, (customer_id, customer_address_id, 'Pending', cart_id)) 
        conn.commit()

        cursor.close()
        conn.close()
 #Create Order Item
 def create_order_item(order_id, product_id, quantity, price):
   conn = mysql.connector.connect(**DB_CONFIG)
   cursor = conn.cursor(dictionary=True)
    
    # Checks if the item has already been added to the order
   query_check = """
    SELECT * FROM order_item 
    WHERE order_id = %s AND product_id = %s
    """
   cursor.execute(query_check, (order_id, product_id))
   result = cursor.fetchone()
    
   if result:
        print(f"Item já existe no pedido: Order ID {order_id}, Product ID {product_id}")
        # If the item already exists, you can choose to update the quantity or ignore it.
        #Quantity update example:
        new_quantity = result['quantity'] + quantity
        query_update = """
        UPDATE order_item 
        SET quantity = %s, price = %s 
        WHERE order_id = %s AND product_id = %s
        """
        cursor.execute(query_update, (new_quantity, price, order_id, product_id))
   else:
        # If the item does not exist, insert a new record
        print(f"Criando novo item no pedido: Order ID {order_id}, Product ID {product_id}")
        query_insert = """
        INSERT INTO order_item (order_id, product_id, quantity, price)
        VALUES (%s, %s, %s, %s)
        """
        cursor.execute(query_insert, (order_id, product_id, quantity, price))
    
        conn.commit()
        cursor.close()
        conn.close()
 #Show order
 @staticmethod
 def list_order():
   conn = mysql.connector.connect(**DB_CONFIG)
   cursor = conn.cursor(dictionary=True)
        
   cursor.execute("SELECT order_id, customer_id, customer_address_id, shipping_date, total_amount, order_status, cart_id  FROM orders")
   order = cursor.fetchall()

   cursor.close()
   conn.close()
        
   return order
        

