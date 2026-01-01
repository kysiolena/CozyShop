document.addEventListener("DOMContentLoaded", () => {
    "use strict";

    const addCartItem = (prodId, quantity) => {
        fetch(window.add_to_cart_url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': window.csrf,
            },
            mode: 'same-origin',
            body: JSON.stringify({
                product_id: +prodId,
                quantity: +quantity
            })
        })
            // .then(response => response.json())
            // .then(data => {
            //     location.reload()
            // })
            // .catch(error => console.error('Error add to cart:', error))
            .finally(() => location.reload());
    };

    const addToCartButtons = document.querySelectorAll(".add-to-cart");

    addToCartButtons.forEach(addToCartButton => {
        addToCartButton.addEventListener("click", (e) => {
            const prodId = addToCartButton.dataset.product;
            const prodQuantity = addToCartButton.dataset.quantity;

            addToCartButton.textContent = "Adding to cart...";
            addToCartButton.disabled = true;

            addCartItem(prodId, prodQuantity);
        });
    });
});