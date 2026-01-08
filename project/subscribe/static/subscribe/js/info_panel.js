document.addEventListener("DOMContentLoaded", () => {
    "use strict";


    const websocketProtocol = location.protocol === "https:" ? "wss" : "ws";
    const wsEndpoint = `${websocketProtocol}://${location.host}/ws/info-panel/`;
    const socket = new WebSocket(wsEndpoint);

    // Event listener to capture incoming message
    socket.addEventListener("message", (e) => {
        const messageData = JSON.parse(e.data);

        const infoPanel = document.querySelector("#info-panel");

        infoPanel.innerHTML += messageData.message;
    });
});