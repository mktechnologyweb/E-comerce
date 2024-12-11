from models.product import Product

class ProductController:
    #Show products
    def list_products(self):
        products = Product.list_products()
        return [
            {
                "id": product["product_id"],
                "name": product["product_name"],
                "price": product["product_price"],
                "discount_price": product["discount_price"],
                "product_rating": product["product_rating"],
                "id_categoria": product["id_categoria"],
                "images": product["product_image"]
            }
            for product in products
        ]
    #Show products by id
    def get_product_by_id(self, product_id):
        product = Product.get_product_by_id(product_id)
        if product:
            return {
                "product_id": product["product_id"],
                "product_name": product["product_name"],
                "product_mark": product["product_mark"],
                "product_price": product["product_price"],
                "discount_price": product["discount_price"],
                "product_image": product["product_image"],
                "product_rating": product["product_rating"],
                "product_description": product["product_description"],
                "categoria_nome": product["categoria_nome"],
                "categoria_pai_nome": product["categoria_pai_nome"],
                "id_categoria": product["id_categoria"]
            }
        return None

    #Show products by category
    def list_products_by_category(id_categoria):
        product = Product.list_products_by_category(id_categoria)
       
        return [{
            "id": product["id_categoria"],
            "nome_categoria": product["nome_categoria"],
            "price": product["id_categoria_pai"],
            "id_categoria": product["id_categoria"],
          
        }]
    

    #Update products
    def submit_rating(self, product_id, rating):
        try:
            Product.update_product_rating(product_id, rating)
            return {"success": True, "message": "Classificação enviada com sucesso!"}
        except Exception as e:
            return {"success": False, "message": str(e)}
        
    #Search for products
    def search_products(self, search_query):
        # Chama o modelo para buscar produtos no banco de dados
        return Product.search_products(search_query)
    #Show slide
    def list_slide(self):
        slide_image = Product.list_slides()
        return [
            {
                "slide_image": slid["slide_image"],
              
            }
            for slid in slide_image
        ]
    
    #Show products by price
    def get_price_ranges():
     return [
        ("Até R$ 199", "0", "199"),
        ("De R$ 200 até R$ 599", "200", "599"),
        ("De R$ 600 até R$ 999", "600", "999"),
        ("De R$ 1000 até R$ 9999", "1000", "9999"),
        ("Acima de R$ 10000", "10000", None)
    ]
    #Show product by price
    def list_by_price(category_id,min_price, max_price):
       category_name, prices = Product.list_products_by_price_range(category_id,min_price, max_price)
       print(prices) 
       return {
        "category_name": category_name,
        "products": [{
            "id": product["id"],
            "name": product["name"],
            "discount_price": product["discount_price"],
            "product_rating": product["product_rating"],
            "price": product["price"],
            "images": product["images"],
        } for product in prices]
    }