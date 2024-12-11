import mysql.connector
from controllers.config import DB_CONFIG

class Product:
    @staticmethod
    #Show products
    def list_products():
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor(dictionary=True)
        
        cursor.execute("SELECT product_id, product_name, product_price, discount_price, product_image, product_rating,id_categoria FROM product")
        products = cursor.fetchall()

        cursor.close()
        conn.close()
        return products
    
    @staticmethod   
    #Show products by id
    def get_product_by_id(product_id):
     try:
        # Conectar ao banco de dados
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor(dictionary=True)  # Retornar como dicionário
        
        # Consulta SQL para buscar produto pelo ID
        query = """SELECT 
            p.product_id,
            p.product_name,
            p.product_mark,
            p.product_price,
            p.discount_price,
            p.stock_quantity,
            p.product_description,
            p.product_rating,
            p.product_image,
            p.id_categoria,
            c.nome_categoria AS categoria_nome,
            cc.nome_categoria AS categoria_pai_nome
        FROM 
            product p
        LEFT JOIN 
            categorias c ON p.id_categoria = c.id_categoria
        LEFT JOIN 
            categorias cc ON c.id_categoria_pai = cc.id_categoria
        WHERE 
            p.product_id = %s"""
        
       
        cursor.execute(query, (product_id,))
        
    
        product = cursor.fetchone()

     except mysql.connector.Error as err:
        print(f"Erro ao buscar o produto: {err}")
        return None

     finally:
       
        cursor.close()
        conn.close()
     # Returns the product or None if not found
     return product  
    @staticmethod
    #Show products by category
    def list_products_by_category(id_categoria):
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor(dictionary=True)

        query = """
         WITH RECURSIVE categoria_hierarquia AS (
                SELECT 
                    id_categoria,
                    nome_categoria,
                    id_categoria_pai
                FROM 
                    categorias
                WHERE 
                    id_categoria = %s

                UNION ALL

                SELECT 
                    c.id_categoria,
                    c.nome_categoria,
                    c.id_categoria_pai
                FROM 
                    categorias c
                INNER JOIN 
                    categoria_hierarquia ch ON c.id_categoria = ch.id_categoria_pai
            )
            SELECT * FROM categoria_hierarquia;
        """
        cursor.execute(query, (id_categoria,))
        products = cursor.fetchall()

        cursor.close()
        conn.close()
        return products
    
    #Update products
    def update_product_rating(product_id, rating):
     conn = mysql.connector.connect(**DB_CONFIG)
     cursor = conn.cursor()

    
     query = "UPDATE product SET product_rating = %s WHERE product_id = %s"
     cursor.execute(query, (rating, product_id))

     conn.commit()

     cursor.close()
     conn.close()


    #Search for products
    def search_products(search_query):
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor(dictionary=True)
        
        #SQL query to search for products matching the search term (using LIKE)
        query = """
            SELECT p.product_id, p.product_name,p.product_mark, p.product_price, p.product_image, 
           p.discount_price, p.product_rating, c.nome_categoria
          FROM product p
            INNER JOIN categorias c ON p.id_categoria = c.id_categoria
            WHERE product_name LIKE %s OR product_description LIKE %s
        """
        like_pattern = f"%{search_query}%"
        cursor.execute(query, (like_pattern, like_pattern))
        
        results = cursor.fetchall()
        cursor.close()
        conn.close()
        
        return results
    
    #Show slide
    @staticmethod
    def list_slides():
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor(dictionary=True)
        
        cursor.execute("SELECT slide_image FROM promotional_slide")
        slide_image = cursor.fetchall()

        cursor.close()
        conn.close()
        return slide_image
    

    #Show products by price
    def list_products_by_price_range(category_id, min_price, max_price):
     try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor(dictionary=True)

        # Busca produtos dentro da faixa de preço
        if max_price is None:
            cursor.execute("""
                           SELECT 
    c.nome_categoria AS "nome_categoria",
    c.id_categoria AS "ID da Categoria",
    c.id_categoria_pai AS "ID da Categoria Pai",
    s.nome_categoria AS "Nome da Subcategoria",
    j.nome_categoria AS "Nome da Subsubcategoria",
    p.product_id AS "product_id",
    p.product_name AS "product_name",
    p.product_price AS "product_price",
    p.discount_price AS "discount_price",
    p.stock_quantity AS "Quantidade em Estoque",
    p.product_description AS "Descrição do Produto",
    p.product_rating AS "product_rating",
    p.product_image AS "product_image"
FROM 
    categorias c
LEFT JOIN 
    categorias s ON s.id_categoria_pai = c.id_categoria
LEFT JOIN 
    categorias j ON j.id_categoria_pai = s.id_categoria
LEFT JOIN 
    product p ON p.id_categoria = j.id_categoria OR p.id_categoria = c.id_categoria
WHERE 
    c.id_categoria = %s  -- Filtra pela categoria correta
AND 
    p.product_price >= %s;
            """, (category_id, min_price))
        else:
            cursor.execute("""
               SELECT 
    c.nome_categoria AS "nome_categoria",
    c.id_categoria AS "ID da Categoria",
    c.id_categoria_pai AS "ID da Categoria Pai",
    s.nome_categoria AS "Nome da Subcategoria",
    j.nome_categoria AS "Nome da Subsubcategoria",
    p.product_id AS "product_id",
    p.product_name AS "product_name",
    p.product_price AS "product_price",
    p.discount_price AS "discount_price",
    p.stock_quantity AS "Quantidade em Estoque",
    p.product_description AS "Descrição do Produto",
    p.product_rating AS "product_rating",
    p.product_image AS "product_image"
FROM 
    categorias c
LEFT JOIN 
    categorias s ON s.id_categoria_pai = c.id_categoria
LEFT JOIN 
    categorias j ON j.id_categoria_pai = s.id_categoria
LEFT JOIN 
    product p ON p.id_categoria = j.id_categoria OR p.id_categoria = c.id_categoria
WHERE 
    c.id_categoria = %s  -- Filtra pela categoria correta
AND 
    p.product_price  BETWEEN  %s AND  %s
            """, (category_id, min_price, max_price))
         
        products = cursor.fetchall()
       
        if products:
            category_name = products[0]['nome_categoria']
            products = [{
                "id": row['product_id'],
                "name": row['product_name'],
                "discount_price": row['discount_price'],
                "product_rating": row['product_rating'],
                "price": row['product_price'],
                "images": row['product_image']
            } for row in products if row['product_id'] is not None]

     finally:
        cursor.close()
        conn.close()

        return category_name, products 
     

  