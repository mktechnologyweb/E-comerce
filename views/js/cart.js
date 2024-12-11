document.addEventListener('DOMContentLoaded', function() {
    updateCartCount();
    displayCartItems();
});

function displayCartItems() {
    const cartItems = JSON.parse(localStorage.getItem('cart')) || [];
    const cartContainer = document.getElementById('cartItems');
    cartContainer.innerHTML = ''; // Clear existing content

    if (cartItems.length === 0) {
        cartContainer.innerHTML = '<p>O carrinho está vazio.</p>';
        return;
    }

    let totalPrice = 0; // Initializes the total
    let totalQuantity = 0; // Initializes the product count

    cartItems.forEach(item => {
        const itemDiv = document.createElement('div');
        itemDiv.className = 'row';

        //Generates quantity options
        let quantityOptions = '';
        for (let i = 1; i <= 10; i++) {
            quantityOptions += `<option value="${i}" ${i === item.quantity ? 'selected' : ''}>${i}</option>`;
        }

        // Calculate the total for this item
        const itemTotalPrice = (item.price * item.quantity).toFixed(2);
        totalPrice += parseFloat(itemTotalPrice); // Add to total
        totalQuantity += item.quantity; //Adds to product count

        itemDiv.innerHTML = `
            <div class="column left">
                <img src="${item.images}" alt="${item.name}">
            </div>
            <div class="column middle">
                <a class="detail" href="">${item.name}</a>
                <div class="sold">
                    <p>Vendido e entregue por <span><b>Marca</b></span></p>
                    <div class="save"></div>
                    <a onclick="removeFromCart('${item.id}')" href="">Remover</a>
                </div>
            </div>
            <div class="column right">
                <p>Quantidade</p>
                <select class="select_qtd" onchange="updateQuantity('${item.id}', this.value)">
                    ${quantityOptions}
                </select>
            </div>
            <div class="column price">
                <h1>R$ <span id="total-price-${item.id}">${itemTotalPrice}</span></h1>
            </div>
        `;

        cartContainer.appendChild(itemDiv);
    });

    // View order summary
    const summaryDiv = document.createElement('div');
    summaryDiv.innerHTML = `
        <h2>Resumo do pedido</h2>
        <p>${totalQuantity.toString().padStart(2, '0')} Produto${totalQuantity !== 1 ? 's' : ''}</p>
        <p>R$ ${totalPrice.toFixed(2).replace('.', ',')}</p>
        <h3>Total</h3>
        <h2>R$ ${totalPrice.toFixed(2).replace('.', ',')}</h2>
        
    `;
    
    cartContainer.appendChild(summaryDiv);
}


function updateQuantity(productId, newQuantity) {
    const cartItems = JSON.parse(localStorage.getItem('cart')) || [];
    const item = cartItems.find(item => item.id === productId);
   
    if (item) {
        item.quantity = parseInt(newQuantity, 10);
        localStorage.setItem('cart', JSON.stringify(cartItems));
       
       
        //  Updates the total in the interface
        const newTotalPrice = (item.price * item.quantity).toFixed(2);
        const totalPriceElement = document.getElementById(`total-price-${productId}`);
        totalPriceElement.textContent = newTotalPrice;
        item.totalPriceElement = parseInt(newTotalPrice);
        localStorage.setItem('cart', JSON.stringify(cartItems)); // Updates the total price in the interface
    }

    updateCartCount();
    location.reload()
}

function clearCart() {
    localStorage.removeItem('cart');
    alert('Carrinho limpo!');
    displayCartItems();
}

function updateCartCount() {
    const cartItems = JSON.parse(localStorage.getItem('cart')) || [];
    const countElement = document.getElementById('cart-count');
    
    // Checks if the element is found before trying to update it
    if (countElement) {
        countElement.innerHTML = cartItems.reduce((total, item) => total + item.quantity, 0);
    } else {
        console.error("Elemento 'cart-count' não encontrado.");
    }
}

function removeFromCart(productId) {
    let cartItems = JSON.parse(localStorage.getItem('cart')) || [];
    cartItems = cartItems.filter(item => item.id !== productId); // Remove item
    localStorage.setItem('cart', JSON.stringify(cartItems)); //Updates localStorage
    displayCartItems(); // Updates cart view
}

async function checkUserLoginStatus() {
   
    try {
        const response = await fetch('/check_login_status');
      
        // Checks that the response is not a redirect or error
        if (response.status === 401) {
           
            // Redirect to login page if user is not logged in
            window.location.href = '/login_user?redirect=cart';
            
        } else {
            //The user is logged in, you can continue to the appropriate page
            const data = await response.json();
            if (data.logged_in) {
               
                saveCartToDatabase();
              
            }
        }
    } catch (error) {
        console.error('Erro ao verificar o status de login:', error);
    }
}
function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
    return null; // Returns null if cookie is not found
}
// Set the error message based on the cookie
const errorMessage = getCookie('error_message');
console.log('Error Message from Cookie:', errorMessage); // Log to check the value
// Display the message if set
if (errorMessage) {
    document.getElementById('error-message').textContent = errorMessage;
    console.log('Displaying error message:', errorMessage);// Log to confirm display

   // Remove error cookie after display
    document.cookie = 'error_message=; Path=/login_user; Expires=Thu, 01 Jan 1970 00:00:00 GMT';
} else {
    console.log('No error message found.'); // Log if there is no message
}



