// function goBack() {
//     window.location.href = "/home/";  // Redirect to the home page
// }

// function togglePassword(fieldId, eyeId) {
//     let passwordField = document.getElementById(fieldId);
//     let eyeIcon = document.getElementById(eyeId);
    
//     if (passwordField.type === "password") {
//         passwordField.type = "text";
//         eyeIcon.classList.remove("fa-eye");
//         eyeIcon.classList.add("fa-eye-slash");
//     } else {
//         passwordField.type = "password";
//         eyeIcon.classList.remove("fa-eye-slash");
//         eyeIcon.classList.add("fa-eye");
//     }
// }
function goBack() {
    window.location.href = "/home/";  
}

function togglePassword(fieldId, eyeId) {
    let passwordField = document.getElementById(fieldId);
    let eyeIcon = document.getElementById(eyeId);
    
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
