export function downloadBlob(blob: Blob, filename: string): void {
  const objectUrl = URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = objectUrl
  a.download = filename || 'download'
  a.rel = 'noopener'
  document.body.appendChild(a)
  a.click()
  // Tunda cleanup: revoke blob URL secara sinkron tepat setelah click membuat
  // Chrome kehilangan nama download (jatuh ke UUID blob URL). Beri jeda.
  setTimeout(() => {
    document.body.removeChild(a)
    URL.revokeObjectURL(objectUrl)
  }, 1000)
}
