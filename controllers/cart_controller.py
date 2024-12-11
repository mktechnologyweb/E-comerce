import json

from models.cart import Cart
import mysql.connector
from controllers.config import DB_CONFIG
from http.cookies import SimpleCookie
class CartController:
       
  #Save to cart    
  def save_cart(self, customer_id, cart_items):
        # Connecting to the database
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()

        for item in cart_items:
            # Checks if the item already exists in the customer's cart
            cursor.execute(
                "SELECT quantity FROM cart WHERE customer_id = %s AND id = %s",
                (customer_id, item['id'])
            )
            existing_item = cursor.fetchone()

            if existing_item:
                # If the item already exists in the cart, update the quantity and price
                new_quantity = existing_item[0] + item['quantity']
                print(new_quantity)
                
                cursor.execute(
                    "UPDATE cart SET quantity = %s, price = %s, totalPriceElement = %s WHERE customer_id = %s AND id = %s",
                    (new_quantity, item['price'], item['totalPriceElement'], customer_id, item['id'])
                )
           
            else:
                # If the item does not exist, insert a new item into the cart
              
                cursor.execute(
                    "INSERT INTO cart (customer_id, id, quantity, price,totalPriceElement) VALUES (%s, %s, %s, %s, %s)",
                    (customer_id, item['id'], item['quantity'], item['price'],item['totalPriceElement'])
                )

        #Confirm the transaction
        conn.commit()
        cursor.close()
        conn.close()
  #Show products  
  def list_cart(self, customer_id):
      
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()

        cursor.execute("SELECT product.product_image,product.product_name,product.product_mark,cart.id,cart.cart_id,cart.quantity,cart.price,cart.totalPriceElement FROM product INNER JOIN cart ON product.product_id = cart.id  WHERE customer_id = %s", (customer_id,))
        carts = cursor.fetchall()

        cursor.close()
        conn.close()

        return [{"product_image": cart[0],"product_name": cart[1], "product_mark": cart[2], "id": cart[3], "cart_id": cart[4], "quantity": cart[5], "price": cart[6], "totalPriceElement": cart[7]} for cart in carts]
  #delete products from cart
  def delet_cart(self,cart_id):
       conn = mysql.connector.connect(**DB_CONFIG)
       cursor = conn.cursor()

       query = "DELETE FROM cart WHERE cart_id  = %s"
       cursor.execute(query, (cart_id ,))
       conn.commit()

       cursor.close()
       conn.close() 
  