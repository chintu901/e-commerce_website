document.addEventListener("DOMContentLoaded", function () {
    const navbar = document.getElementById("main_top_navbar_div_space");
    const parentDiv = document.querySelector(".product_left_featuring_area_New_Arrivals");
    const childDiv = document.querySelector(".product_left_featuring_area_New_Arrivals_box");

    const navbarHeight = navbar.offsetHeight;
    const gap = 3; // 5px gap between navbar and child box

    window.addEventListener("scroll", function () {
        const scrollY = window.scrollY;
        const parentTop = parentDiv.offsetTop;
        const parentBottom = parentTop + parentDiv.offsetHeight;
        const childHeight = childDiv.offsetHeight;

        const maxTop = parentBottom - childHeight; // Max scroll limit for child

        if (scrollY + navbarHeight >= parentTop - gap) {
            let newTop = scrollY - parentTop + navbarHeight + gap; // Add the 5px gap

            if (newTop + childHeight >= parentDiv.offsetHeight) {
                // Stop at the bottom of the parent
                childDiv.style.position = "absolute";
                childDiv.style.top = (parentDiv.offsetHeight - childHeight) + "px";
            } else {
                // Move the child box down with scrolling
                childDiv.style.position = "absolute";
                childDiv.style.top = newTop + "px";
            }
        } else {
            // Reset when scrolling back up
            childDiv.style.position = "absolute";
            childDiv.style.top = "0px"; // Reset to initial position
        }
    });
});
