document.addEventListener("DOMContentLoaded", function () {
    const navbar = document.getElementById("main_top_navbar_div_space");
    const parentDiv = document.querySelector(".product_left_featuring_area_New_Arrivals");
    const childDiv = document.querySelector(".product_left_featuring_area_New_Arrivals_box");

    if (!navbar || !parentDiv || !childDiv) return; // Prevent errors if elements are missing

    const navbarHeight = navbar.offsetHeight;
    const gap = 5; // Space between navbar and child
    let ticking = false; // For requestAnimationFrame optimization

    parentDiv.style.position = "relative"; // Ensure parent is relative for absolute positioning

    function updateChildPosition() {
        const scrollY = window.scrollY;
        const parentTop = parentDiv.offsetTop;
        const parentBottom = parentTop + parentDiv.offsetHeight;
        const childHeight = childDiv.offsetHeight;

        let newTop = scrollY - parentTop + navbarHeight + gap;

        // Prevent child from moving outside parent
        if (newTop < 0) {
            newTop = 0;
        } else if (newTop + childHeight > parentDiv.offsetHeight) {
            newTop = parentDiv.offsetHeight - childHeight;
        }

        childDiv.style.position = "absolute";
        childDiv.style.top = newTop + "px";

        ticking = false; // Reset flag after execution
    }

    window.addEventListener("scroll", function () {
        if (!ticking) {
            requestAnimationFrame(updateChildPosition);
            ticking = true;
        }
    });
});
