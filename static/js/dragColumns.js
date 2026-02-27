import { postJSON, getDragAfterElement } from "./utils.js";

export function initDragColumns() {

    let draggedColumn = null;
    const tasklistsContainer = document.getElementById("tasklistsContainer");

    if (!tasklistsContainer) return;

    document.querySelectorAll(".tasklist").forEach(column => {

        column.setAttribute("draggable", true);

        column.addEventListener("dragstart", () => {
            draggedColumn = column;
            column.classList.add("opacity-60", "scale-105");
        });

        column.addEventListener("dragend", () => {
            column.classList.remove("opacity-60", "scale-105");
            updateTasklistOrder();
            draggedColumn = null;
        });
    });

    // Dragover en el contenedor principal para permitir soltar columnas
    tasklistsContainer.addEventListener("dragover", e => {
        e.preventDefault();
        const afterElement = getDragAfterElement(tasklistsContainer, e.clientX, "horizontal", ".tasklist:not(.dragging)");

        if (!afterElement) {
            tasklistsContainer.appendChild(draggedColumn);
        } else {
            tasklistsContainer.insertBefore(draggedColumn, afterElement);
        }
    });

    function updateTasklistOrder() {
        const columns = [...document.querySelectorAll(".tasklist")];
        const payload = columns.map((col, index) => ({
            id: col.dataset.tasklistId,
            order: index
        }));

        postJSON("/tasklist/reorder/", payload)
            .then(res => res.json())
            .then(data => console.log(data));
    }
}
