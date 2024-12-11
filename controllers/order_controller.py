from controllers.config import DB_CONFIG
from models.order import Order
import mysql.connector
class OderController:
     #Create order
     def register_order(self, user_id, address_id, cart_id):
         Order.create_order(user_id, address_id, cart_id) 
     #Show order   
     def list_order():
         orders = Order.list_order()
         return [{"order_id": order["order_id"], "customer_id": order["customer_id"], "customer_address_id": order["customer_address_id"], "shipping_date": order["shipping_date"], "total_amount": order["total_amount"], "order_status": order["order_status"], "cart_id": order["cart_id"] } for order in orders]
     #Create Order Item
     def register_order_item(self, order_id, product_id, quantity, price):
        Order.create_order_item(order_id, product_id, quantity, price)  
        
    #cart and order id list
     def list_cart_ids_from_orders():
      orders = Order.list_order()
      return [{"order_id": order["order_id"], "customer_id": order["customer_id"], "customer_address_id": order["customer_address_id"], "shipping_date": order["shipping_date"], "total_amount": order["total_amount"], "order_status": order["order_status"], "cart_id": order["cart_id"] } for order in orders]
     

    #Show favorites
     def list_my():
       conn = mysql.connector.connect(**DB_CONFIG)
       cursor = conn.cursor(dictionary=True)
    
       query = """
    SELECT 
        c.cart_id, 
        c.customer_id, 
        c.quantity, 
        c.price, 
        c.id,
        o.order_id, 
        o.customer_address_id, 
        o.shipping_date, 
        o.total_amount, 
        o.order_status
    FROM 
        cart c
    LEFT JOIN 
        orders o 
    ON 
        c.cart_id = o.cart_id
    WHERE 
        o.cart_id IS NOT NULL
    """
    
       cursor.execute(query)
       result = cursor.fetchall()
    
       cursor.close()
       conn.close()
    
       return result
