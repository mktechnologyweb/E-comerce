import bcrypt
import mysql.connector
from controllers.config import DB_CONFIG

class User:
    #Register users
    @staticmethod
    def create_user(first_name, last_name, email, password):
       
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()

        
        query = """
        INSERT INTO customer (first_name, last_name, email, password)
        VALUES (%s, %s, %s, %s)
        """
        cursor.execute(query, (first_name, last_name, email, hashed_password))

       
        conn.commit()
        cursor.close()
        conn.close()

    @staticmethod
    #Check email
    def get_user_by_email(email):
       
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor(dictionary=True)

       
        query = "SELECT * FROM customer WHERE email = %s"
        cursor.execute(query, (email,))
        user = cursor.fetchone()

        
        cursor.close()
        conn.close()
        return user

    def __init__(self, first_name, last_name, email, password):
        #Initializes client attributes
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password

    #authenticate user
    def authenticate_user(email, password):
     conn = mysql.connector.connect(**DB_CONFIG)
     cursor = conn.cursor()
     query = "SELECT customer_id, password,email FROM customer WHERE email = %s"
     cursor.execute(query, (email,))
     result = cursor.fetchone()
     
     if result:
        customer_id, hashed_password,email = result
       
        # The hashed password must be in bytes for verification
        if isinstance(hashed_password, str):
          
            hashed_password = hashed_password.encode('utf-8')
            
        if bcrypt.checkpw(password.encode('utf-8'), hashed_password):
            return {"id": customer_id, "email":email }

     return None

    @staticmethod
    #show user by id
    def get_user_by_id(customer_id):
        # Conexão com o banco de dados
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor(dictionary=True)

        # Consulta o cliente pelo ID
        query = "SELECT * FROM customer WHERE customer_id = %s"
        cursor.execute(query, (customer_id,))
        user = cursor.fetchall()

        # Fechamento da conexão
        cursor.close()
        conn.close()

        return user

    def __init__(self, username, password, email):
        self.username = username
        self.password = password
        self.email = email
    #Update user
    def update_user(name,last_name,email,user_id):
         conn = mysql.connector.connect(**DB_CONFIG)
         cursor = conn.cursor(dictionary=True)
         
         query = "UPDATE customer SET first_name = %s,last_name = %s,email= %s WHERE customer_id = %s"
         cursor.execute(query, (name,last_name,email,user_id))
         conn.commit()

         cursor.close()
         conn.close()
        


    @staticmethod
    #Show logged in user name
    def select_name(customer_id ):
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor(dictionary=True)
        
        query = "SELECT customer_id , first_name FROM customer WHERE customer_id = %s"
        cursor.execute(query, (customer_id,))
        name = cursor.fetchone()

        cursor.close()
        conn.close()
        return name