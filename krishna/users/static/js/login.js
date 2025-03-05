// Function to validate login credentials
function validateLogin() {
    let email = document.getElementById("email").value;
    let password = document.getElementById("password").value;

    if (email === "" || password === "") {
        alert("Please fill in all fields before logging in.");
        return;
    }

    // Example check (In real application, use backend validation)
    if (email === "test@gmail.com" && password === "1234") {
        alert("Login Successful! Redirecting...");
        window.location.href = "index.html"; // Redirect to home page
    } else {
        alert("Invalid credentials. Please try again.");
    }
}

// Function to close login popup
function closeLogin() {
    document.getElementById("loginPopup").style.display = "none";
}

// Function to toggle password visibility
function togglePassword() {
    let passwordField = document.getElementById("password");
    let eyeIcon = document.getElementById("eyeIcon");

    if (passwordField.type === "password") {
        passwordField.type = "text";
        eyeIcon.classList.remove("fa-eye");
        eyeIcon.classList.add("fa-eye-slash");
    } else {
        passwordField.type = "password";
        eyeIcon.classList.remove("fa-eye-slash");
        eyeIcon.classList.add("fa-eye");
    }
}
