document.getElementById("login-form").addEventListener("submit", function () {
    const btn = document.getElementById("login-button");
    btn.disabled = true;
    btn.textContent = "Logging in...";
});