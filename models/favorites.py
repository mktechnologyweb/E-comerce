import mysql.connector
from controllers.config import DB_CONFIG

class Favorites:
 #Save Favorites
 def save_fav(favorites,user_id):
       
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        for item in favorites:
        #Check if id is already in database
         cursor.execute("SELECT * FROM favorites WHERE id = %s", (item['id'],))
         result = cursor.fetchone()
        
         if result:
            print(f"onclick(alert('Produto com ID {item['id']} já está salvo nos favoritos.))")
         else:
            # Insert the favorite into the database
            cursor.execute(
                "INSERT INTO favorites (id, image,id_user) VALUES (%s, %s,%s)",
                (item['id'], item['image'],user_id)
            )
            print(f"Produto com ID {item['id']} adicionado aos favoritos.")
           
    # Confirm the transaction
        conn.commit()
        cursor.close()
        conn.close()
 #List favorites       
 def fav_list():
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT id_fav, id, image FROM favorites")
    favorits = cursor.fetchall()
    
    
    cursor.close()
    conn.close()
    return favorits
 #Delete favorites
 def delete_fave(id_fav):
       conn = mysql.connector.connect(**DB_CONFIG)
      
       cursor = conn.cursor()

       query = "DELETE FROM favorites WHERE id_fav = %s"
       cursor.execute(query, (id_fav,))
       conn.commit()

       cursor.close()
       conn.close() 