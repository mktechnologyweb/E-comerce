import mysql.connector
from controllers.config import DB_CONFIG

class Cart:
    def __init__(self, customer_id ):
        self.user_id = customer_id 
        self.items = []
        
    @staticmethod
    #Show Cart
    def list_cart():
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor(dictionary=True)
        
        cursor.execute("")
        carts = cursor.fetchall()

        cursor.close()
        conn.close()
        
        return carts
        
   
  

