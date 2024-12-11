import mysql.connector

from controllers.config import DB_CONFIG
class Payment:
 #Save payment
 def save_payment(payment_id,order_id, card_number, card_name, expiry_date, cvv, amount, payment_status,user_id):
    print("esse", user_id)
    
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor()
    check_query = "SELECT COUNT(*) FROM payments WHERE payment_id = %s"
    cursor.execute(check_query, (payment_id,))
    
    payment_exists = cursor.fetchone()[0] > 0
    
    if payment_exists:
        print("Pagamento existe", payment_exists)
        # update payment information
        update_query = """
        UPDATE payments
        SET card_number = %s, card_name = %s, expiry_date = %s, cvv = %s
        WHERE payment_id = %s AND order_id = %s
        """
        cursor.execute(update_query, (card_number, card_name, expiry_date, cvv, payment_id, order_id))
        conn.commit()  
        print("Pagamento atualizado com sucesso!")
    else:
       

     query = """
    INSERT INTO payments (order_id, card_number, card_name, expiry_date, cvv, amount, payment_status,user_pyment_id
)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """
     cursor.execute(query, (order_id, card_number, card_name, expiry_date, cvv, amount, payment_status,user_id))
     conn.commit()

     cursor.close()
     conn.close()
 
#Update payment information
 def update_payment(payment_id, order_id, card_number, card_name, expiry_date, cvv):
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor()

    # Checks if payment exists
    check_query = "SELECT COUNT(*) FROM payments WHERE payment_id = %s AND order_id = %s"
    cursor.execute(check_query, (payment_id, order_id))
    
    payment_exists = cursor.fetchone()[0] > 0

    if payment_exists:
        print("Pagamento existe", payment_exists)
        # Update payment information
        update_query = """
        UPDATE payments
        SET card_number = %s, card_name = %s, expiry_date = %s, cvv = %s
        WHERE payment_id = %s AND order_id = %s
        """
        cursor.execute(update_query, (card_number, card_name, expiry_date, cvv, payment_id, order_id))
        conn.commit()  
        print("Pagamento atualizado com sucesso!")
    else:
        print("Pagamento não encontrado.")

    cursor.close()  
    conn.close()  
       
#Show payment
 def list_pyment():
   conn = mysql.connector.connect(**DB_CONFIG)
   cursor = conn.cursor(dictionary=True)
        
   cursor.execute("SELECT card_number ,payment_id,order_id, card_name, expiry_date,cvv FROM payments")
   payments = cursor.fetchall()

   cursor.close()
   conn.close()
        
   return payments
 

 #Show payment by id
 def list_pyment_id(user_id):
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor(dictionary=True)
        
        query = "SELECT payment_id,  user_pyment_id,card_number,card_name,expiry_date,cvv  FROM payments WHERE user_pyment_id = %s"
        cursor.execute(query, (user_id,))
        user_id = cursor.fetchall()

        cursor.close()
        conn.close()
        return user_id
 
