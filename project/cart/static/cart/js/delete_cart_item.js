document.addEventListener("DOMContentLoaded", () => {
    "use strict";

    const deleteCartItem = (url) => {
        fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': window.csrf,
            },
            mode: 'same-origin',
        })
            .then(response => response.json())
            .then(data => {
                location.reload()
            })
            .catch(error => console.error('Error delete from cart:', error));
    };

    const deleteFromCartButtons = document.querySelectorAll(".delete-from-cart");

    deleteFromCartButtons.forEach(deleteFromCartButton => {
        deleteFromCartButton.addEventListener("click", (e) => {
            const url = deleteFromCartButton.dataset.url;

            deleteCartItem(url);
        });
    });
});