document.addEventListener("DOMContentLoaded", function () {
    document.getElementById("register_button").addEventListener("click", function(event) {
        event.preventDefault();
        window.location.href = "/registration_page";
    });
});
