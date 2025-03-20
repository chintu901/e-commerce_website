document.addEventListener("DOMContentLoaded", function () {
    const navbar = document.getElementById("main_top_navbar_div_space");
    const parentDiv = document.querySelector(".product_left_featuring_area_New_Arrivals");
    const childDiv = document.querySelector(".product_left_featuring_area_New_Arrivals_box");

    const navbarHeight = navbar.offsetHeight;
    const gap = 5; // 1px gap between navbar and child

    window.addEventListener("scroll", function () {
        const scrollY = window.scrollY;
        const parentTop = parentDiv.offsetTop;
        const parentBottom = parentTop + parentDiv.offsetHeight;
        const childHeight = childDiv.offsetHeight;

        let newTop = scrollY - parentTop + navbarHeight + gap; 

        if (newTop <= 0) {
            // Keep child at the top
            newTop = 0;
        } else if (newTop + childHeight >= parentDiv.offsetHeight) {
            // Keep child inside parent
            newTop = parentDiv.offsetHeight - childHeight;
        }

        // Apply smooth movement
        childDiv.style.position = "absolute";
        childDiv.style.top = newTop + "px";
    });
});
