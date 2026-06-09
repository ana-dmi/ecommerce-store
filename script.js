// Shopping Cart functionality
let cart = [];

// Add to Cart button handlers
document.querySelectorAll('.add-btn').forEach(button => {
    button.addEventListener('click', function(e) {
        e.preventDefault();

        const productCard = this.closest('.product-card');
        const productName = productCard.querySelector('h3').textContent;
        const productPrice = productCard.querySelector('.price').textContent;

        // Add to cart
        cart.push({
            name: productName,
            price: productPrice,
            id: Date.now()
        });

        // Show feedback
        this.textContent = '✓ Added!';
        this.style.backgroundColor = '#27AE60';

        setTimeout(() => {
            this.textContent = 'Add to Cart';
            this.style.backgroundColor = '';
        }, 1500);

        updateCartCount();
    });
});

// Update cart count in navbar
function updateCartCount() {
    const cartBtn = document.querySelector('.cart-btn');
    if (cart.length > 0) {
        cartBtn.textContent = `🛒 Cart (${cart.length})`;
    } else {
        cartBtn.textContent = '🛒 Cart';
    }
}

// Scroll animations
const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.style.opacity = '1';
            entry.target.style.transform = 'translateY(0)';
        }
    });
});

// Observe product cards
document.querySelectorAll('.product-card').forEach(card => {
    card.style.opacity = '0';
    card.style.transform = 'translateY(20px)';
    card.style.transition = 'all 0.6s ease';
    observer.observe(card);
});

// Smooth scroll for navigation links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    });
});

// Cart button functionality
document.querySelector('.cart-btn').addEventListener('click', function(e) {
    if (this.textContent.includes('Cart (')) {
        e.preventDefault();
        showCartModal();
    }
});

// Show cart modal
function showCartModal() {
    if (cart.length === 0) {
        alert('Your cart is empty. Add some coffee!');
        return;
    }

    let total = 0;
    let cartSummary = 'Your Cart:\n\n';

    cart.forEach((item, index) => {
        const price = parseFloat(item.price.replace('£', ''));
        total += price;
        cartSummary += `${index + 1}. ${item.name} - ${item.price}\n`;
    });

    cartSummary += `\n─────────\nTotal: £${total.toFixed(2)}\n\nProceeding to checkout...`;
    alert(cartSummary);
}

// Page load animations
window.addEventListener('load', function() {
    document.body.style.opacity = '0';
    document.body.style.animation = 'fadeIn 0.8s ease forwards';
});

// Add fade-in animation
const style = document.createElement('style');
style.textContent = `
    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }
`;
document.head.appendChild(style);

// Log when page loads
console.log('☕ Welcome to Brew Coffee Shop!');
console.log('Explore our premium collection of beans, capsules, and iced coffee.');
console.log(`Currently ${cart.length} items in cart.`);
