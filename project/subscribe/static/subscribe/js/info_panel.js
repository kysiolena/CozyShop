document.addEventListener("DOMContentLoaded", () => {
    "use strict";

    const infoPanel = document.querySelector("#info-panel");

    const websocketProtocol = location.protocol === "https:" ? "wss" : "ws";
    const wsEndpoint = `${websocketProtocol}://${location.host}/ws/info-panel/`;
    const socket = new WebSocket(wsEndpoint);

    // Event listener to capture incoming message
    socket.addEventListener("message", (e) => {
        // Get HTML alert
        const data = JSON.parse(e.data);

        // Create container for HTML alert
        const divEl = document.createElement("div");

        // Place HTML to container
        divEl.innerHTML = data.message;

        if (infoPanel) {
            // Add container with alert to Info Panel
            infoPanel.appendChild(divEl);

            // Hide container
            setTimeout(() => {
                divEl.classList.add("fade");
            }, 5000);

            // Delete container
            setTimeout(() => {
                infoPanel.removeChild(divEl);
            }, 5200);
        }
    });
});