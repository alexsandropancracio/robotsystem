export type ProgressEventName =
  | "xml-progress"
  | "rename-progress"
  | "separator-progress";

if (!window.atualizarProgresso) {
  window.atualizarProgresso = function (
    eventName: ProgressEventName,
    percent: number
  ) {
    console.log(`[PROGRESS] ${eventName}: ${percent}%`);

    window.dispatchEvent(
      new CustomEvent(eventName, {
        detail: percent,
      })
    );
  };
}
