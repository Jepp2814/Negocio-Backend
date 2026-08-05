console.log("Dashboard cargado");

const userMenuButton = document.getElementById("userMenuButton");
const userDropdownMenu = document.getElementById("userDropdownMenu");

if (userMenuButton && userDropdownMenu) {
    userMenuButton.addEventListener("click", function () {
        userDropdownMenu.classList.toggle("show");

        const isOpen = userDropdownMenu.classList.contains("show");
        userMenuButton.setAttribute("aria-expanded", isOpen);
    });

    document.addEventListener("click", function (event) {
        const clickedInsideMenu =
            userMenuButton.contains(event.target) ||
            userDropdownMenu.contains(event.target);

        if (!clickedInsideMenu) {
            userDropdownMenu.classList.remove("show");
            userMenuButton.setAttribute("aria-expanded", "false");
        }
    });
}