function changeImage(imageSrc) {
    const mainImage = document.getElementById('currentImage');
    mainImage.style.opacity = '0';  // Fade out effect
    setTimeout(() => {
        mainImage.src = imageSrc;
        mainImage.style.opacity = '1';  // Fade in effect
    }, 300);  // Time to change the image (matches the fade out)
}

const imageContainer = document.querySelector('.main-image');
const image = document.querySelector('#currentImage');

// Event listener for mousemove to track mouse position inside the container
imageContainer.addEventListener('mousemove', function(e) {
    const rect = imageContainer.getBoundingClientRect();
    const x = e.clientX - rect.left; // X position inside the container
    const y = e.clientY - rect.top;  // Y position inside the container

    const xPercent = (x / rect.width) * 100;
    const yPercent = (y / rect.height) * 100;

    // Move the image to the correct point, keeping the zoom effect
    image.style.transformOrigin = `${xPercent}% ${yPercent}%`;
    image.style.transform = 'scale(2)'; // Zoom the image
});

// Event listener for mouseleave to reset image size and position
imageContainer.addEventListener('mouseleave', function() {
    image.style.transform = 'scale(1)'; // Reset to normal size
    image.style.transformOrigin = 'center'; // Reset the origin point
     if (window.location.pathname === '/cart.html') {
        displayCartItems();  // Display items in the cart if on the cart page
    }
    updateCartCount();  // Update cart count
});

// Function to add product to the cart
function addToCart(product_id, productName, price, images) {
    // Check if there is already a cart in localStorage
    let cart = JSON.parse(localStorage.getItem('cart')) || [];

    // Check if the product is already in the cart
    let existingProduct = cart.find(item => item.id == product_id);

    if (existingProduct) {
        // Increment the quantity if the product is already in the cart
        existingProduct.quantity += 1;
    } else {
        // Add the new product to the cart
        cart.push({
            id: product_id,
            name: productName,
            price: price,
            images: images,
            quantity: 1
        });
    }

    // Update localStorage with the new cart data
    localStorage.setItem('cart', JSON.stringify(cart));

    alert('Product added to the cart!');
    updateCartCount();  // Update cart count after adding the product
}
