from models.categorie import Category

class CategoryController:
   #Show categories
   def list_categories(self):
        categories = Category.list_categories()
        return [{"id_categoria": category["id_categoria"], "name": category["nome_categoria"]} for category in categories]
   #Show categories by id 
   def list_products_by_category(category_id):
           category_name, products = Category.list_products_by_category(category_id)

           return {
        "category_name": category_name,
        "products": [{
            "id": product["id"],
            "name": product["name"],
            "discount_price": product["discount_price"],
            "product_rating": product["product_rating"],
            "price": product["price"],
            "images": product["images"],
            "id_categoria": product["id_categoria"],
        } for product in products]
    }

   #Show sub categories by id 
   def list_subItem_category(category_id):
       subItem = Category.list_subItem_category(category_id)

       return [{"nome_categoria": item["nome_categoria"], "id_categoria": item["id_categoria"]} for item in subItem]
   
   #Show sub categories by id
   def get_category_names(id_sub_item):
       subItem_name = Category.get_category_names(id_sub_item)
       
       return [{"parent_category_name": item["parent_category_name"], "subcategory_name": item["subcategory_name"], "id_1": item["id_1"], "id_2": item["id_2"]} for item in subItem_name]
   #Show sub item
   def list_sub_item(id_sub_item):
        
        products = Category.list_products_by_subcategory(id_sub_item)

        return [{
            "product_id": product["product_id"],
            "product_name": product["product_name"],
            "discount_price": product["discount_price"],
            "product_rating": product["product_rating"],
            "product_price": product["product_price"],
            "product_image": product["product_image"],
            "id_categoria": product["id_categoria"],
        } for product in products]
    
   #Show category by price 
   def category_price_cont(product_price):
        price = Category.category_price_cont(product_price)
        return [{"categoria": c["categoria"], "categoria_pai": c["categoria_pai"], "id_categoria": c["id_categoria"],"id_categoria_pai": c["id_categoria_pai"]}for c in price]
     
   #List main category 
   def category_pai_category(id_categoria_pai=None, id_categoria=None):
     products = Category.list_products_by_subcategory(id_categoria_pai, id_categoria)
     return [{
            "product_id": product["product_id"],
            "product_name": product["product_name"],
            "discount_price": product["discount_price"],
            "product_rating": product["product_rating"],
            "product_price": product["product_price"],
            "product_image": product["product_image"],
            "id_categoria": product["id_categoria"],
            "categoria_pai": product["categoria_pai"],
            "categoria_vo": product["categoria_vo"],
            "categoria": product["categoria"]
        } for product in products]
   #List main category
   def category_pai_category(id_categoria_pai=None, id_categoria=None):
     products = Category.list_products_by_subcategory(id_categoria_pai, id_categoria)
     try:
      return [{
            "product_id": product["product_id"],
            "product_name": product["product_name"],
            "discount_price": product["discount_price"],
            "product_rating": product["product_rating"],
            "product_price": product["product_price"],
            "product_image": product["product_image"],
            "id_categoria": product["id_categoria"],
            "categoria_pai": product["categoria_pai"],
            "categoria_vo": product["categoria_vo"],
            "id_categoria": product["id_categoria"],
            "id_vo": product["id_vo"],
            "id_pai": product["id_pai"],
            "categoria": product["categoria"]
        } for product in products]
     except KeyError: 'categoria'
     return [{
            "product_id": product["product_id"],
            "product_name": product["product_name"],
            "discount_price": product["discount_price"],
            "product_rating": product["product_rating"],
            "product_price": product["product_price"],
            "product_image": product["product_image"],
            "id_categoria": product["id_categoria"],
            "categoria_pai": product["categoria_pai"],
            "id_pai": product["id_pai"],
            "id_vo": product["id_vo"],
            "categoria_vo": product["categoria_vo"]
            
        } for product in products]
   #List category category
   def category_category_category(id_categoria):
     products = Category.list_products_by_subcategory_subcategory(id_categoria)
     
     return [{
            "product_id": product["product_id"],
            "product_name": product["product_name"],
            "discount_price": product["discount_price"],
            "product_rating": product["product_rating"],
            "product_price": product["product_price"],
            "product_image": product["product_image"],
            "id_categoria": product["id_categoria"],
            "categoria_pai": product["categoria_pai"],
            "categoria_vo": product["categoria_vo"],
            "id_categoria": product["id_categoria"],
            "id_vo": product["id_vo"],
            "id_pai": product["id_pai"],
            "categoria": product["categoria"]
        } for product in products]