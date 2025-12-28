document.addEventListener('DOMContentLoaded', () => {
    "use strict";

    const createOrder = (url, data) => {
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
            .then(data => {
                if (data.status === "success") {
                    location.replace(data.message);
                } else {
                    location.reload();
                }
            })
            .catch(() => location.reload());
        // .finally(() => location.reload());
    };

    const updateContent = (pm, wrapper) => {
        if (wrapper) {
            // Clean wrapper
            wrapper.innerHTML = "";

            const content = document.querySelector(`#pm-${pm}-template`)?.content;

            if (content) {
                wrapper.appendChild(document.importNode(content, true));
            }
        }
    };

    // Current payment method: card, paypal, etc.
    let pm = null;

    const paymentMethodRadioElements = document.querySelectorAll("input[name='payment_method']");
    const paymentMethodContentWrapper = document.querySelector("#pm-content");

    paymentMethodRadioElements.forEach(radioElement => {
        if (radioElement.checked) {
            pm = radioElement.value;

            updateContent(pm, paymentMethodContentWrapper);
        }

        radioElement.addEventListener("change", () => {
            pm = radioElement.value;

            updateContent(pm, paymentMethodContentWrapper);
        });
    });

    const createOrderButton = document.querySelector("#create-order-button");

    if (createOrderButton) {
        createOrderButton.addEventListener('click', (e) => {
            e.preventDefault();

            // Get order create url
            const url = createOrderButton.dataset.url;

            // Get related form element
            const form = document.querySelector("#pm-content form");

            let formData;

            if (url && form) {
                formData = new FormData(form);
            } else {
                // No form
                formData = new FormData();
            }

            if (formData instanceof FormData) {
                // Add payment method
                formData.append("pm", pm);

                const data = Object.fromEntries(formData.entries());

                // Create order request
                createOrder(url, data);
            }
        });
    }
});