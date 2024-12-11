import mysql.connector
from controllers.config import DB_CONFIG
from models.user import User

class UserController:
    #Register users
    def register_user(self, first_name, last_name, email, password):
        User.create_user(first_name, last_name, email, password)

    #show user by id
    def get_user_by_id(customer_id):
        user = User.get_user_by_id(customer_id)
        
        return [{
            "first_name": u["first_name"],
             "last_name": u["last_name"],
             "email": u["email"],
        } for u in user]


    def login(self, email, password):
       
        # Authenticate the user
        user = User.authenticate_user(email, password)
       
        if user:
            return {"status": "success", "customer_id": user["id"]}
        else:
            return {"status": "error", "message": "Usuário ou senha inválidos."}


   
    #Update user
    def update_user(name,last_name,email,user_id):
        User.update_user(name,last_name,email,user_id)
    #logged in user_
    def is_user_logged_in(self, cookies):
        # Replace 'user_id' with the correct cookie name
        return 'user_id' in cookies  
    #Show username
    def get_name(self, customer_id):
        name = User.select_name(customer_id)
        if name:
            return {
                "first_name": name["first_name"],
                
            }
       
