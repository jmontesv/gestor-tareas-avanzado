
// Obtener CSRF token para peticiones POST
export function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== "") {
        const cookies = document.cookie.split(";");
        for (let cookie of cookies) {
            cookie = cookie.trim();
            if (cookie.startsWith(name + "=")) {
                cookieValue = decodeURIComponent(
                    cookie.substring(name.length + 1)
                );
                break;
            }
        }
    }
    return cookieValue;
}

// Función genérica para hacer POST con JSON
export function postJSON(url, data) {
    return fetch(url, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": getCookie("csrftoken"),
        },
        body: JSON.stringify(data),
    });
}


/**
 * Devuelve el elemento después del cursor durante drag & drop
 * @param {HTMLElement} container Contenedor donde se hace el drag
 * @param {number} position Posición del mouse (clientX o clientY)
 * @param {string} axis "vertical" o "horizontal"
 * @param {string} selector Selector de los elementos arrastrables dentro del contenedor
 */
export function getDragAfterElement(container, position, axis = "vertical", selector = ".task:not(.dragging)") {
    const draggableElements = [...container.querySelectorAll(selector)];

    // Reduce para encontrar el elemento más cercano por debajo/derecha del cursor
    return draggableElements.reduce((closest, child) => {
        // Obtener el rectángulo del elemento
        const box = child.getBoundingClientRect();
        const offset = axis === "vertical"
            ? position - box.top - box.height / 2
            : position - box.left - box.width / 2;

        if (offset < 0 && offset > closest.offset) {
            return { offset, element: child };
        } else {
            return closest;
        }
    }, { offset: Number.NEGATIVE_INFINITY }).element;
}