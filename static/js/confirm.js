export function showConfirm(message, onConfirm) {

    const modal = document.getElementById("confirmModal");
    const overlay = document.getElementById("confirmOverlay");
    const messageEl = document.getElementById("confirmMessage");
    const cancelBtn = document.getElementById("confirmCancel");
    const acceptBtn = document.getElementById("confirmAccept");

    if (!modal) return;

    // Insertar mensaje dinámico
    messageEl.textContent = message;

    // Mostrar modal
    modal.classList.remove("hidden");
    modal.classList.add("flex");

    function closeModal() {
        modal.classList.add("hidden");
        modal.classList.remove("flex");

        // Limpiar listeners para evitar acumulación
        cancelBtn.removeEventListener("click", handleCancel);
        acceptBtn.removeEventListener("click", handleAccept);
        overlay.removeEventListener("click", handleCancel);
        document.removeEventListener("keydown", handleEscape);
    }

    function handleCancel() {
        closeModal();
    }

    function handleAccept() {
        closeModal();
        onConfirm();
    }

    function handleEscape(e) {
        if (e.key === "Escape") closeModal();
    }

    cancelBtn.addEventListener("click", handleCancel);
    acceptBtn.addEventListener("click", handleAccept);
    overlay.addEventListener("click", handleCancel);
    document.addEventListener("keydown", handleEscape);
}

