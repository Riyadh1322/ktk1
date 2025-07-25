document.addEventListener('DOMContentLoaded', () => {
    console.log('Website loaded successfully!');

    // Example: Add interactivity for modal pop-ups or other features
    const carousel = document.querySelector('#productCarousel');
    if (carousel) {
        console.log('Carousel is ready!');
    }

    // Add to Cart functionality
    document.querySelectorAll('.add-to-cart').forEach(button => {
        button.addEventListener('click', (event) => {
            const productId = event.target.getAttribute('data-product-id');
            console.log(`Product ${productId} added to cart.`);
            alert(`Product ${productId} added to cart.`);
        });
    });
});