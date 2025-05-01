document.addEventListener("DOMContentLoaded", function () {
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== "") {
            const cookies = document.cookie.split(";");
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === name + "=") {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    let historyPage = 1;
    let currentQuery = "";
    const chatBox = document.getElementById("chat-box");
    const userInput = document.getElementById("user-input");
    const sendBtn = document.getElementById("send-btn");
    const speakBtn = document.getElementById("speak-btn");
    const languageButtons = document.querySelectorAll(".language-btn");
    let selectedLanguage = "hi";


    let username = localStorage.getItem("username");

    if (!username) {
        username = prompt("Please enter your name:");
        if (username) {
            localStorage.setItem("username", username);
        } else {
            username = "User"; // Default fallback
        }
    }

    // Update Welcome Text
    const welcomeText = document.getElementById("welcome-text");
    if (welcomeText) {
        welcomeText.innerText = `Welcome, ${username}!`;
    }


    // Check if language was saved earlier
    if (localStorage.getItem("selectedLanguage")) {
        selectedLanguage = localStorage.getItem("selectedLanguage");


    function setLanguage(lang) {
        selectedLanguage = lang;
        localStorage.setItem("selectedLanguage", lang);
        alert("Language set to " + (lang === "hi" ? "Hindi" : "English"));

}

    }

    function appendMessage(sender, message) {
        const messageDiv = document.createElement("div");
        messageDiv.classList.add("message", sender + "-message");
        if (sender === "bot") {
            // Typing animation
            let index = 0;
            const typingInterval = setInterval(() => {
                messageDiv.innerText += message[index];
                index++;
                if (index >= message.length) {
                    clearInterval(typingInterval);
                }
                chatBox.scrollTop = chatBox.scrollHeight;
            }, 50); // typing speed (lower is faster)
        } else {
            messageDiv.innerText = message;
        }
        chatBox.appendChild(messageDiv);
        chatBox.scrollTop = chatBox.scrollHeight;
    }
    

    function sendMessage() {
        const message = userInput.value.trim();
        if (message === "") return;
    
        appendMessage("user", message);
        userInput.value = "";
    
        // Show "Bot is typing..." temporary message
        const typingMessage = document.createElement("div");
        typingMessage.classList.add("message", "bot-message");
        typingMessage.id = "typing";
        typingMessage.innerText = "Bot is typing...";
        chatBox.appendChild(typingMessage);
        chatBox.scrollTop = chatBox.scrollHeight;
    
        setTimeout(() => {
            // Simulating server response after small delay
            chatBox.removeChild(typingMessage);
    
            // Now fetch actual bot response
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
        }, 1000); // Delay to simulate typing
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

    userInput.addEventListener("keydown", function (event) {
        if (event.key === "Enter" && !event.shiftKey) {
            event.preventDefault(); // Stop from creating a new line
            sendMessage();          // Send the message
        }
    });

    function toggleDarkMode() {
        document.body.classList.toggle("dark-mode");
        localStorage.setItem("darkMode", document.body.classList.contains("dark-mode"));
    }
    
    // Keep dark mode if it was active
    if (localStorage.getItem("darkMode") === "true") {
        document.body.classList.add("dark-mode");
    }
    
    const profileBtn = document.getElementById('profileBtn');
    const profileDropdown = document.getElementById('profileDropdown');

    profileBtn.addEventListener('click', () => {
        profileDropdown.classList.toggle('show');
    });
    
    // Hide dropdown if clicked outside
    document.addEventListener('click', function (event) {
        if (event.target.classList.contains("replay-message")) {
            const msg = event.target.innerText;
            userInput.value = msg;
            sendMessage();
        }
    }); 
    
    document.querySelectorAll('.profile-dropdown a').forEach(link => {
        link.addEventListener('click', function(event) {
            if (this.textContent.trim() === "Logout") {
                event.preventDefault();
                if (confirm("Are you sure you want to logout?")) {
                    // Redirect or handle logout here
                    alert("You have been logged out successfully!");
                    // window.location.href = '/logout'; // If you have a real logout page
                }
            }
        });
    });
    
    fetch("/chatbot/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": getCookie("csrftoken")
        },
        body: JSON.stringify({ message: message, language: selectedLanguage })
    })
    .then(response => response.json())
    .then(data => {
        chatBox.removeChild(typingMessage);
        appendMessage("bot", data.response);
        speakText(data.response);
    })
    .catch(error => {
        chatBox.removeChild(typingMessage);
        appendMessage("bot", "Error: Could not connect to chatbot.");
    });
    function loadHistory(reset = true) {
        if (reset) {
            historyPage = 1;
            currentQuery = document.getElementById("search-history").value;
            document.getElementById("chat-history").innerHTML = "";
        }
    
        fetch(`/history/?q=${encodeURIComponent(currentQuery)}&page=${historyPage}`)
            .then(res => res.json())
            .then(data => {
                const historyBox = document.getElementById("chat-history");
                const loadMoreBtn = document.getElementById("load-more-btn");
    
                data.history.forEach(item => {
                    const div = document.createElement("div");
                    div.innerHTML = `<b>🧑 You:</b> <span class="replay-message" style="cursor:pointer;color:#007bff" title="Click to resend">${item.question}</span><br>
                                     <b>🤖 Bot:</b> ${item.answer}<br>
                                     <small>${new Date(item.time).toLocaleString()}</small>`;
                    historyBox.appendChild(div);
                });
    
                if (data.has_more) {
                    loadMoreBtn.style.display = "inline-block";
                } else {
                    loadMoreBtn.style.display = "none";
                }
            });
    }
    
    function loadMoreHistory() {
        historyPage++;
        loadHistory(false); // load next page
    }
    
});
