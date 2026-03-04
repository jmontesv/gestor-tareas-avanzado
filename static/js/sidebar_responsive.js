const sidebar = document.getElementById("sidebar");
const toggleSidebarMobile = document.getElementById("toggleSidebarMobile");
const openSidebarMain = document.getElementById("openSidebar");
const menuTextElements = document.querySelectorAll(".menu-text");

function isMobile() {
    return window.innerWidth < 640;
}

function showSidebarMobile() {
    sidebar.classList.remove("-translate-x-full");
}

function hideSidebarMobile() {
    sidebar.classList.add("-translate-x-full");
}

function expandDesktop() {
    sidebar.classList.remove("w-20");
    sidebar.classList.add("w-64");
    // Pequeño retraso para evitar que el texto aparezca antes de que el sidebar se expanda
    setTimeout(() => {
        menuTextElements.forEach(el => el.classList.remove("hidden"));
    }, 200);
}

function collapseDesktop() {
    sidebar.classList.remove("w-64");
    sidebar.classList.add("w-20");
    menuTextElements.forEach(el => el.classList.add("hidden"));
}

// Botón para alternar el sidebar en móvil o colapsar/expandir en escritorio
toggleSidebarMobile.addEventListener("click", () => {
    if (isMobile()) {
        sidebar.classList.toggle("-translate-x-full");
    } else {
        if (sidebar.classList.contains("w-64")) {
            collapseDesktop();
        } else {
            expandDesktop();
        }
    }
});

// Botón para abrir el sidebar en móvil
openSidebarMain.addEventListener("click", () => {
    if (isMobile()) {
        showSidebarMobile();
    }
});

// Ajuste automático al redimensionar 
window.addEventListener("resize", () => {
    if (isMobile()) {
        sidebar.classList.remove("w-20", "w-64");
        sidebar.classList.add("w-full");
        menuTextElements.forEach(el => el.classList.remove("hidden"));
        sidebar.classList.add("-translate-x-full");
    } else {
        sidebar.classList.remove("w-full", "-translate-x-full");
        expandDesktop();
    }
});

// Estado principal al cargar la página
if (isMobile()) {
    sidebar.classList.add("w-full");
    hideSidebarMobile();
} else {
    expandDesktop();
}