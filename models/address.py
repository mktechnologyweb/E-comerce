import mysql.connector
from controllers.config import DB_CONFIG

class Address:
    #Update address
    @staticmethod
    def save_or_update_address(user_id, address_id, street, number, neighborhood, complement, city, state, zip_code):
    # Database connection
     conn = mysql.connector.connect(**DB_CONFIG)
     cursor = conn.cursor()

    #Check if an address with the same user_id and address_id already exists
     check_query = "SELECT COUNT(*) FROM address WHERE user_id = %s AND address_id = %s"
     cursor.execute(check_query, (user_id, address_id))
     
     address_exists = cursor.fetchone()[0] > 0

     if address_exists:
        # If the address already exists, do an UPDATE
        update_query = """
        UPDATE address
        SET street = %s, number = %s, neighborhood = %s, complement = %s, city = %s, state = %s, zip_code = %s
        WHERE user_id = %s AND address_id = %s
        """
        cursor.execute(update_query, (street, number, neighborhood, complement, city, state, zip_code, user_id, address_id))
       
     else:
        # If the address does not exist, do an INSERT
        insert_query = """
        INSERT INTO address (user_id, address_id, street, number, neighborhood, complement, city, state, zip_code)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(insert_query, (user_id, address_id, street, number, neighborhood, complement, city, state, zip_code))

    # Commit changes and close connection
     conn.commit()
     cursor.close()
     conn.close()
    #Show address
    @staticmethod
    def list_address():
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor(dictionary=True)
        
        cursor.execute("SELECT address_id,user_id,street,number,neighborhood,complement,city,state,zip_code FROM address")
        address = cursor.fetchall()

        cursor.close()
        conn.close()
        
        return address
    
    #Show address
    @staticmethod
    def get_address_id(user_id):
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor(dictionary=True)
        
        query = "SELECT address_id, user_id FROM address WHERE user_id = %s"
        cursor.execute(query, (user_id,))
        user_id = cursor.fetchall()

        cursor.close()
        conn.close()
        return user_id