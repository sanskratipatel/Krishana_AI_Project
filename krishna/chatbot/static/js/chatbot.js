document.addEventListener("DOMContentLoaded", function () {
    const chatBox = document.getElementById("chat-box");
    const userInput = document.getElementById("user-input");
    const sendBtn = document.getElementById("send-btn");
    const speakBtn = document.getElementById("speak-btn");
    const languageButtons = document.querySelectorAll(".language-btn");
    let selectedLanguage = "hi";

    languageButtons.forEach(button => {
        button.addEventListener("click", function () {
            setLanguage(this.getAttribute("data-lang"));
        });
    });

    function setLanguage(lang) {
        alert("Language set to " + (lang === "hi" ? "Hindi" : "English"));
    }

    function appendMessage(sender, message) {
        const messageDiv = document.createElement("div");
        messageDiv.classList.add("message", sender + "-message");
        messageDiv.innerText = message;
        chatBox.appendChild(messageDiv);
        chatBox.scrollTop = chatBox.scrollHeight;
    }

    function sendMessage() {
        const message = userInput.value.trim();
        if (message === "") return;

        appendMessage("user", message);
        userInput.value = "";

        fetch("/bot/chatbot/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ message: message }),
        })
        .then(response => response.json())
        .then(data => {
            appendMessage("bot", data.response);
            speakText(data.response); // Speak bot response
        })
        .catch(error => {
            appendMessage("bot", "Error: Could not connect to chatbot.");
        });
    }

    function speakText(text) {
        const speech = new SpeechSynthesisUtterance();
        speech.text = text;
        speech.lang = selectedLanguage === "hi" ? "hi-IN" : "en-US";
        window.speechSynthesis.speak(speech);
    }

    function startVoiceRecognition() {
        const recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
        recognition.lang = selectedLanguage === "hi" ? "hi-IN" : "en-US";
        recognition.start();

        recognition.onresult = function (event) {
            userInput.value = event.results[0][0].transcript;
            sendMessage();
        };
    }

    languageButtons.forEach(button => {
        button.addEventListener("click", function () {
            selectedLanguage = this.dataset.lang;
            alert("Language set to " + (selectedLanguage === "hi" ? "Hindi" : "English"));
        });
    });

    sendBtn.addEventListener("click", sendMessage);
    speakBtn.addEventListener("click", startVoiceRecognition);
});
