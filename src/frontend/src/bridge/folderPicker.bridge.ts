type FolderPickerCallback = (inputId: string, path: string) => void;

let callback: FolderPickerCallback | null = null;

export function registerFolderPickerCallback(
  fn: FolderPickerCallback
) {
  callback = fn;
}

// 🔥 função chamada pelo Python
window.onPastaSelecionada = function (
  inputId: string,
  path: string
) {
  console.log("[PYWEBVIEW] Pasta selecionada:", inputId, path);

  if (callback) {
    callback(inputId, path);
  }
};
