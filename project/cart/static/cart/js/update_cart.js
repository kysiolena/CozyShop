document.addEventListener("DOMContentLoaded", () => {
    "use strict";

    const updateCart = (url, data) => {
        fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': window.csrf,
            },
            mode: 'same-origin',
            body: JSON.stringify(data)
        })
            .then(response => response.json())
            .then(data => location.reload())
            .catch(error => console.error('Error update cart:', error));
    };

    const cleanCart = (url) => {
        fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': window.csrf,
            },
            mode: 'same-origin',
        })
            .then(response => response.json())
            .then(data => location.reload())
            .catch(error => console.error('Error clean cart:', error));
    };

    // Cart Items
    const quantityContainers = document.querySelectorAll(".quantity-container");

    quantityContainers.forEach(quantityContainer => {
        const minusButton = quantityContainer.querySelector(".quantity-minus");
        const plusButton = quantityContainer.querySelector(".quantity-plus");
        const input = quantityContainer.querySelector(".quantity-input");

        minusButton.addEventListener("click", (e) => {
            const val = +input.value;

            if (val > 1) {
                input.value = val - 1
            }
        });

        plusButton.addEventListener("click", (e) => {
            const val = +input.value;

            input.value = val + 1
        });

        input.addEventListener("input", (e) => {
            input.value = +e.target.value || 1
        });
    });

    // Update Button
    const updateButton = document.querySelector(".update-cart");

    if (updateButton) {
        const url = updateButton.dataset.url;

        updateButton.addEventListener("click", (e) => {
            const data = [];
            quantityContainers.forEach(quantityContainer => {
                const prodId = quantityContainer.dataset.product;
                const input = quantityContainer.querySelector(".quantity-input");

                data.push({
                    "product_id": +prodId,
                    "quantity": +input.value,
                })
            });


            updateCart(url, data);
        });
    }

    // Clean Button
    const cleanButton = document.querySelector(".clean-cart");

    if (cleanButton) {
        const url = cleanButton.dataset.url;
        
        cleanButton.addEventListener("click", (e) => {
            cleanCart(url);
        });
    }

});