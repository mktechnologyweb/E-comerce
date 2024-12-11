from http.cookies import SimpleCookie
from http.server import SimpleHTTPRequestHandler, HTTPServer
import json
import os
import logging
import mysql.connector
from urllib.parse import urlparse, parse_qs
from controllers.adress_controller import AddressController
from controllers.category_controller import CategoryController
from controllers.favorites_controller import FavoritesController
from controllers.order_controller import OderController
from controllers.product_controller import ProductController
from controllers.pyment_controller import PymentController
from controllers.user_controller import UserController
from controllers.cart_controller import CartController
from controllers.config import DB_CONFIG



#Check logged in users with open order

def verify_user_owns_order(customer_id, cart_id):
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor()

    query = """
       SELECT c.customer_id
       FROM payments p
       INNER JOIN orders o ON p.order_id = o.cart_id
       INNER JOIN cart c ON o.cart_id = c.cart_id
       WHERE c.cart_id = %s AND c.customer_id = %s;"""
    cursor.execute(query, (cart_id, customer_id))
    result = cursor.fetchone()

    if result:
        print(f"Usuário {customer_id} é o dono do cart_id {cart_id}.")
    else:
        print(f"Nenhum resultado encontrado para o cart_id {cart_id} e customer_id {customer_id}.")

    return result is not None

#Check logged in users with registered address
def verify_user_owns_address(user_id, address_id):
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor()

    query = """
        SELECT a.user_id
        FROM address a
        INNER JOIN customer c ON a.user_id = c.customer_id
        WHERE a.address_id = %s AND a.user_id = %s;
    """
    cursor.execute(query, (address_id, user_id))
    result = cursor.fetchone()

    if result:
        print(f"Usuário {user_id} é o dono do endereço com ID {address_id}.")
    else:
        print(f"Nenhum resultado encontrado para address_id {address_id} e user_id {user_id}.")

    return result is not None


class MyHandler(SimpleHTTPRequestHandler):

