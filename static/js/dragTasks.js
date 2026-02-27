import { postJSON, getDragAfterElement } from "./utils.js";

export function initDragTasks() {

    let draggedTask = null;
    let originTasklist = null;

    document.querySelectorAll(".task").forEach(task => {

        task.addEventListener("dragstart", () => {
            draggedTask = task;
            originTasklist = task.closest(".tasklist-body");
            task.classList.add(
                "opacity-60",
                "scale-105",
                "shadow-xl",
                "bg-blue-50",
                "border",
                "border-blue-300"
            );
        });

        task.addEventListener("dragend", () => {
            task.classList.remove(
                "opacity-60",
                "scale-105",
                "shadow-xl",
                "bg-blue-50",
                "border",
                "border-blue-300"
            );

            const currentTasklist = task.closest(".tasklist-body");

            // Si quedó en la misma columna o se movió → llamamos a moveTask
            if (draggedTask) {
                const taskId = task.dataset.taskId;
                const tasklistId = currentTasklist.closest(".tasklist").dataset.tasklistId;

                // Preparamos el payload con el orden de todas las tareas de la columna
                const tasks = [...currentTasklist.querySelectorAll(".task")];
                const order = tasks.map((t, index) => ({
                    id: t.dataset.taskId,
                    order: index
                }));

            // POST a move_task que ahora también hace reorder
            postJSON(`/tasks/${taskId}/move/`, {
                tasklist_id: tasklistId,
                order: order
            }).then(res => res.json())
              .then(data => {
                  if (!data.success) console.error("Error al mover/reordenar tarea");
              });
            };
        });
    });

    document.querySelectorAll(".tasklist-body").forEach(container => {

        container.addEventListener("dragover", e => {
            e.preventDefault();
            const afterElement = getDragAfterElement(container, e.clientY);
            if (!afterElement) {
                container.appendChild(draggedTask);
            } else {
                container.insertBefore(draggedTask, afterElement);
            }
        });

        container.addEventListener("dragenter", () => container.classList.add("bg-blue-50"));
        container.addEventListener("dragleave", () => container.classList.remove("bg-blue-50"));

        container.addEventListener("drop", async () => {
            if (!draggedTask) return;
            container.classList.remove("bg-blue-50");

            const currentTasklist = container.closest(".tasklist");
            const taskId = draggedTask.dataset.taskId;
            const tasklistId = currentTasklist.dataset.tasklistId;

            const tasks = [...container.querySelectorAll(".task")];
            const payload = tasks.map((task, index) => ({
                id: task.dataset.taskId,
                order: index
            }));

            postJSON(`/tasks/${taskId}/move/`, {
                tasklist_id: tasklistId,
                order: payload
            });
        });
    });
}
