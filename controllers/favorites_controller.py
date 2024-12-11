from models.favorites import Favorites


class FavoritesController:
    #Save Favorites
    def save_cart_favorites(favorites,user_id):
            
        Favorites.save_fav(favorites,user_id)
   #List favorites 
    def list_fav(self):
     favs = Favorites.fav_list()
     return [{ "id_fav": fav["id_fav"],"id": fav["id"], "image": fav["image"]} for fav in favs]
    #Delete favorites
    def delete_fave(self, id_fav):
        Favorites.delete_fave(id_fav)