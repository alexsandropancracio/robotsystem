console.log("[NAVIGATION] Módulo carregado");

function getActiveView() {
    return document.querySelector(".view.active");
}

function resetView(view) {
    if (!view) return;

    // Dispara evento global de reset
    const event = new CustomEvent("view:reset", {
        detail: { viewId: view.id }
    });

    document.dispatchEvent(event);
    console.log(`[NAVIGATION] Reset solicitado para -> ${view.id}`);
}

function navigateTo(targetId) {
    const active = getActiveView();
    if (!active) return;

    // 🔥 RESET DA VIEW ATUAL
    resetView(active);

    document.querySelectorAll(".view").forEach(v =>
        v.classList.remove("active")
    );

    const target = document.getElementById(targetId);
    if (!target) return;

    target.classList.add("active");
    console.log(`[NAVIGATION] Navegou para -> ${targetId}`);
}

// Botões e links
document.addEventListener("click", ev => {
    const btnNav = ev.target.closest("[data-nav]");
    if (btnNav) {
        ev.preventDefault();
        navigateTo(btnNav.dataset.nav);
        return;
    }

    const btnAction = ev.target.closest("[data-action]");
    if (btnAction) {
        ev.preventDefault();
        if (btnAction.dataset.action === "logout") {
            // chama Python via PyWebview
            window.pywebview.api.logout().then(result => {
                console.log("[NAVIGATION] Logout feito:", result);
            });
        }
    }
});
