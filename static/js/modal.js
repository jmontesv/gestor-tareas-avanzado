import { getCookie } from "./utils.js";
import { showConfirm } from "./confirm.js";

export function initTaskModals() {
    const modal = document.getElementById("taskModal");
    const modalContent = document.getElementById("taskModalContent");
    const overlay = document.getElementById("taskModalOverlay");
    const closeBtn = document.getElementById("closeTaskModal");

    function openModal() {
        modal.classList.remove("hidden");
        document.body.classList.add("overflow-hidden");
    }

    function closeModal() {
        modal.classList.add("hidden");
        modalContent.innerHTML = "";
        document.body.classList.remove("overflow-hidden");
    }

    closeBtn?.addEventListener("click", closeModal);
    overlay?.addEventListener("click", closeModal);
    document.addEventListener("keydown", e => { if(e.key === "Escape") closeModal(); });

    // Abrir modal para crear tarea
    document.querySelectorAll(".open-task-modal").forEach(btn => {
        btn.addEventListener("click", e => {
            e.preventDefault();
            const tasklistId = btn.dataset.tasklistId;

            openModal();
            modalContent.innerHTML = "Cargando…";

            fetch(`/tasklist/${tasklistId}/task/create/`)
                .then(res => res.json())
                .then(data => modalContent.innerHTML = data.html);
        });
    });

    // Abrir modal para editar tarea
    document.querySelectorAll(".task").forEach(task => {
        task.addEventListener("click", () => {
            const taskId = task.dataset.taskId;

            openModal();
            modalContent.innerHTML = "Cargando…";

            fetch(`/tasks/${taskId}/update/`)
                .then(res => res.json())
                .then(data => modalContent.innerHTML = data.html);
        });
    });

    // Eliminar tarea con confirmación
    document.addEventListener("click", e => {
        if (e.target.matches("#deleteTaskBtn")) {
            const taskId = e.target.dataset.taskId;

            showConfirm("¿Eliminar esta tarea? Esta acción no se puede deshacer.", () => {
                fetch(`/tasks/${taskId}/delete/`, {
                    method: "POST",
                    headers: { "X-CSRFToken": getCookie("csrftoken") }
                })
                .then(res => res.json())
                .then(data => {
                    if (data.success) {
                        const taskEl = document.querySelector(`.task[data-task-id="${taskId}"]`);
                        if (taskEl) {
                            taskEl.style.transition = "opacity 0.3s ease, transform 0.3s ease";
                            taskEl.style.opacity = "0";
                            taskEl.style.transform = "translateY(-10px)";
                            setTimeout(() => taskEl.remove(), 300);
                        }
                        closeModal();
                    }
                });
            });
        }
    });

    // Delegación submit del formulario dentro del modal
    modalContent.addEventListener("submit", e => {
        if (!e.target.matches("#taskForm")) return;

        e.preventDefault();
        fetch(e.target.action, {
            method: "POST",
            body: new FormData(e.target),
            headers: { "X-Requested-With": "XMLHttpRequest" }
        })
        .then(res => res.json())
        .then(data => {
            if (data.success) {
                closeModal();
                location.reload();
            } else {
                modalContent.innerHTML = data.html;
            }
        });
    });
}