function saveCartToDatabase() {
    const cartItems = JSON.parse(localStorage.getItem('cart')) || [];
    
    fetch('/save_cart', {
        
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            
        },
        
        body: JSON.stringify({ cart: cartItems }),
        
    }).then(response => {
        if (response.ok) {
            alert('Carrinho salvo com sucesso!');
             //Clear local cart
        } else {
            alert('Erro ao salvar o carrinho.');
        }
    });
}

// Selects the elements
const useRegisteredAddressCheckbox = document.getElementById('use_registered_address');
const addressForm = document.getElementById('address_form');
const continueButton = document.getElementById('continue-button');




     



document.addEventListener('DOMContentLoaded', function() {
   // Use event delegation on the document or a parent container
    document.body.addEventListener('click', function(event) {
        // Check if the clicked element is a payment edit button
        if (event.target && event.target.id.startsWith('editPaymentButton')) {
            const paymentId = event.target.dataset.paymentId;
            const paymentModal = document.getElementById(`paymentModal-${paymentId}`);
            
            if (paymentModal) {
                paymentModal.style.display = 'block'; // Open corresponding modal
            } else {
                console.error(`Modal para o ID ${paymentId} não encontrado.`);
            }
        }

        // Close modal if close button is clicked
        if (event.target && event.target.classList.contains('close')) {
            const modal = event.target.closest('.modal');
            if (modal) {
                modal.style.display = 'none'; //Close modal
            }
        }
    });

    // Close modal when clicking outside of it
    window.addEventListener('click', function(event) {
        const openModal = document.querySelector('.modal[style*="display: block"]');
        if (openModal && event.target === openModal) {
            openModal.style.display = 'none'; // Fechar o modal aberto
        }
    });

   
});




document.addEventListener('DOMContentLoaded', function() {
    //Use event delegation on the document or a parent container
    document.body.addEventListener('click', function(event) {
        //Check if the clicked element is an address edit button
        if (event.target && event.target.id.startsWith('editAdressButton')) {
            const addressId = event.target.dataset.addressId;
            const adressModal = document.getElementById(`adressModal-${addressId}`);
            
            if (adressModal) {
                adressModal.style.display = 'block'; // Open corresponding modal
            } else {
                console.error(`Modal para o ID ${addressId} não encontrado.`);
            }
        }

        //  Close modal if close button is clicked
        if (event.target && event.target.classList.contains('close')) {
            const modal = event.target.closest('.modal');
            if (modal) {
                modal.style.display = 'none'; // Close modal
            }
        }
    });

    // Close modal when clicking outside of it
    window.addEventListener('click', function(event) {
        const openModal = document.querySelector('.modal[style*="display: block"]');
        if (openModal && event.target === openModal) {
            openModal.style.display = 'none'; // Close open modal
        }
    });

    // Logic to save the address via AJAX when the form is submitted
    document.body.addEventListener('submit', function(event) {
        if (event.target && event.target.classList.contains('address-form')) {
            event.preventDefault(); // Prevents default submit behavior
            const form = event.target;
            const formData = new FormData(form);
            
            // Sends the AJAX request
            fetch('/save_address', {
                method: 'POST',
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    alert('Endereço salvo com sucesso!');
                    form.closest('.modal').style.display = 'none'; //Close modal after success
                } else {
                    console.error('Erro ao salvar endereço:', data.error);
                    alert('Erro ao salvar o endereço.');
                }
            })
            .catch(error => {
                console.error('Erro ao salvar o endereço:', error);
                alert('Erro ao salvar o endereço.');
            });
        }
    });
});



function addToFavoritesss() {
    const favoritItems = JSON.parse(localStorage.getItem('favorites')) || [];
    fetch('/save_favorites', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            
        },
        body: JSON.stringify({ favorites: favoritItems }),
    }).then(response => {
        if (response.ok) {
            alert('Favoritos salvo com sucesso!');
           
        } else {
            alert('Erro ao salvar o favorito.');
        }
    });
}



function validateCardForm() {
   // Validates the card number by removing spaces
    const cardNumberInput = document.getElementById('card_number');
    const cardNumber = cardNumberInput.value.replace(/\s+/g, ''); // Remove spaces
    if (!/^\d{13,19}$/.test(cardNumber)) { // Validates if they are only numbers with between 13 and 19 digits
        alert("O número do cartão deve ter entre 13 e 19 dígitos.");
        return false;
    }

    //Validates the expiration date
    const expiryDate = document.getElementById('expiry_date').value;
    const [month, year] = expiryDate.split('/').map(Number);
    
    if (!month || !year || month < 1 || month > 12) {
        alert("A data de validade do cartão está incorreta.");
        return false;
    }

    const today = new Date();
    const currentYear = today.getFullYear() % 100; //Last 2 digits of current year
    const currentMonth = today.getMonth() + 1; // Current month (0 to 11)

    if (year < currentYear || (year === currentYear && month < currentMonth)) {
        alert("A data de validade do cartão está incorreta.");
        return false;
    }

    return true; // If everything is correct, the form can be submitted.
}