// ui/progress.js
console.log("[PROGRESS] Módulo progress carregado");

// 🔥 Estas funções ficam globais (acessíveis pelo PyWebView)
window.atualizarProgressoXML = pct => updateProgress("#xml_converter", pct, ".progress-fill-xml", ".progress-percent");
window.atualizarProgressoSeparator = pct => updateProgress("#progress-separator", pct, ".progress-fill-separator", ".progress-percent");
window.atualizarProgressoRename = pct => updateProgress("#rename", pct, ".progress-fill-rename", ".progress-percent");

// 📌 Função interna para atualizar o estilo da barra
function updateProgress(containerId, pct, barSelector = ".progress-fill-xml", percentSelector = ".progress-percent") {
    setTimeout(() => {
        try {
            const container = document.querySelector(containerId);
            if (!container) return;
            const bar = container.querySelector(barSelector);
            const percent = container.querySelector(percentSelector);
            if (bar) bar.style.width = pct + "%";
            if (percent) percent.textContent = pct + "%";
            console.log(`[PROGRESS] ${containerId} atualizado: ${pct}%`);
        } catch (err) {
            console.error("[ERRO UPDATE PROGRESS]", err);
        }
    }, 50);
}

export function resetProgressBars() {
    try {
        document.querySelectorAll(".progress-fill-xml, .progress-fill-separator, .progress-fill-rename")
            .forEach(bar => bar.style.width = "0%");
        document.querySelectorAll(".progress-percent").forEach(text => text.textContent = "0%");
        console.log("[PROGRESS] Barras resetadas");
    } catch (err) {
        console.error("[ERRO RESET PROGRESS]", err);
    }
}

document.addEventListener("view:reset", ev => {
    const { viewId } = ev.detail;

    // views que usam progresso
    const viewsWithProgress = ["xml_converter", "rename", "progress-separator"];

    if (!viewsWithProgress.includes(viewId)) return;

    resetProgressBars();
    console.log(`[PROGRESS] Reset aplicado na view -> ${viewId}`);
});
