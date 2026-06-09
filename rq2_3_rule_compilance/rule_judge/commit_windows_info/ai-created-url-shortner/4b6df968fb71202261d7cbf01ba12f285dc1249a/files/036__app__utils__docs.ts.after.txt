export function openReadme(path: string) {
  const win = window.open(`/__open-in-editor?file=${path}`, "_blank");
  setTimeout(() => win?.close(), 1);
}