#Receive the javascript function to load the page without changing the page
    def ajax(self):
      
        return self.headers.get('X-Requested-With') == 'XMLHttpRequest'
    
    
    #Sends an HTML response to the client
    def _send_html_response(self, html_content):
       
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        
        
        self.wfile.write(html_content.encode('utf-8'))
    
    #Get cookies from header
    def get_user_id_from_cookies(self):
      
        
        cookie_header = self.headers.get('Cookie')
        
        if cookie_header:
            #Parse cookies
            cookie = SimpleCookie(cookie_header)
            
            #Checks if the 'user_id' cookie exists
            if 'user_id' in cookie:
                return cookie['user_id'].value
        return None 
    

    #Extracts the value of a parameter from the URL query string
    def get_query_param(self, param_name):
       
        from urllib.parse import urlparse, parse_qs
        #Parse the full URL 
        query_components = parse_qs(urlparse(self.path).query)
        #Returns the value of the parameter, if it exists
        return query_components.get(param_name, [None])[0]



    # Checks if the user is logged in based on the 'user_id' cookie
    def check_user_login_status(self):
       
        user_id = self.get_user_id_from_cookies()
        
        return user_id is not None


    #Initializes the logged_in_user attribute
    def __init__(self, *args, **kwargs):
        self.logged_in_user = None  #
        super().__init__(*args, directory='views', **kwargs)


    #Overrides the end_headers method to add CORS (Cross-Origin Resource Sharing) support.
    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        super().end_headers()

   


    def do_GET(self):
    # Check if it is a static file (CSS or JS)
     if self.path.startswith('/css/') or self.path.startswith('/js/'):
        return super().do_GET()

    # Parses the URL path and parameters
     parsed_path = urlparse(self.path)
     query_params = parse_qs(parsed_path.query)

    # Check if the path is to the login page
     if parsed_path.path == '/login_user':
        redirect_page = query_params.get('redirect', [None])[0]
        #Pass redirection as argument
        self.handle_login_user(redirect_page)
        print(f"Requisição recebida: {self.path}")
    # Other routes
     elif parsed_path.path == "/my_account":
         user_is_logged_in = self.check_user_login_status()
         if user_is_logged_in == True:
          self.handle_success_mycount()
         else:
           self.handle_login_user()
     elif parsed_path.path == "/payment":
        ajax = self.ajax()
        user_is_logged_in = self.check_user_login_status()
        if ajax == True:
         if user_is_logged_in == True:
          self.handle_payment_my_account()
         else:
           self.handle_login_user()
        else:
           self.handle_success_mycount()
     elif parsed_path.path == "/address":
        ajax = self.ajax()
        user_is_logged_in = self.check_user_login_status()
        if ajax == True:
         if user_is_logged_in == True:
          self.handle_accounty_addrress()
         else:
           self.handle_login_user()
        else:
           self.handle_success_mycount()
     elif parsed_path.path == "/produtos":
        self.handle_product_list()
     elif parsed_path.path == "/":
        self.handle_index()

     elif parsed_path.path.startswith("/detalhes"):
        self.handle_details_product()


     elif parsed_path.path == "/cart":
        self.handle_cart()
    
     elif parsed_path.path == "/favorits_my":

        ajax = self.ajax()
        user_is_logged_in = self.check_user_login_status()
        if ajax == True:
         if user_is_logged_in == True:
          self.list_favorits_my()
         else:
          self.handle_login_user()
        else:
           self.handle_success_mycount()
     elif parsed_path.path == "/preferences_page":

        ajax = self.ajax()
        user_is_logged_in = self.check_user_login_status()
        if ajax == True:
         if user_is_logged_in == True:
          self.account_preferences_page()
         else:
          self.handle_login_user()
        else:
           self.handle_success_mycount()


     elif parsed_path.path == "/checkout":
        user_is_logged_in = self.check_user_login_status()
        if user_is_logged_in == True:
         self.handle_checkout_cart()
        else:
         self.handle_login_user()
     elif parsed_path.path == "/cadastro":
        self.handle_cadastro()
    
     elif parsed_path.path == "/logout":
         self.handle_logout()
     
     elif parsed_path.path == "/categoria":
        category_id = query_params.get("id", [None])[0]
        if category_id:
            self.handle_category_page(category_id)

     elif parsed_path.path == "/category_pryce":
        category_id = query_params.get("id", [None])[0]
        min_price = query_params.get("min_price", [None])[0]
        max_price = query_params.get("max_price", [None])[0]
        if category_id and min_price and max_price:
            self.category_price_list(category_id,min_price,max_price)

     elif parsed_path.path == "/product_pyce_filter":
        id_categoria_pai = query_params.get("id_categoria_pai", [None])[0]
        id_categoria = query_params.get("id_categoria", [None])[0]
        
        if id_categoria_pai or id_categoria:
            
            self.category_price_filter(id_categoria_pai,id_categoria)

     elif parsed_path.path == "/product_filter_category":
        
        id_categoria = query_params.get("id_categoria", [None])[0]
        
        if id_categoria:
            
            self.category_price_filter_category(id_categoria)

     elif parsed_path.path == "/sub_item":
        id_sub_item = query_params.get("id_sub_item", [None])[0]
        if id_sub_item:
            self.handle_sub_item_page(id_sub_item)

     elif parsed_path.path == "/subitem":
        id = query_params.get("id", [None])[0]
        if id:
            self.handle_product_page(id)

     elif self.path.startswith("/search_products"):
        query_components = parse_qs(urlparse(self.path).query)
        search_query = query_components.get("search", [None])[0]
        if search_query:
            self.handle_search_products(search_query)
    
        else:
            self.send_response(400)
            self.end_headers()
            self.wfile.write(b"Erro: Termo de pesquisa e necessario.")
     elif parsed_path.path == "/check_login_status":
        self.handle_checkout()



    def do_POST(self):
       parsed_path = urlparse(self.path)
       query_params = parse_qs(parsed_path.query)
       if self.path == "/register":
        self.handle_register()
       #Check if the route is for login 
       elif parsed_path.path == "/login": 
        self.handle_login()
        print(f"Requisição recebida: {self.path}")
       elif self.path == "/save_cart":
        self.handle_save()
       elif self.path == "/save_favorites":
        self.handle_save_favorites()
       elif self.path == "/save_address":
        self.handle_save_address()
       elif self.path == "/process_payment":
        self.handle_payment()
       elif parsed_path.path == "/save_orders":
        self.handle_save_orders()
       elif parsed_path.path == "/updadte_payment":
        self.updadte_payment()
       elif parsed_path.path == "/updadte_preferences":
        self.account_preferences_page_update()
       elif parsed_path.path == "/submit_rating":
        self.handle_submit_rating()
       elif self.path == "/delete_fav":
             self.delet_favorits()

       elif self.path == "/delete_cart":
             self.delet_cart()
       else:
        self.handle_404()

    #Renders HTML template with header and footer
    def render_template(self, title):
        user_is_logged_in = self.check_user_login_status()
        user_is_logged_in_str = '/my_account' if user_is_logged_in else '/login_user' 
        user_is_logged_in_text = 'Minha Conta' if user_is_logged_in else 'Entre ou cadastre-se' 
       
        base_template = f"""
        <!DOCTYPE html>
        <html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <link rel="stylesheet" href="/css/styles.css">
   
    <link rel="stylesheet" href="/css/category.css">
    <link rel="stylesheet" href="/css/details.css">
    
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">
    
    <!-- Slider de Produto -->
      
    
</head>
<body>
    <div class="nav">
        <div class="logo">
            <a href="/">Logo</a>
          
            </div>
           
            <div class="search">
              <form action="/search_products" method="GET"> <!-- Envia o valor de 'search' -->
                  <input type="text" placeholder="O que você tá procurando?" name="search" required>
                  <button type="submit"><i class="fa fa-search"></i></button> 
              </form>
          </div>
           <div class="user-icon">
          <i class="fa fa-user"></i>
          <a href="{ user_is_logged_in_str }">
          <p class="t"> { user_is_logged_in_text }</p>
         </a>
        </div>
      </a>
        <div class="heart-icon">
        <a  href="/favorits_my"><i class="fa  fa-heart"></i></a>
        </div>
        <div class="cart">
        <a href="/cart"><i class="fa fa-cart-plus"></i></a>
        </div>
        <span id="cart-count" class="cart-count" style="color: red;">0</span> 
     </div>
        """
        
        return base_template
       

    #check if the user has an order
    def verify_user_owns_order_item(self,customer_id, order_id):
      conn = mysql.connector.connect(**DB_CONFIG)
      cursor = conn.cursor()

      query = """
        SELECT oi.order_id
        FROM orders o
        INNER JOIN order_item oi ON o.order_id = oi.order_id
        WHERE o.order_id = %s AND o.customer_id = %s;
    """
      cursor.execute(query, (order_id, customer_id))
      result = cursor.fetchone()

      cursor.close()
      conn.close()

      return result is not None


    #Checks if the logged in user is the owner of the favorite item
    def verify_user_owns_favorite(self, user_id, fav_id):
      
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()

        query = """
           SELECT f.id_fav
           FROM favorites f
           INNER JOIN customer c ON f.id_user = c.customer_id
           WHERE f.id_fav = %s AND f.id_user = %s;
           """
        cursor.execute(query, (fav_id, user_id))
        result = cursor.fetchone()

        cursor.close()
        conn.close()

        return result is not None

 

    #Check if the user is logged in
    def handle_checkout(self):
     user_id = self.get_user_id_from_cookies()
   
     if user_id is None:
        # Returns a JSON response indicating that the user is not logged in.
        self.send_response(401)  #Code 401 for unauthorized
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps({'logged_in': False}).encode())
     else:
        #the user is logged in
        self.send_response(200)  #Code 200 for success
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps({'logged_in': True, 'user_id': user_id}).encode())

      
      
    #Save to cart
    def handle_save(self):
     content_length = int(self.headers['Content-Length'])
     post_data = self.rfile.read(content_length)
     data = json.loads(post_data.decode('utf-8'))
    
     cart_items = data.get('cart', [])
     user_id = self.get_user_id_from_cookies()
     cart_controller = CartController()
     cart_controller.save_cart(user_id, cart_items)
    
    #Redirects after saving cart
     self.send_response(302)

     #Redirects to a success or summary page
     self.send_header('Location', '/checkout')  
     self.end_headers()



    #Save to Favorites
    def handle_save_favorites(self):
     content_length = int(self.headers['Content-Length'])
     post_data = self.rfile.read(content_length)
     data = json.loads(post_data.decode('utf-8'))
     user_id = self.get_user_id_from_cookies()
     if user_id == None:
        print("Precisa logar")
     else:
      favorites = data.get('favorites', [])
     
      favorites_controller = FavoritesController
      favorites_controller.save_cart_favorites(favorites,user_id)
    
     self.send_response(302)
     self.send_header('Location', '/')
     self.end_headers()



    #Registration page
    def handle_register(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        data = parse_qs(post_data.decode('utf-8'))

        first_name = data.get('first_name', [None])[0]
        last_name = data.get('last_name', [None])[0]
        email = data.get('email', [None])[0]
        password = data.get('password', [None])[0]

        user_controller = UserController()
        user_controller.register_user(first_name,last_name, email, password)

        self.send_response(302)
        self.send_header('Location', '/my_account') 
        self.end_headers()

    #Success page
    def handle_success(self):
     cookie_header = self.headers.get('Cookie')
    
      
     if cookie_header:
        cookies = dict(x.strip().split('=') for x in cookie_header.split(';'))
        user_id = cookies.get('user_id')
     else:
       user_id = None

     if not user_id:
        self.send_response(403)  # Acesso proibido
        self.end_headers()
        self.wfile.write(b'Acesso proibido. Voce precisa estar logado.')
        return
    
     user_controller = UserController()
     user = user_controller.get_user_by_id(user_id)  # Busca o usuário pelo ID
    
     if user:
        html_content = self._render_template("customer/my_account", {})
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(html_content.encode('utf-8'))
     else:
        self.send_response(403)  # Acesso proibido
        self.end_headers()
        self.wfile.write(b'Acesso proibido. Voce precisa estar logado.')
   

    #Login function
    def handle_login(self):
        logging.info(f"Received request: {self.path}")
        parsed_url = urlparse(self.path)
        query = parsed_url.query
        logging.info(f"Query parameters: {query}")
    
        redirect_page = parse_qs(query).get('redirect', [None])[0]
        logging.info(f"Redirect page: {redirect_page}")
        parsed_url = urlparse(self.path)
        query = parsed_url.query
        redirect_page = parse_qs(query).get('redirect', [None])[0]
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        data = parse_qs(post_data.decode('utf-8'))
        email = data.get('email', [None])[0]
        password = data.get('password', [None])[0]
        user_controller = UserController()
        login = user_controller.login(email, password)
        if login["status"] == "error":
            if redirect_page == 'cart':
             error_message = "Credenciais invalidas. Tente novamente."
             self.send_response(302)
             self.send_header('Set-Cookie', f'error_message={error_message}; Path=/login_user;')
             self.send_header('Location', '/login_user?redirect=cart')
             self.end_headers()
            else:
              error_message = "Credenciais invalidas. Tente novamente."
              
              self.send_response(302)
              self.send_header('Set-Cookie', f'error_message={error_message}; Path=/login_user;')
              self.send_header('Location', '/login_user')
              self.end_headers()  
        if login["status"] == "success":
          user = login
          if user:
            #Redirects based on parameter
            if redirect_page == 'cart':
                print("agora é", redirect_page)
                self.send_response(302)  #Sends HTTP status 302 (redirect) 
                self.send_header('Location', '/cart')
            else:
                self.send_response(302)
                #Redirects to user account  
                self.send_header('Location', '/my_account')  
            
            #Sets the user cookie 
            self.send_header('Set-Cookie', f'user_id={user["customer_id"]}; Path=/; HttpOnly')
            self.end_headers()
        else:
            # Login failure case
            self.send_response(401)
            self.end_headers()
    

    #Page after product search
    def handle_search_products(self, search_query):
    
     product_controller = ProductController()
     search_results = product_controller.search_products(search_query)

    
     with open('views/search_results.html', 'r') as file:
        content = file.read()
    
     if  search_results == []:
      title = search_query
      full_page = self.render_template(title)
      product_list_html = f"""
        {full_page}
         <h1> Não temos este produto no momento</h1>
        <a href="/">Voltar para a Página Inicial</a>
        """
     else:
      product_list_html = ""
      for product in search_results:
       
        title = search_query
        full_page = self.render_template(title)
        product_list_html += f"""
        
         {full_page}
         <h1>Você buscou por: {search_query}</h1>
         <div class="product">
                <a href="/detalhes?id={product['product_id']}">
                    <img src="{product['product_image']}" alt="{product['product_name']}">
                </a>
                <h3>{product['product_name']}</h3>
                <p>Preço: R$ {product['product_price']:.2f}</p>
                    <p>Preço com Desconto: <strong>R$ {product['discount_price']:.2f}</strong></p>
                    <p>Classificação: <span style="color: gold;"> {'★' * product['product_rating']}</span> <span>{'☆' * (5 - product['product_rating'])}</span></p>
            </div>
        """
     
     content = content.replace("<!-- PRODUCT_RESULTS_PLACEHOLDER -->", product_list_html)
    
     self.send_response(200)
     self.send_header('Content-type', 'text/html')
     self.end_headers()
     self.wfile.write(content.encode('utf-8'))


    #Product details page
    def handle_details_product(self):
     try:
        query = self.path.split("?")[1]
        product_id = int(query.split("=")[1])

        controller = ProductController()
        product = controller.get_product_by_id(product_id)
        user_is_logged_in = self.check_user_login_status()
        
        
        if user_is_logged_in == True:
         vaforits = "".join(
           f"""
            <button onclick="addToFavoritesss('{product['product_id']}', '{product['product_name']}', {product['product_price']}, '{product['product_image']}')" class="favorite-button">
                                        <i class="fa fa-heart" id="favoriteIcon"></i>
                                    </button>
          """
        )
         
        else:
             vaforits = "".join(
           f"""
            <button onclick="alert('Você Precisa estar logado!')" class="favorite-button">
                                        <i class="fa fa-heart" id="favoriteIcon"></i>
                                    </button>
          """
        )
        if product:
            # Get Product Category Hierarchy
            id_categoria = product["id_categoria"]
            hierarquia_categorias = CategoryController.category_category_category(id_categoria)
            
            # Building the breadcrumb
          
            breadcrumb = "".join(f"""
            <span>
                <a href="/categoria?id={product["id_vo"]}">{product['categoria_vo']}</a>
                <span class="angle fa fa-angle-right" aria-hidden="true"></span>
            </span>
            <span>
                <a href="/sub_item?id_sub_item={product["id_pai"]}">{product['categoria_pai']}</a>
                <span class="angle fa fa-angle-right" aria-hidden="true"></span>
            </span>
            <span>
                <a href="/product_filter_category?id_categoria={product["id_categoria"]}">{product['categoria']}</a>
                <span class="angle fa fa-angle-right" aria-hidden="true"></span>
            </span>
        """ for product in hierarquia_categorias)
            title = product['product_name']
            full_page = self.render_template(title)
            #Product Detail Page HTML
            product_html = f"""
              {full_page}
                
                <main>
                    <div class="links">
                        <span>{breadcrumb}</span>
                    </div>
                 <div class="details_product">
                    <h1>Informações do produto</h1>
                 
                        <div class="conteiner_vertical">
                            <p>Código do produto: {product['product_id']}</p>
                            
                            <hr class="vertical-hr">
                            <p>Mais produtos da mesma marca:<span style="color:#00c2ff;"> {product['product_mark']}</span> </p>
                        </div>
                        </main>
                         <hr class="hr_product">
                        <div class="product-container">
                            <div class="product-slider">
                                <div class="main-image image-zoom-container">
                                    <img id="currentImage" src="{product['product_image']}" alt="{product['product_name']}">
                                    {vaforits}
                                </div>
                                  <hr class="hr_thumnails">
                         <div class="thumbnails">
                         <img src="{product['product_image']}"  alt="Imagem 1" onmouseover ="changeImage('{product['product_image']}')">
                         <img src="{product['product_image']}"  alt="Imagem 2" onmouseover ="changeImage('{product['product_image']}')">
                         <img src="{product['product_image']}"  alt="Imagem 3" onmouseover ="changeImage('{product['product_image']}')">
                         <img src="{product['product_image']}"  alt="Imagem 4" onmouseover ="changeImage('{product['product_image']}')">
                         </div>
                          </div>
                        <!-- Seção de Preço -->
                         <hr class="vertical-hr-procuct">
                         <div class="price">
                                  <p class="sold"><span>Vendido e entregue por <a href="/">Loja</a></span>
                                </p>
                                 <div class="stars conteiner_vertical">
                                <span style="color: gold;"> {'★' * product['product_rating']}</span> <span>{'☆' * (5 - product['product_rating'])}</span>
                                 <hr class="vertical-hr">
                                 <p style="color: #000;">Avaliações</p>
                                <hr class="vertical-hr">
                                 </div>
                                 <div>
                                 <span class="discount_card"><b>R$ {product['discount_price']:.3f}</b> </span>
                                 <span>em até </span>  
                                 <span>10x de</span>
                                <span class="discount_card"> <b>R$ {product['discount_price'] / 10}</b> </span>
                                <span>sem juros no cartão de crédito.</span>
                                </p>
                                </div>
                                <hr class="hr_payment">
                                <div class="display">      
                                <p><span>R$ {product['product_price']:.3f}</span>
                                <button class="color_button" onclick="addToCart('{product['product_id']}', '{product['product_name']}', {product['discount_price']}, '{product['product_image']}')">Comprar</button></p>
                            </div>
                        </div>
                    </div>
                </main>
                <div class="description">
                {product['product_description']}
                </div>
                <script src="/js/cart.js"></script>
                <script src="/js/detalhes_product.js"></script>
            </body>
            </html>
            """
           
           
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(product_html.encode('utf-8'))
        else:
             self.handle_404()
     except Exception as e:
        self.send_response(500)
        self.end_headers()
        self.wfile.write(f"Erro ao buscar detalhes do produto: {str(e)}".encode('utf-8'))
    
    
    #Logged in customer account
    def handle_success_mycount(self):
    # Retrieves the ID of the logged in user
     customer_id = self.get_user_id_from_cookies()
     name_controller = UserController()
     name = name_controller.get_name(customer_id)
     names = name["first_name"] 
     
    # Initializes the order controller (OrderController)
     order_controller = OderController
     
    
    # Retrieves the logged in user's order list
     lista = order_controller.list_my()
    
    # Initializes the variable to store the HTML of all requests
     html_content_final = ""

     for pedido in lista:
        order_id = pedido['order_id']
        
           
        # Verifies if the order belongs to the logged in user using the verify_user_owns_order_item function
        if self.verify_user_owns_order_item(customer_id, order_id):
            
            # Builds the HTML for each request
             html_content_final += f"""
            <div class="container-section">
                <div class="card-order-column">
                   
                    <h5>Número do pedido:</h5>
                    <p>{pedido['order_id']}</p>
                </div>
                <div class="card-order-column">
                    <h5>Data de envio:</h5>
                    <p>{pedido['shipping_date']}</p>
                </div>
                <div class="card-order-column">
                    <h5>Status:</h5>
                    <p>{pedido['order_status']}</p>
                </div>
                <div class="card-order-column">
                    <h5>Valor do pedido:</h5>
                    <p>R$ {pedido['total_amount']}</p>
                </div>
            </div>
            <form action="/submit_rating" method="POST">
            <label for="rating">Avalie este produto (1 a 5 estrelas):</label>
            <input type="number" id="rating" name="rating" min="1" max="5" required>
            <input type="hidden" name="product_id" value="{ pedido['id'] }">
            <button type="submit">Enviar Avaliação</button>
           </form>
            """
        else:
            # If the request does not belong to the user, it is ignored.
            continue

    # Renders the customer account template with the order list
     html_content_final = self._render_template("customer/my_account", {"name": names, "lista": html_content_final})

    # Checks if the HTML was generated successfully and sends the response
     if html_content_final:
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(html_content_final.encode('utf-8'))
     else:
        # Handles 404 error if something goes wrong
        self.handle_404()


    #Logged in customer preferences
    def account_preferences_page(self):
        customer_id = self.get_user_id_from_cookies()
        user = UserController.get_user_by_id(customer_id)
       
        for u in user:
         content = f"""

             <h2 class="info">Informações Pessoais</h2>
            <form action="/updadte_preferences" method="POST"class="form">
                <label for="nome">Nome</label>
                <input type="text" id="full_name" name="name" value="{u["first_name"]}" required>

                <label for="Sobre Nome">Sobre Nome</label>
                <input type="text" id="full_name" name="last_name" value="{u["last_name"]}" required>
                
                <label for="email">E-mail:</label>
                <input type="email" id="email" name="email" value="{u["email"]}" required>
                
               
                
                <button type="submit">Salvar Alterações</button>
            </form>

        """
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(content.encode('utf-8'))
    

    #Updating registered data
    def account_preferences_page_update(self):
       user_id = self.get_user_id_from_cookies()
       content_length = int(self.headers['Content-Length'])
       post_data = self.rfile.read(content_length)
       data = parse_qs(post_data.decode('utf-8'))

       name = data.get('name', [None])[0]         
       last_name = data.get('last_name', [None])[0]  
       email = data.get('email', [None])[0]
       UserController.update_user(name,last_name,email,user_id)
       self.send_response(302)
       self.send_header('Location', 'my_account')
       self.end_headers() 



    #Cart Page
    def handle_cart(self):  
    # Checks if the user is logged in
     user_is_logged_in = self.check_user_login_status()
     user_is_logged_in_str = '/my_account' if user_is_logged_in else '/login_user'
     user_is_logged_in_text = 'Minha Conta' if user_is_logged_in else 'Entre ou cadastre-se'
     user_id = self.get_user_id_from_cookies()

    # Instantiate the address controller
     address_controller = AddressController
     address_list = address_controller.list_address()  # Obtém os endereços do usuário

    

    # Initializes basic HTML content
     html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Cart</title>
        <link rel="stylesheet" href="/css/styles.css">
        <link rel="stylesheet" href="/css/cart.css">
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">
    </head>
    <body>
        <div class="nav">
            <div class="logo">
                <a href="/">Logo</a>
            </div>
            <div class="service">
                <a href="{user_is_logged_in_str}" class="user-icon">
                    <i class="fa fa-user" style="color:#ffff; font-size: 46px; padding: 2px;"></i>
                    {user_is_logged_in_text}
                </a>
                <i class="icons fa fa-phone" aria-hidden="true"> <a href="">Central de atendimento</a></i>
                <i class="icons fa fa-archive" aria-hidden="true"> <a href="">Meus pedidos</a></i>
                <i class="icons fa fa-lock" aria-hidden="true"> <a href="">Ambiente 100% seguro</a></i>
            </div>
        </div>
        <div class="my_cart">
            <h1>Meu Carrinho</h1>
            <div id="cartItems"></div>
            <hr class="hr_cart">
    """

    # Checks if the user is logged in and has registered addresses
     if user_is_logged_in:
        if address_list:  # If there are registered addresses
            # Search for the first address the user has
            address_found = False
            for address in address_list:
                address_id = address['address_id']
                if verify_user_owns_address(user_id, address_id):
                    html_content += f"""
                    <div id="address_form">
                        <h2>Endereço de Entrega</h2>
                        <form action="/save_address" method="POST">
                            
                            <label for="street">Endereço (Linha 1):</label>
                            <input type="text" id="street" name="street" placeholder="Rua, avenida, etc." 
                                   value="{address['street']}" required>
                            <label for="number">Número (Linha 2):</label>
                            <input type="text" id="number" name="number" placeholder="Número" 
                                   value="{address['number']}" required>
                            <label for="neighborhood">Bairro:</label>
                            <input type="text" id="neighborhood" name="neighborhood" 
                                   value="{address['neighborhood']}" required>
                            <label for="city">Cidade:</label>
                            <input type="text" id="city" name="city" 
                                   value="{address['city']}" required>
                            <label for="state">Estado:</label>
                            <input type="text" id="state" name="state" 
                                   value="{address['state']}" required>
                            <label for="zipcode">CEP:</label>
                            <input type="text" id="zip_code" name="zip_code" 
                                   value="{address['zip_code']}" required>
                            <label for="complement">Telefone:</label>
                            <input type="tel" id="complement" name="complement" placeholder="Complemento" 
                                   value="{address['complement']}" required>
                             <button style="color: aqua;"  onclick="checkUserLoginStatus()">Continuar</button>
                        </form>
                    </div>
                    
                    """
                    address_found = True
                    break  # Exit the loop after finding the first address
            
            if not address_found:
                #If you did not find a valid address, show the registration form
                html_content += f"""
                <div id="address_form">
                    <h2>Cadastrar Endereço de Entrega</h2>
                    <form action="/save_address" method="POST">
                        
                        <label for="street">Endereço (Linha 1):</label>
                        <input type="text" id="street" name="street" placeholder="Rua, avenida, etc." required>
                        <label for="number">Número (Linha 2):</label>
                        <input type="text" id="number" name="number" placeholder="Número" required>
                        <label for="neighborhood">Bairro:</label>
                        <input type="text" id="neighborhood" name="neighborhood" required>
                        <label for="city">Cidade:</label>
                        <input type="text" id="city" name="city" required>
                        <label for="state">Estado:</label>
                        <input type="text" id="state" name="state" required>
                        <label for="zipcode">CEP:</label>
                        <input type="text" id="zip_code" name="zip_code" required>
                        <label for="complement">Telefone:</label>
                        <input type="tel" id="complement" name="complement" placeholder="Complemento" required>
                         <button style="color: aqua;"  onclick="checkUserLoginStatus()">Cadastrar</button>
                    </form>
                    
                </div>
                """
        else:  #When there are no registered addresses
            html_content += f"""
                <div id="address_form">
                    <h2>Cadastrar Endereço de Entrega</h2>
                    <form action="/save_address" method="POST">
                       
                        <label for="street">Endereço (Linha 1):</label>
                        <input type="text" id="street" name="street" placeholder="Rua, avenida, etc." required>
                        <label for="number">Número (Linha 2):</label>
                        <input type="text" id="number" name="number" placeholder="Número" required>
                        <label for="neighborhood">Bairro:</label>
                        <input type="text" id="neighborhood" name="neighborhood" required>
                        <label for="city">Cidade:</label>
                        <input type="text" id="city" name="city" required>
                        <label for="state">Estado:</label>
                        <input type="text" id="state" name="state" required>
                        <label for="zipcode">CEP:</label>
                        <input type="text" id="zip_code" name="zip_code" required>
                        <label for="complement">Telefone:</label>
                        <input type="tel" id="complement" name="complement" placeholder="Complemento" required>
                        <button style="color: aqua;"  onclick="checkUserLoginStatus()">Cadastrar</button>
                    </form>
                </div>
            """
     else:
        # If the user is not logged in, it also displays the form
        html_content += f"""
            <h2>Entre ou cadastre-se para cadastrar um endereço</h2>
            <button style="color: aqua;"  onclick="checkUserLoginStatus()">Fazer Login</button>
        """

    # Closes the HTML structure
     html_content += """
        </div>
        <script src="/js/cart.js"></script>
    </body>
    </html>
    """

    # Sends the HTTP response with the rendered content
     self.send_response(200)
     self.send_header('Content-type', 'text/html')
     self.end_headers()
     self.wfile.write(html_content.encode('utf-8'))

      
    #Favorites list
    def list_favorits_my(self):
    #Retrieves the ID of the logged in user
     user_id = self.get_user_id_from_cookies()

    # Initializes the product and favorites controller
     controller = ProductController()
     products = controller.list_products()
    
     favs = FavoritesController()
     fav = favs.list_fav()

     fav_html = ""  # Variable to store the HTML of all bookmarks
    # Iterates through favorites and products to generate HTML
     for f in fav:
        # Checks if the favorite belongs to the logged in user
        if self.verify_user_owns_favorite(user_id, f['id_fav']):
            for product in products:
                if product["id"] == f['id']:
                    #Generate HTML only for items owned by the logged in user
                    fav_html += f"""
                    <html lang="en">
                    <head>
                        <meta charset="UTF-8">
                        <meta name="viewport" content="width=device-width, initial-scale=1.0">
                        <title>Favoritos</title>
                    </head>
                    <body>
                    <div class="my_cart">
                        <h1>Meus Favoritos</h1>
                        <div class="favorite-item">
                            <div class="image-container">
                                <img src="{f['image']}" alt="Imagem do produto" class="favorite-image">
                                <div class="quick-view">
                                    <a href="/detalhes?id={product['id']}" class="quick-view-link"><i class="fa fa-eye" aria-hidden="true"></i></a>
                                </div>
                            </div>
                            <div class="favorite-details">
                                <form  action="/delete_fav" method="POST">
                                <input type="hidden"  name="id_fav" value ="{f['id_fav']}">
                                <button  type="submit">Remover dos Favoritos</button>
                                </form>
                            </div>
                        </div>
                    </div>
                    """

    # Renderizar o HTML com a variável fav_html
     html_content = self._render_template("customer/favorits_my", {"fav": fav_html})
     if html_content:
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(html_content.encode('utf-8'))
     else:
        self.handle_404()


    #Delete favorites
    def delet_favorits(self):
       content_length = int(self.headers['Content-Length'])
       post_data = self.rfile.read(content_length)
       data = parse_qs(post_data.decode('utf-8'))
       id_fav  = data.get('id_fav', [None])[0]
      
       delet_fav = FavoritesController()
       delet_fav.delete_fave(id_fav)
       self.send_response(302)  
       self.send_header('Location', '/my_account')  
       self.end_headers()


    #payment registration
    def handle_checkout_cart(self):
        customer_id = self.get_user_id_from_cookies()
        controller = CartController()
        #Gets cart items for the user
        cart_items = controller.list_cart(customer_id)
        payment_controller = PymentController 
        payments = payment_controller.list_pyment_id(customer_id)
        print(customer_id)
        for cart_item in cart_items:
          cart_content = f"""
       
        <div class="payment-container">  
        
        <div class="column left">
            <img src="{cart_item['product_image']} alt="{cart_item['product_name']}">
        </div>
        <div class="column middle">
            
            <div class="sold">
                <p>Vendido e entregue por <span><b>{cart_item['product_mark']}</b></span></p>
             
               <form action="/delete_cart" method="post">
               <input type="hidden" id="user_id" name="cart_id" value="{cart_item['cart_id']}" required>
                <input style="background-color: white;border: none; cursor: pointer;" type="submit" onclick="removeFromCart('{cart_item['id']}')"value="Remover"> 
              </form>
            </div>
        </div>
        <div class="column right">
            <p>Quantidade</p>
            <span> {cart_item['quantity']} </span>
        </div>
        <div class="column price">
            <h1>R$ <span id="total-price-{cart_item['id']}">{cart_item['totalPriceElement']}</span></h1>
        </div>
   

            """
         
        if payments == []:
          
       
           pyment_content = f"""
           <div class="product-summary">
          <form action="/save_orders" method="post" class="payment-form" onsubmit="return validateCardForm()">
    <h2>Pagamento</h2>

    <input type="hidden" id="user_id" name="cart_id" value="{cart_item['cart_id']}" required>

    <label for="card_number">Número do Cartão:</label>
   <input type="text" id="card_number" name="card_number" placeholder="0000 0000 0000 0000"
       maxlength="19" required>
<small class="form-help">O número deve ter entre 13 e 19 dígitos.</small>

    <label for="card_name">Nome no Cartão:</label>
    <input type="text" id="card_name" name="card_name" placeholder="Nome Completo"
           pattern="[A-Za-zÀ-ú ]+" required>
    <small class="form-help">Apenas letras e espaços são permitidos.</small><br>

    <label for="expiry_date">Data de Validade:</label>
    <input type="text" id="expiry_date" name="expiry_date" placeholder="MM/YY" required>
    <small class="form-help">Insira a data de validade no formato MM/YY.</small><br>

    <label for="cvv">CVV:</label>
    <input type="text" id="cvv" name="cvv" placeholder="123"  maxlength="4" required>
    <small class="form-help">O CVV deve ter 3 ou 4 dígitos.</small><br>

    <button type="submit">Finalizar Pagamento</button>
</form>

            </div>
            </div>
            
                 <script src="/js/cart.js"></script>
                 <script>
            location.reload();
            break
            </script>
                </body>
             </html>
             """ 

        else:
           for payment in payments:
              pyment_content = f"""
                <div class="product-summary">
                <form action="/save_orders" method="post" class="payment-form" onsubmit="return validateCardForm()">
                <h2>Pagamento</h2>
                <input type="hidden" id="user_id" name="cart_id" value=" {cart_item['cart_id']}" required>
    
                <input type="hidden" id="payment_id" name="payment_id" value="{payment['payment_id']}" required>
                <label for="card_number">Número do Cartão:</label>
                 <input type="text" id="card_number" name="card_number" value="{payment['card_number']}"
                    maxlength="19" required><br>

                <label for="card_name">Nome no Cartão:</label>
                 <input type="text" id="card_name" name="card_name"  value="{payment['card_name']}" 
                    pattern="[A-Za-zÀ-ú ]+"  required><br>

                <label for="expiry_date">Data de Validade:</label>
                 <input type="text" id="expiry_date" name="expiry_date" placeholder="MM/AA" value="{payment['expiry_date']}" 
                 placeholder="MM/YY" required><br>

                <label for="cvv">CVV:</label>
                 <input type="text" id="cvv" name="cvv" value="{payment['cvv']}" 
                  maxlength="4" required><br>
    
                 <button type="submit">Finalizar Pagamento</button>
                </form>

    <script src="/js/cart.js"></script>
     <script>
            location.reload();
            break
            </script>
                </body>
             </html>
            """
            
# Renderiza o HTML ou faz o que for necessário com o html_content
        html_content = self._render_template(
            "checkout", 
            {
               "cart_content": cart_content,
               "pyment": pyment_content
            }
        )
        
        
         
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(html_content.encode('utf-8'))


    #Delete cart
    def delet_cart(self):
       content_length = int(self.headers['Content-Length'])
       post_data = self.rfile.read(content_length)
       data = parse_qs(post_data.decode('utf-8'))
       cart_id   = data.get('cart_id', [None])[0]
      
       delet_cart = CartController()
       delet_cart.delet_cart(cart_id)
       self.send_response(302) 
       self.send_header('Location', '/') 
       self.end_headers()


    #save orders
    def handle_save_orders(self):
       user_id = self.get_user_id_from_cookies()
        
       
       content_length = int(self.headers['Content-Length'])
       post_data = self.rfile.read(content_length)
       data = parse_qs(post_data.decode('utf-8'))

       
       cart_id = data.get('cart_id', [None])[0]
       adress = AddressController.get_address_id(user_id)
       orders_controller = OderController()
      
       for ad in adress:
        address_id = ad["address_id"]
        print(address_id)
        if verify_user_owns_address(user_id, address_id):
         print("kkkk",user_id, address_id)             
         
         order_id = orders_controller.register_order(user_id, address_id, cart_id)
         
       card_number = data.get('card_number', [None])[0]
       card_name = data.get('card_name', [None])[0]
       expiry_date = data.get('expiry_date', [None])[0]
       payment_id = data.get('payment_id', [None])[0]
       cvv = data.get('cvv', [None])[0]
       amount = 100.00 
       order_id = data.get('cart_id', [None])[0]
      
    # Payment validation simulation
       if card_number and card_name and expiry_date and cvv:
        # Simulated payment success
        payment_status = 'Sucesso'
        save_payment = PymentController()
        save_payment.save_payment(payment_id,order_id, card_number, card_name, expiry_date, cvv, amount, payment_status,user_id)
        self.send_response(302)
        self.send_header('Location', '/my_account')
        self.end_headers()
       else:
        # Payment failed
        payment_status = 'Falha'
        save_payment = PymentController()
        save_payment.save_payment(order_id, card_number, card_name, expiry_date, cvv, amount, payment_status,user_id)
        self.send_response(400)
        self.send_header('Location', '/')
        self.end_headers()

       cart_items_ = CartController()
       cart_items = cart_items_.list_cart(user_id)
       order = OderController
       order = order.list_order()
       
       
       for item in cart_items:
            product_id = item['id']
            quantity = item['quantity']
            price = item['price']
            
       for i in  order:
          order_id = i['order_id']   
       orders_controller.register_order_item(order_id,product_id, quantity, price)  


    #save addresses
    def handle_save_address(self):
        user_id = self.get_user_id_from_cookies()
        
        
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        data = parse_qs(post_data.decode('utf-8'))
        street = data.get('street', [None])[0]
        number = data.get('number', [None])[0]
        neighborhood = data.get('neighborhood', [None])[0]
        complement = data.get('complement', [None])[0]
        city = data.get('city', [None])[0]
        state = data.get('state', [None])[0]
        zip_code = data.get('zip_code', [None])[0]
        
        address_cpntroller = AddressController()
        adress = AddressController.get_address_id(user_id)
        if adress == []:
           print("u",user_id)
           address_id = None
           address_cpntroller.save_adress(user_id, address_id, street, number, neighborhood, complement, city, state, zip_code)
           
        else:
          for ad in adress:
           
           address_id = ad["address_id"]
         
           if verify_user_owns_address(user_id, address_id):
            
            
            address_cpntroller.save_adress(user_id, address_id, street, number, neighborhood, complement, city, state, zip_code)
          
            
        self.send_response(302)  
        self.send_header('Location', '/checkout')
        self.end_headers()


    #save payment
    def handle_payment(self):
      content_length = int(self.headers['Content-Length'])
      post_data = self.rfile.read(content_length)
      data = parse_qs(post_data.decode('utf-8'))

      card_number = data.get('card_number', [None])[0]
      card_name = data.get('card_name', [None])[0]
      expiry_date = data.get('expiry_date', [None])[0]
      cvv = data.get('cvv', [None])[0]
      amount = 100.00  
      order_id = data.get('cart_id', [None])[0]

    # Payment validation simulation
      if card_number and card_name and expiry_date and cvv:
        # Simulated payment success
        payment_status = 'Sucesso'
        save_payment = PymentController()
        save_payment.save_payment(order_id, card_number, card_name, expiry_date, cvv, amount, payment_status)
        self.send_response(302)
        self.send_header('Location', '/my_account')
        self.end_headers()
      else:
        # Payment failed
        status = 'Falha'
        save_payment = PymentController()
        save_payment.save_payment(order_id, card_number, card_name, expiry_date, cvv, amount, payment_status)
        self.send_response(400)
        self.send_header('Location', '/')
        self.end_headers()


    #product list
    def handle_product_list(self):
        try:
            controller = ProductController()
            products = controller.list_products()
            products_html = "".join(
                f"<li>{product['name']} - ${product['price']} - <img src='/image/{product['images']}' alt='{product['name']}' /></li>"
                for product in products
            )
            html_content = self._render_template("product_list", {"products": products_html})

            if html_content:
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(html_content.encode('utf-8'))
            else:
                self.handle_404()
        except Exception as e:
            self.send_response(500)
            self.end_headers()
            self.wfile.write(f"Erro ao buscar produtos: {str(e)}".encode('utf-8'))



    #lidar com logout
    def handle_logout(self):
    # Clear login state
     self.logged_in_user = None  
     self.send_response(302)
     # Redirects to login page
     self.send_header('Location', '/login_user')  
     # Remove the cookie
     self.send_header('Set-Cookie', 'user_id=; Expires=Thu, 01 Jan 1970 00:00:00 GMT;') 
     self.end_headers()



    #Home page
    def handle_index(self):
      try:
        
        product_controller = ProductController()
        products = product_controller.list_products()
        slide = ProductController()
        slides = slide.list_slide()
        categorys = CategoryController()
        category = categorys.list_categories()
        #Show page title
        title = "Bem Vindo à Loja"
        full_page = self.render_template(title)
       

        # Render the products
        products_html = "".join(
            f"""
            <div class="product-card">
                <a href="/detalhes?id={product['id']}">
                    <img src="{product['images']}" alt="{product['name']}">
                </a>
                <h3>{product['name']}</h3>
                <p>Preço: R$ {product['price']:.3f}</p>
                    <p>Preço com Desconto: <strong>R$ {product['discount_price']:.3f}</strong></p>
                    <p>Classificação: <span style="color: gold;"> {'★' * product['product_rating']}</span> <span>{'☆' * (5 - product['product_rating'])}</span></p>
            </div>
            """ for product in products
        )

        # Render the categories
        categories_html = "".join(
                
                f'<ul><li><a href="/categoria?id={cat["id_categoria"]}">{cat["name"]}</a></li></ul>'
               
                 for cat in category)
        slides_html = "".join(
         f' <div class="Slides fade"><img src="{sli["slide_image"]}"></div>'
       for sli in slides
      )

        # Checks if the user is logged in
        

        html_content = self._render_template(
            "index", 
            {
                "products": products_html,
                "categories": categories_html,
                "slides": slides_html,
                "full_page": full_page,
               
            }
        )
        
        if html_content:
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(html_content.encode('utf-8'))
        else:
            self.handle_404()
      except Exception as e:
        self.send_response(500)
        self.end_headers()
        self.wfile.write(f"Erro ao carregar a página: {str(e)}".encode('utf-8'))



    #Category Page
    def handle_category_page(self, category_id):
     try:
        #Capture category ID from URL
        category_id = self.get_query_param('id')
        if not category_id:
            self.send_response(400)
            self.end_headers()
            self.wfile.write(b"Erro: Categoria nao especificada.")
            return
        
        #Calls the controller to get the products in the category
        category_data = CategoryController.list_products_by_category(category_id)
        category_item = CategoryController.list_subItem_category(category_id)
        ranges = ProductController.get_price_ranges()  
        if category_data["products"] is not None:
            category_name = category_data["category_name"]
            
            # Generate the HTML for the breadcrumb directly here
            breadcrumb_html = f"""
           
               <span>
                    <a href="categoria?id={category_id}">{category_name}</a>
                    <span class="anbgle fa fa-angle-right" aria-hidden="true"></span>
                </span>
           
            """

            bread_html = f"""
           
               {category_name}
               
           
            """
            title = category_name
            full_page = self.render_template(title)

            #Generates the HTML to display the products
            products_html = "".join(
                f"""
                <div class="product">
                    <a href="/detalhes?id={product['id']}">
                        <img src="{product['images']}" alt="{product['name']}  class="product-image"">    
                    </a>
                    <h3 class="product-name">{product['name']}</h3>
                    <p class="">Preço: R$ {product['price']:.3f}</p>
                    <p class="product-discount" >Preço com Desconto: <strong>R$ {product['discount_price']:.3f}</strong></p>
                     <p>Classificação: <span style="color: gold;"> {'★' * product['product_rating']}</span> <span>{'☆' * (5 - product['product_rating'])}</span></p>
                </div>
                """ for product in category_data["products"]
            )

            item_category = "".join(
                f""" 
    
                <div class="sub-category-item">
                    <div class="">
                      <a href="/sub_item?id_sub_item={item["id_categoria"]}">
                      <h5 class="sub-category-name">{item["nome_categoria"]}</h5>
                      </a>
                    </div>
                </div> """
                 for item in category_item
            )

            # HTML Generation
            categories_html = ""
            
           
            for label, min_price, max_price in ranges: 
              categories_html += f"""
            <div class="price-range">
                <a href="/category_pryce?id={category_id}&min_price={min_price}&max_price={max_price}">
                    {label} <!-- Aqui você pode adicionar a contagem real -->
                </a>
            </div>
            """
            
        

          
               
                 
      


           
            # Renderiza o template da página de categoria com os produtos filtrados
            html_content = self._render_template("category", {
                "breadcrumb": breadcrumb_html,
                "products": products_html,
                "bread": bread_html,
                "full_page":full_page,
                "category_price" : categories_html,
                "item_category": item_category,
               
            })
            
            if html_content:
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(html_content.encode('utf-8'))
            else:
                self.handle_404()
    
     except Exception as e:
        self.send_response(500)
        self.end_headers()
        self.wfile.write(f"Erro ao carregar a página: {str(e)}".encode('utf-8'))


    #Category with price list
    def category_price_list(self,category_id, min_price, max_price):
       try:
        # Capture category ID from URL
        category_id = self.get_query_param('id')
        min_price = self.get_query_param('min_price')
        max_price = self.get_query_param('max_price')
       
        if not category_id:
            self.send_response(400)
            self.end_headers()
            self.wfile.write(b"Erro: Categoria nao especificada.")
            return
        
        # Calls the controller to get the products in the category
        range = ProductController.list_by_price(category_id,min_price,max_price)
        
        
          
        if range["products"] is not None:
            category_name = range["category_name"]
          
            for product in range["products"]:
               product_price = product["price"]
               category_item = CategoryController.category_price_cont(product_price)
               
            # Generate the HTML for the breadcrumb directly here
            breadcrumb_html = f"""
           
               <span>
                    <a href="categoria?id={category_id}">{category_name}</a>
                    <span class="anbgle fa fa-angle-right" aria-hidden="true"></span>
                </span>
           
            """

            bread_html = f"""
           
               {category_name}
               
           
            """


            # Gera o HTML para exibir os produtos
            products_html = "".join(
                f"""
                <div class="product">
                    <a href="/detalhes?id={product['id']}">
                        <img src="{product['images']}" alt="{product['name']}">    
                    </a>
                   <h3 class="product-name">{product['name']}</h3>
                    <p class="">Preço: R$ {product['price']:.3f}</p>
                    <p class="product-discount" >Preço com Desconto: <strong>R$ {product['discount_price']:.3f}</strong></p>
                     <p>Classificação: <span style="color: gold;"> {'★' * product['product_rating']}</span> <span>{'☆' * (5 - product['product_rating'])}</span></p>
                </div>
                """ for product in range["products"]
            )

            item_category = "".join(
                f""" 
                <div class="sub-category-item">
                      <a href="/product_pyce_filter?id_categoria_pai={item["id_categoria_pai"]}">
                      <h5 class="sub-category-name">{item["categoria_pai"]}</h5></a>
                    </div>
                 """
                 for item in category_item
            )


            title = category_name
            full_page = self.render_template(title)

            # Verifica se o usuário está logado
            
            
            # Renderiza o template da página de categoria com os produtos filtrados
            html_content = self._render_template("category_pryce", {
                "breadcrumb": breadcrumb_html,
                "products": products_html,
                "bread": bread_html,
                "item_category": item_category,
                "full_page" : full_page
            })
            
            if html_content:
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(html_content.encode('utf-8'))
            else:
                self.handle_404()
    
       except Exception as e:
        self.send_response(500)
        self.end_headers()
        self.wfile.write(f"Erro ao carregar a página: {str(e)}".encode('utf-8'))



    #Price filter
    def category_price_filter(self,id_categoria,id_categoria_pai):
        
        id_categoria = self.get_query_param('id_categoria')
        id_categoria_pai = self.get_query_param('id_categoria_pai')

    # Makes sure at least one of the two parameters was passed
        if id_categoria is None and id_categoria_pai is None:
          return {"error": "É necessário fornecer id_categoria ou id_categoria_pai"}

    # Calls the function that searches for products based on the parameters
        p = CategoryController.category_pai_category(id_categoria_pai=id_categoria_pai, id_categoria=id_categoria)
        
        # Generate the HTML for the breadcrumb directly here
        
        try:
        # Generating breadcrumbs
         breadcrumb_html = "".join(f"""
            <span>
                <a href="/categoria?id={product["id_vo"]}">{product['categoria_vo']}</a>
                <span class="angle fa fa-angle-right" aria-hidden="true"></span>
            </span>
            <span>
                <a href="/sub_item?id_sub_item={product["id_pai"]}">{product['categoria_pai']}</a>
                <span class="angle fa fa-angle-right" aria-hidden="true"></span>
            </span>
            <span>
                <a href="/product_filter_category?id_categoria={product["id_categoria"]}">{product['categoria']}</a>
                <span class="angle fa fa-angle-right" aria-hidden="true"></span>
            </span>
        """ for product in p)
        # Handling the case where vo_category or parent_category may not exist
        except KeyError: 
         breadcrumb_html = "".join(f"""
            <span>
                <a href="/categoria?id={product["id_vo"]}">{product['categoria_vo']}</a>
                <span class="angle fa fa-angle-right" aria-hidden="true"></span>
            </span>
            <span>
                <a href="/sub_item?id_sub_item={product["id_pai"]}">{product['categoria_pai']}</a>
                <span class="angle fa fa-angle-right" aria-hidden="true"></span>
            </span>
        """ for product in p)
    
        for product in p:
           
         title = product['categoria_pai']
         full_page = self.render_template(title)
        
        products_html = "".join(
                f"""
                <div class="product">
                    <a href="/detalhes?id={product['product_id']}">
                        <img src="{product['product_image']}" alt="{product['product_name']}">    
                    </a>
                   <h3 class="product-name">{product['product_name']}</h3>
                    <p class="">Preço: R$ {product['product_price']:.3f}</p>
                    <p class="product-discount" >Preço com Desconto: <strong>R$ {product['discount_price']:.3f}</strong></p>
                     <p>Classificação: <span style="color: gold;"> {'★' * product['product_rating']}</span> <span>{'☆' * (5 - product['product_rating'])}</span></p>
                </div>
                """ for product in p
            )

        html_content = self._render_template("product_pyce_filter", {
                
                "products": products_html,
                "breadcrumb":breadcrumb_html,
                 "full_page": full_page
             })
        
        html_content
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(html_content.encode('utf-8'))


    #Filter prices and categories
    def category_price_filter_category(self,id_categoria):
        
        id_categoria = self.get_query_param('id_categoria')
       
    # Makes sure at least one of the two parameters was passed
       

    # Calls the function that searches for products based on the parameters
        p = CategoryController.category_category_category(id_categoria)
        
        # Generate the HTML for the breadcrumb directly here
        
       
        # Generating breadcrumbs
        breadcrumb_html = "".join(f"""
            <span>
                <a href="/categoria?id={product["id_vo"]}">{product['categoria_vo']}</a>
                <span class="angle fa fa-angle-right" aria-hidden="true"></span>
            </span>
            <span>
                <a href="/sub_item?id_sub_item={product["id_pai"]}">{product['categoria_pai']}</a>
                <span class="angle fa fa-angle-right" aria-hidden="true"></span>
            </span>
            <span>
                <a href="/product_filter_category?id_categoria={product["id_categoria"]}">{product['categoria']}</a>
                <span class="angle fa fa-angle-right" aria-hidden="true"></span>
            </span>
        """ for product in p)
        
    
   

        
        products_html = "".join(
                f"""
                <div class="product">
                    <a href="/detalhes?id={product['product_id']}">
                        <img src="{product['product_image']}" alt="{product['product_name']}">    
                    </a>
                    <h3 class="product-name">{product['product_name']}</h3>
                    <p class="">Preço: R$ {product['product_price']:.3f}</p>
                    <p class="product-discount" >Preço com Desconto: <strong>R$ {product['discount_price']:.3f}</strong></p>
                     <p>Classificação: <span style="color: gold;"> {'★' * product['product_rating']}</span> <span>{'☆' * (5 - product['product_rating'])}</span></p>
                </div>
                """ for product in p
            )
        for product in p:
         title = product['categoria']
         full_page = self.render_template(title)

        html_content = self._render_template("product_filter_category", {
                
                "products": products_html,
                "full_page":full_page,
                "breadcrumb":breadcrumb_html
             })
        
        html_content
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(html_content.encode('utf-8'))
        
        
        
    #category sub item page             
    def handle_sub_item_page(self, id_sub_item):
      try:
        id_sub_item = self.get_query_param('id_sub_item')
       
        
        if not id_sub_item:
            self.send_response(400)
            self.end_headers()
            self.wfile.write(b"Erro: Categoria nao especificada.")
            return
        
        # Get the category names
        category_item = CategoryController.get_category_names(id_sub_item)
       
        products_item = CategoryController
        products = products_item.list_sub_item(id_sub_item)
        sub = CategoryController
        subcategories = sub.list_subItem_category(id_sub_item)  
        
        # Generate the HTML for the breadcrumb
        for item in category_item:
          breadcrumb_html = f"""
       
            <span>
                <a href="categoria?id={item["id_2"]}">{item["parent_category_name"]}</a>
                <span class="anbgle fa fa-angle-right" aria-hidden="true"></span>
            </span>
            <span>
                <a href="sub_item?id_sub_item={item["id_1"]}">{item["subcategory_name"]}</a>
            </span>
      
        <div> <h1>{item["subcategory_name"]}</h1> </div>
        """
          sidebar_html = "".join(
            f"""
            <div class="subcategory">
                <h4>{item["parent_category_name"]}</h4>
                <h3>{item["subcategory_name"]}</h3>
             
                    <a href="/product_pyce_filter?id_categoria={subcategory['id_categoria']}">
                       <h5 class="sub-category-name">{subcategory['nome_categoria']}</h5></a>
             </div>
            """ for subcategory in subcategories
        )
        
        tilte_html = "".join({item["subcategory_name"]})
        # Gera o HTML para exibir os produtos
        products_html = "".join(
            f"""
            <div class="product">
                <a href="/detalhes?id={product['product_id']}">
                    <img src="{product['product_image']}" alt="{product['product_name']}">    
                </a>
                 <h3 class="product-name">{product['product_name']}</h3>
                    <p class="">Preço: R$ {product['product_price']:.3f}</p>
                    <p class="product-discount" >Preço com Desconto: <strong>R$ {product['discount_price']:.3f}</strong></p>
                     <p>Classificação: <span style="color: gold;"> {'★' * product['product_rating']}</span> <span>{'☆' * (5 - product['product_rating'])}</span></p>
                </div>
            """ for product in products
        )

        title = tilte_html
        full_page = self.render_template(title)
       
        # Renderiza o template da página do subitem com os produtos filtrados
        html_content = self._render_template("sub_item", {
            "breadcrumb": breadcrumb_html,
            "products": products_html,
             "sidebar": sidebar_html,
             "full_page": full_page,
           
        })
        
        if html_content:
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(html_content.encode('utf-8'))
        else:
            self.handle_404()

      except Exception as e:
        self.send_response(500)
        self.end_headers()
        self.wfile.write(f"Erro ao carregar a página: {str(e)}".encode('utf-8'))
        
    #Products page
    def handle_product_page(self,product_id):
     try:
        # Capture the product ID from the URL
        product_id = self.get_query_param('id')
        if not product_id:
            self.send_response(400)
            self.end_headers()
            self.wfile.write(b"Erro: Produto nao especificado.")
            return
        
        # Get product details
        product_details = CategoryController.list_sub_item(product_id)  # Função que busca detalhes do produto
        for detail in product_details:
          
         if not product_details:
            self.handle_404()
            return
        
        # Get the category names
        id_categoria = detail["id_categoria"]
        hierarquia_categorias = ProductController.list_products_by_category(id_categoria)

        # Building the breadcrumb
        breadcrumb_parts = [categoria["nome_categoria"] for categoria in reversed(hierarquia_categorias)]
        breadcrumb = " > ".join(breadcrumb_parts)
       
        
        item_id = hierarquia_categorias[0]["price"]
        item_none = hierarquia_categorias[2]["nome_categoria"]
        print(item_none)
        sub = CategoryController
        subcategories = sub.list_subItem_category(item_id)
        print(subcategories)
        for c in subcategories:
        
       
        # Generate the HTML for the breadcrumb
         breadcrumb_html = f"""
        <div class="links">
            <span>
                <a href="/">site.com.br</a>
                <span class="anbgle fa fa-angle-right" aria-hidden="true"></span>
            </span>
            <span>
                <a href="/">{breadcrumb}</a>
                <span class="anbgle fa fa-angle-right" aria-hidden="true"></span>
            </span>
           
        </div>
        <div> <h1>{c["nome_categoria"]}</h1></div>
        <div> <h1>{item_none}</h1></div>
        """

        # Search for related products in the same subcategory
        related_products = CategoryController.list_sub_item(id_categoria)
       
        # Generates HTML to display related products
        related_products_html = "".join(
            f"""
            <div class="product">
                <a href="/detalhes?id={product['product_id']}">
                    <img src="{product['product_image']}" alt="{product['product_name']}">    
                </a>
                <h3>{product['product_name']}</h3>
                <p>Preço: R$ {product['product_price']}</p>
                <p>Preço com Desconto: <strong>R$ {product['discount_price']}</strong></p>
                <p>Classificação: {"★" * int(product['product_rating'])}</p>
            </div>
            """ for product in related_products
        )
        title = "Existe"
        full_page = self.render_template(title)
        # Renders the product page template with details and related products
        html_content = self._render_template("subitem", {
            "breadcrumb": breadcrumb_html,
            "related_products": related_products_html,
            "full_page":full_page
            
        })
        
        if html_content:
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(html_content.encode('utf-8'))
        else:
            self.handle_404()

     except Exception as e:
        self.send_response(500)
        self.end_headers()
        self.wfile.write(f"Erro ao carregar a página: {str(e)}".encode('utf-8'))



    #Login page
    def handle_login_user(self, redirect_page=None):
    #Renders the login page with the redirect parameter if present
     context = {"redirect_page": redirect_page} if redirect_page else {}
     html_content = self._render_template("login_user", context)
     self.send_response(200)
     self.send_header('Content-type', 'text/html')
     self.end_headers()
     self.wfile.write(html_content.encode('utf-8'))


    #Registration page
    def handle_cadastro(self):
        html_content = self._render_template("cadastro", {})
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(html_content.encode('utf-8'))


    #Customer payment page
    def handle_payment_my_account(self):
      # Get the user_id from the cookie 
     customer_id = self.get_user_id_from_cookies() 

     if customer_id is None:
        self.send_response(401)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps({'logged_in': False}).encode())
        return
     print(f"User ID recuperado do cookie: {customer_id}")
    
     payment_controller = PymentController  
     payments = payment_controller.list_payments() 
     print(f"Pagamentos encontrados: {payments}")
     # Initialize empty HTML
     pyment_html = "" 
    
    # Iterates over payments and generates HTML
     for payment in payments:
        #Gets the order_id related to the payment
        order_id = payment['order_id']  
        
        # Checks if the logged in user is the owner of the order associated with the payment
        if not verify_user_owns_order(customer_id, order_id):
            print(f"Usuário {customer_id} não é dono do pedido {order_id}")
            continue  # Skip this payment if the user is not the owner
        print(f"Renderizando pagamento para o usuário {customer_id}, order_id: {order_id}")
        # Generate HTML for payment
        pyment_html += f"""
         
            <div class="card-payment">
         
                <div class="card-payment-header">
                    <h5>Debit / Credit Card</h5>
                    <button id="editPaymentButton-{payment['payment_id']}" class="btn-edit" data-payment-id="{payment['payment_id']}">✏️</button>
                    
                </div>
                <div class="card-payment-body">
                    <p><strong>Card Number:</strong> {payment['card_number']}</p>
                    <p><strong>Expiry Date:</strong> {payment['expiry_date']}</p>
                    <p><strong>Name on Card:</strong> {payment['card_name']}</p>
                </div>
            </div>
            <div id="paymentModal-{payment['payment_id']}" class="modal">
            <div class="modal-content">
                <span class="close">&times;</span>
                <h2>Editar Detalhes de Pagamento</h2>
                <!-- Formulário de edição de pagamento -->
                <form id="editPaymentForm" action="/updadte_payment" method="post" onsubmit="return validateCardForm()">
                   <label for="card_number">Número do Cartão:</label>
                 <input type="text" id="card_number" name="card_number" value="{payment['card_number']}"
                    maxlength="19" required><br>

                <label for="card_name">Nome no Cartão:</label>
                 <input type="text" id="card_name" name="card_name"  value="{payment['card_name']}" 
                    pattern="[A-Za-zÀ-ú ]+"  required><br>

                <label for="expiry_date">Data de Validade:</label>
                 <input type="text" id="expiry_date" name="expiry_date" placeholder="MM/AA" value="{payment['expiry_date']}" 
                 placeholder="MM/YY" required><br>

                <label for="cvv">CVV:</label>
                 <input type="text" id="cvv" name="cvv" value="{payment['cvv']}" 
                  maxlength="4" required><br>
    
                    <button type="submit">Salvar Alterações</button>
                </form>
            </div>
        </div>
        """
     if not pyment_html:
        # If no payment is rendered, add an error message or log
        print("Nenhum pagamento foi renderizado.")
    #Render HTML with the pyment_html variable
     html_content = self._render_template("customer/payment", {"pyment": pyment_html})
     print(f"HTML gerado: {html_content}")
     self.send_response(200)
     self.send_header('Content-type', 'text/html')
     self.end_headers()
     self.wfile.write(html_content.encode('utf-8'))


  
    #Update payment
    def updadte_payment(self):
       content_length = int(self.headers['Content-Length'])
       post_data = self.rfile.read(content_length)
       data = parse_qs(post_data.decode('utf-8'))
       card_number = data.get('card_number', [None])[0]
       card_name = data.get('card_name', [None])[0]
       payment_id = data.get('payment_id', [None])[0]
       expiry_date = data.get('expiry_date', [None])[0]
       cvv = data.get('cvv', [None])[0]
      
        
       order_id = data.get('order_id', [None])[0]
       updat_pay = PymentController()
       updat_pay.update_payment(payment_id, order_id, card_number, card_name, expiry_date, cvv)
       self.send_response(302)
       self.send_header('Location', '/')
       self.end_headers()
       


    #Customer address page
    def handle_accounty_addrress(self):
     address_controller = AddressController
     address_list = address_controller.list_address()
     user_id = self.get_user_id_from_cookies()
     # Initialize empty HTML
     address_html = "" 

     for i in address_list:
        # Get the address ID
        address_id = i['address_id']  

       # Checks if the user owns the address
        if verify_user_owns_address(user_id, address_id):
           # Generate HTML for the address if the user owns it
            address_html += f"""
              <div class="card-payment">
                <div class="card-payment-header">
                    <h5>Endereço para envio</h5>
                    <button id="editAdressButton-{i['address_id']}" class="btn-edit" data-address-id="{i['address_id']}">✏️</button>
                </div>
                <div class="card-payment-body">
                    <p><strong>Rua:</strong> {i['street']}</p>
                    <p><strong>Número:</strong> {i['number']}</p>
                    <p><strong>Bairro:</strong> {i['neighborhood']}</p>
                    <p><strong>Complemento:</strong> {i['complement']}</p>
                    <p><strong>Cidade:</strong> {i['city']}</p>
                    <p><strong>Estado:</strong> {i['state']}</p>
                    <p><strong>CEP:</strong> {i['zip_code']}</p>
                </div>
            </div>

            <div id="adressModal-{i['address_id']}" class="modal">
                <div class="modal-content">
                    <span class="close">&times;</span>
                    <h2>Editar Endereço</h2>
                    <form id="editAdressButton" action="/save_address" method="POST">
                        <h2>Endereço de Entrega</h2>
                        <label for="street">Endereço (Linha 1):</label>
                        <input type="text" id="street" name="street" placeholder="Rua, avenida, etc." 
                               value="{i['street'] if 'street' in i else ''}" required>
                        <label for="number">Número (Linha 2):</label>
                        <input type="text" id="number" name="number" placeholder="Número" 
                               value="{i['number'] if 'number' in i else ''}" required>
                        <label for="neighborhood">Bairro:</label>
                        <input type="text" id="neighborhood" name="neighborhood" 
                               value="{i['neighborhood'] if 'neighborhood' in i else ''}" required>
                        <label for="city">Cidade:</label>
                        <input type="text" id="city" name="city" 
                               value="{i['city'] if 'city' in i else ''}" required>
                        <label for="state">Estado:</label>
                        <input type="text" id="state" name="state" 
                               value="{i['state'] if 'state' in i else ''}" required>
                        <label for="zipcode">CEP:</label>
                        <input type="text" id="zip_code" name="zip_code" 
                               value="{i['zip_code'] if 'zip_code' in i else ''}" required>
                        <label for="complement">Telefone:</label>
                        <input type="tel" id="complement" name="complement" placeholder="Complemento" 
                               value="{i['complement'] if 'complement' in i else ''}" required>
                        <input type="submit" value="Submit">
                    </form>
                </div>
            </div>
            <script src="/js/cart.js"></script>
            """
        

    # Render HTML with the address_html variable
     html_content = self._render_template("customer/address", {"address": address_html})
     self.send_response(200)
     self.send_header('Content-type', 'text/html')
     self.end_headers()
     self.wfile.write(html_content.encode('utf-8'))



    #submit rating
    def handle_submit_rating(self):
     try:
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length).decode('utf-8')
        params = parse_qs(post_data)

        product_id = params.get('product_id')[0]
        rating = int(params.get('rating')[0])

        controller = ProductController()
        result = controller.submit_rating(product_id, rating)

        if result['success']:
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(f"Classificação enviada com sucesso!".encode('utf-8'))
        else:
            self.send_response(500)
            self.end_headers()
            self.wfile.write(f"Erro ao enviar classificação: {result['message']}".encode('utf-8'))

     except Exception as e:
        self.send_response(500)
        self.end_headers()
        self.wfile.write(f"Erro ao processar requisição: {str(e)}".encode('utf-8'))


    #Load the pages
    def _render_template(self, template_name, context=None):
        if context is None:
            # Ensuring context is not None
            context = {}  

        try:
            # Reads the template HTML file
            with open(f'views/{template_name}.html', 'r', encoding='utf-8') as file:
                html_content = file.read()

            # Replaces context variables in HTML content
            for key, value in context.items():
                html_content = html_content.replace(f'{{{{ {key} }}}}', str(value))

            return html_content
        except FileNotFoundError:
            return None
        
#Start server
def run(server_class=HTTPServer, handler_class=MyHandler, port=8080):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Servindo na porta {port}...')
    httpd.serve_forever()



if __name__ == "__main__":
    run()