document.getElementById("sendBtn").addEventListener("click", sendMessage);
document.getElementById("userInput").addEventListener("keypress", function (event) {
    if (event.key === "Enter") {
        sendMessage();
    }
});

function sendMessage() {
    const userInput = document.getElementById("userInput").value.trim();
    if (userInput === "") return;

    appendMessage(userInput, "user-message", "static/User.jpg");
    document.getElementById("userInput").value = "";

    fetch("/get", {
        method: "POST",
        headers: {
            "Content-Type": "application/x-www-form-urlencoded"
        },
        body: "msg=" + encodeURIComponent(userInput)
    })
    .then(response => response.json())
    .then(data => {
        appendMessage(data.response, "bot-message", "static/logo.jpg");
    });
}

function appendMessage(message, className, icon) {
    const chatbox = document.getElementById("chatbox");
    const messageDiv = document.createElement("div");
    messageDiv.className = `message ${className}`;

    const iconImg = document.createElement("img");
    iconImg.src = icon;
    iconImg.alt = className.includes("bot") ? "Bot" : "User";
    iconImg.className = "speaker-icon";

    const textDiv = document.createElement("div");
    textDiv.textContent = message;
    textDiv.className = "text";

    messageDiv.appendChild(iconImg);
    messageDiv.appendChild(textDiv);
    chatbox.appendChild(messageDiv);
    chatbox.scrollTop = chatbox.scrollHeight;
}
