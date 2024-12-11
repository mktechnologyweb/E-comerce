import mysql.connector
from controllers.config import DB_CONFIG


class Category:
    @staticmethod
    #Show categories
    def list_categories():
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor(dictionary=True)
        
        cursor.execute("""SELECT 
    id_categoria,
    id_categoria_pai,                    
    nome_categoria 
FROM 
    categorias 
WHERE 
    id_categoria_pai IS NULL;""""")
        categories = cursor.fetchall()

        cursor.close()
        conn.close()
        return categories
    
    #Show categories by id
    def list_products_by_category(category_id):
     try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor(dictionary=True)
       
        
        #Search for products in the category and its subcategories
        cursor.execute("""
             SELECT 
    c.nome_categoria AS "nome_categoria",
    c.id_categoria AS "id_categoria" ,
    s.nome_categoria AS "Nome da Subcategoria",
    j.nome_categoria AS "Nome da Subsbcategoria",
    p.product_id AS "product_id",
    p.product_name AS "product_name",
    p.product_price AS "product_price",
    p.discount_price AS "discount_price",
    p.stock_quantity AS "Quantidade em Estoque",
    p.product_description AS "Descrição do Produto",
    p.product_rating AS "product_rating",
    p.product_image AS "product_image",
    p.id_categoria AS "ID da Categoria"
FROM 
    categorias c
LEFT JOIN 
    categorias s ON s.id_categoria_pai = c.id_categoria
LEFT JOIN 
    categorias j ON j.id_categoria_pai = s.id_categoria
LEFT JOIN 
    product p ON p.id_categoria = j.id_categoria OR p.id_categoria = c.id_categoria
WHERE 
    c.id_categoria = %s;  -- Filtra apenas a categoria Eletrodomésticos
        """, (category_id,))
     

        results = cursor.fetchall()
       
        if results:
            category_name = results[0]['nome_categoria']
            products = [{
                "id": row['product_id'],
                "name": row['product_name'],
                "discount_price": row['discount_price'],
                "product_rating": row['product_rating'],
                "price": row['product_price'],
                "images": row['product_image'],
                "id_categoria": row['id_categoria']
            } for row in results if row['product_id'] is not None]
           
            return category_name, products
            
     finally:
        cursor.close()
        conn.close()

    #Show category sub item by id
    def list_subItem_category(category_id):
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor(dictionary=True)
        
        cursor.execute(""" 
    SELECT 
    id_categoria, nome_categoria 
    
FROM 
    categorias
WHERE 
    id_categoria_pai = %s; """,(category_id,))
        categories = cursor.fetchall()

        cursor.close()
        conn.close()
        return categories
    

    #deletar
    def get_category_names(id_sub_item):#essa
      try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor(dictionary=True)

        # Query to get category and parent category name
        cursor.execute("""
            SELECT 
                c.nome_categoria AS subcategory_name,
                c.id_categoria AS id_1,
                cp.id_categoria AS id_2,
                cp.nome_categoria AS parent_category_name
            FROM 
                categorias c
            LEFT JOIN 
                categorias cp ON c.id_categoria_pai = cp.id_categoria
            WHERE 
                c.id_categoria = %s;
        """, (id_sub_item,))

        result = cursor.fetchall()

      

      finally:
        cursor.close()
        conn.close()

        return result
      

    #Search for products in the subcategory and its subcategories
    def list_products_by_subcategory(subcategory_id):
     try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor(dictionary=True)

        #Search for products in the subcategory and its subcategories
        cursor.execute("""
            SELECT 
                p.product_id,
                p.product_name,
                p.discount_price,
                p.product_rating,
                p.product_price,
                p.product_image,
                p.id_categoria
            FROM 
                product p
            WHERE 
                p.id_categoria IN (
                    SELECT id_categoria 
                    FROM categorias 
                    WHERE id_categoria = %s OR id_categoria_pai = %s
                );
        """, (subcategory_id, subcategory_id))

        products = cursor.fetchall()

     finally:
        cursor.close()
        conn.close()

        return products
     
    #Show products by price
    def category_price_cont(product_price):
     try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor(dictionary=True)

        # Busca os produtos na subcategoria e suas subcategorias
        cursor.execute("""
            SELECT 
    p.product_name, 
    c1.nome_categoria AS categoria,
    c1.id_categoria,
    c1.id_categoria_pai,                                       
    c2.nome_categoria AS categoria_pai,
    COUNT(p.product_price) AS contagem_precos
FROM 
    product p
JOIN 
    categorias c1 ON p.id_categoria = c1.id_categoria
LEFT JOIN 
    categorias c2 ON c1.id_categoria_pai = c2.id_categoria
WHERE 
    p.product_price = %s
GROUP BY 
    p.product_name, c1.nome_categoria, c2.nome_categoria;

                );
        """, (product_price,))

        price = cursor.fetchall()

     finally:
        cursor.close()
        conn.close()

        return price
     

    @staticmethod
    #Show products by category
    def list_products_by_subcategory(id_categoria_pai=None, id_categoria=None):
        try:
            conn = mysql.connector.connect(**DB_CONFIG)
            cursor = conn.cursor(dictionary=True)

            # Check if parent category_id is provided
            if id_categoria_pai is not None:
                cursor.execute("""
                   SELECT 
                        p.product_id,
                        p.product_name,
                        p.discount_price,
                        p.product_rating,
                        p.product_price,
                        p.product_image,
                        p.id_categoria,
                        c2.nome_categoria AS categoria_pai,
                        c3.nome_categoria AS categoria_vo,
                        c2.id_categoria AS id_pai,
                        c3.id_categoria AS id_vo    
                    FROM 
                        product p
                    JOIN 
                        categorias c1 ON p.id_categoria = c1.id_categoria
                    LEFT JOIN 
                        categorias c2 ON c1.id_categoria_pai = c2.id_categoria
                    LEFT JOIN 
                        categorias c3 ON c2.id_categoria_pai = c3.id_categoria
                    WHERE 
                        c1.id_categoria_pai = %s;
                """, (id_categoria_pai,))
                
                result = cursor.fetchall()

            # If there is no parent category_id, search for category_id
            elif id_categoria is not None:
                cursor.execute("""
                    SELECT 
                        p.product_id,
                        p.product_name,
                        p.discount_price,
                        p.product_rating,
                        p.product_price,
                        p.product_image,
                        p.id_categoria, 
                        c1.id_categoria AS id_categoria, 
                        c2.id_categoria AS id_pai,
                        c3.id_categoria AS id_vo,
                        c1.nome_categoria AS categoria, 
                        c2.nome_categoria AS categoria_pai,
                        c3.nome_categoria AS categoria_vo
                    FROM 
                        product p
                    JOIN 
                        categorias c1 ON p.id_categoria = c1.id_categoria
                    LEFT JOIN 
                        categorias c2 ON c1.id_categoria_pai = c2.id_categoria
                    LEFT JOIN 
                        categorias c3 ON c2.id_categoria_pai = c3.id_categoria
                    WHERE 
                        c1.id_categoria = %s;
                """, (id_categoria,))
                
                result = cursor.fetchall()

            else:
                result = []

        except mysql.connector.Error as err:
            print(f"Error: {err}")
            result = []

        finally:
            cursor.close()
            conn.close()

        return result
    
    #Show products by sub category
    def list_products_by_subcategory_subcategory(id_categoria):
        try:
            conn = mysql.connector.connect(**DB_CONFIG)
            cursor = conn.cursor(dictionary=True)

           # If parent_category_id is provided, fetches products from the subcategory and its supercategories

# If category_id is provided, fetches only products from the specific category "2-Door Refrigerator"
          
            cursor.execute("""
                    SELECT 
                        p.product_id,
                        p.product_name,
                        p.discount_price,
                        p.product_rating,
                        p.product_price,
                        p.product_image,
                        p.id_categoria, 
                        c1.id_categoria AS id_categoria, 
                        c2.id_categoria AS id_pai,
                        c3.id_categoria AS id_vo,
                        c1.nome_categoria AS categoria, 
                        c2.nome_categoria AS categoria_pai,
                        c3.nome_categoria AS categoria_vo
                    FROM 
                        product p
                    JOIN 
                        categorias c1 ON p.id_categoria = c1.id_categoria
                    LEFT JOIN 
                        categorias c2 ON c1.id_categoria_pai = c2.id_categoria
                    LEFT JOIN 
                        categorias c3 ON c2.id_categoria_pai = c3.id_categoria
                    WHERE 
                        c1.id_categoria = %s;  -- Filtra pela categoria específica "Geladeira 2 Portas"
                """, (id_categoria,))
                
            result = cursor.fetchall()

            

        except mysql.connector.Error as err:
            print(f"Error: {err}")
            result = []

        finally:
            cursor.close()
            conn.close()

        return result