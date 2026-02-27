import { initTaskModals } from "./modal.js";
import { initDragTasks } from "./dragTasks.js";
import { initDragColumns } from "./dragColumns.js";

document.addEventListener("DOMContentLoaded", () => {
    initTaskModals();
    initDragTasks();
    initDragColumns();
});