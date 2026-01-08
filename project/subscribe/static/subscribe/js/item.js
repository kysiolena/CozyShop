document.addEventListener("DOMContentLoaded", () => {
    "use strict";

    const subscribeItem = (url) => {
        fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': window.csrf,
            },
            mode: 'same-origin',
        })
            // .then(response => response.json())
            // .then(data => {
            //     location.reload()
            // })
            // .catch(error => console.error('Error subscribe product:', error))
            .finally(() => location.reload());
    };

    const unsubscribeItem = (url) => {
        fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': window.csrf,
            },
            mode: 'same-origin',
        })
            // .then(response => response.json())
            // .then(data => {
            //     location.reload()
            // })
            // .catch(error => console.error('Error unsubscribe product:', error))
            .finally(() => {
                if (location.href.includes("profile")) {
                    const url = new URL(location.href);
                    url.searchParams.delete("page");

                    location.replace(url.href);
                } else {
                    location.reload();
                }
            });
    };

    const subscribeButtons = document.querySelectorAll(".subscribe-product");

    subscribeButtons.forEach(subscribeButton => {
        subscribeButton.addEventListener("click", (e) => {
            const url = subscribeButton.dataset.url;

            subscribeButton.textContent = "Subscribing...";
            subscribeButton.disabled = true;

            subscribeItem(url);
        });
    });

    const unsubscribeButtons = document.querySelectorAll(".unsubscribe-product");

    unsubscribeButtons.forEach(unsubscribeButton => {
        unsubscribeButton.addEventListener("click", (e) => {
            const url = unsubscribeButton.dataset.url;

            unsubscribeButton.textContent = "Unsubscribing...";
            unsubscribeButton.disabled = true;

            unsubscribeItem(url);
        });
    });
});