document.addEventListener("DOMContentLoaded", function () {
    document.querySelector(".button-pushable").addEventListener("click", function () {
        let username = document.getElementById("username_input_box").value.trim();
        if (username === "") {
            alert("Please enter your username.");
            return;
        }

        // Hide Step 1
        document.getElementById("step1").style.display = "none";

        // Show Step 2 with Fade-in Effect
        let step2 = document.getElementById("step2");
        step2.style.display = "block";
        setTimeout(() => {
            step2.style.opacity = "1";
        }, 10);
    });
});
