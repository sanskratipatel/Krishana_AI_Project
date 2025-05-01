// Load User Data
function loadUserData() {
    fetch("/user-data/")
        .then(response => response.json())
        .then(data => {
            document.getElementById("username").textContent = data.username;
        });
}
loadUserData();

// Fetch Chat History
function loadChatHistory() {
    fetch("/chat-history/")
        .then(response => response.json())
        .then(data => {
            let history = document.getElementById("chatHistory");
            history.innerHTML = "";
            data.messages.forEach(msg => {
                history.innerHTML += `<p><b>You:</b> ${msg.user_message} <br> <b>Bot:</b> ${msg.bot_response}</p>`;
            });
        });
}
loadChatHistory();

// Send Message
function sendMessage() {
    let userInput = document.getElementById("userInput").value;
    fetch("/chatbot/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: userInput })
    })
    .then(response => response.json())
    .then(data => {
        loadChatHistory();
        speak(data.response);  // Speak the bot response
    });
}

// Voice Recognition
function startVoiceRecognition() {
    let recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
    recognition.lang = "hi-IN"; // Default Hindi
    recognition.start();

    recognition.onresult = function(event) {
        document.getElementById("userInput").value = event.results[0][0].transcript;
        sendMessage();
    };
}

// Text-to-Speech (Voice Reply)
function speak(text) {
    let utterance = new SpeechSynthesisUtterance(text);
    utterance.lang = "hi-IN"; // Default Hindi
    window.speechSynthesis.speak(utterance);
}

// Language Switching
function setLanguage(lang) {
    document.documentElement.lang = lang;
}
