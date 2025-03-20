document.addEventListener("DOMContentLoaded", function () {
    const navbar = document.getElementById("main_top_navbar_div_space");
    const parentDiv = document.querySelector(".product_right_featuring_area_New_Arrivals_second");
    const childDiv = document.querySelector(".product_right_featuring_area_New_Arrivals_box_second");

    const navbarHeight = navbar.offsetHeight;
    const gap = 1; // 3px gap between navbar and child

    window.addEventListener("scroll", function () {
        const scrollY = window.scrollY;
        const parentTop = parentDiv.offsetTop;
        const parentBottom = parentTop + parentDiv.offsetHeight;
        const childHeight = childDiv.offsetHeight;

        const maxTop = parentBottom - childHeight; // Max scroll limit for child

        if (scrollY + navbarHeight >= parentTop - gap) {
            let newTop = scrollY - parentTop + navbarHeight + gap; 

            if (newTop + childHeight >= parentDiv.offsetHeight) {
                // Stop at the bottom smoothly
                newTop = parentDiv.offsetHeight - childHeight;
            }

            // Apply smooth movement
            childDiv.style.transform = `translateY(${newTop}px)`;
        } else {
            // Reset to initial position
            childDiv.style.transform = "translateY(0px)";
        }
    });
});
