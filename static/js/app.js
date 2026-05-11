// static/js/app.js
const API_URL = '/api';
let cart = [];

// Initialize App
document.addEventListener('DOMContentLoaded', () => {
    loadProducts();
    updateCartUI();
});

// Fetch Products
async function loadProducts() {
    const response = await fetch(`${API_URL}/products`);
    const products = await response.json();
    const container = document.getElementById('products-container');
    
    container.innerHTML = products.map(product => `
        <div class="product-card">
            <h3>${product.name}</h3>
            <p class="price">$${product.price.toFixed(2)}</p>
            <p>${product.description}</p>
            <button onclick="addToCart(${product.id}, '${product.name}', ${product.price})">
                Add to Cart
            </button>
        </div>
    `).join('');
}

// Cart Logic
function addToCart(id, name, price) {
    const existingItem = cart.find(item => item.id === id);
    if (existingItem) {
        existingItem.quantity += 1;
    } else {
        cart.push({ id, name, price, quantity: 1 });
    }
    updateCartUI();
}

function updateCartUI() {
    const cartContainer = document.getElementById('cart-items');
    const totalEl = document.getElementById('cart-total');
    
    let total = 0;
    cartContainer.innerHTML = cart.map(item => {
        total += item.price * item.quantity;
        return `
            <div class="cart-item">
                <span>${item.name} (x${item.quantity})</span>
                <span>$${(item.price * item.quantity).toFixed(2)}</span>
            </div>
        `;
    }).join('');
    
    totalEl.innerText = `$${total.toFixed(2)}`;
}

// Checkout Logic
async function checkout() {
    const token = localStorage.getItem('access_token');
    if (!token) {
        alert("Please login first!");
        return;
    }

    const orderData = {
        items: cart.map(item => ({ product_id: item.id, quantity: item.quantity }))
    };

    const response = await fetch(`${API_URL}/orders`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify(orderData)
    });

    if (response.ok) {
        alert("Order placed successfully!");
        cart = [];
        updateCartUI();
    } else {
        alert("Failed to place order.");
    }
}