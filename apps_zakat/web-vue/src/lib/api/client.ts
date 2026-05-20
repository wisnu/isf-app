function resolveBaseUrl(): string {
  const explicit = (import.meta.env.VITE_API_BASE_URL as string | undefined)?.trim()
  if (explicit) return explicit
  if (typeof window !== 'undefined') {
    const port = (import.meta.env.VITE_BFF_PORT as string | undefined) ?? '7000'
    return `${window.location.protocol}//${window.location.hostname}:${port}`
  }
  return 'http://localhost:7000'
}

export const BASE_URL = resolveBaseUrl()

export class ApiError extends Error {
  constructor(public code: string, message: string, public status: number) {
    super(message)
  }
}

async function request<T>(method: string, path: string, body?: unknown): Promise<T> {
  const response = await fetch(`${BASE_URL}${path}`, {
    method,
    credentials: 'include',
    headers: { 'Content-Type': 'application/json' },
    body: body !== undefined ? JSON.stringify(body) : undefined,
  })
  const payload = await response.json().catch(() => ({} as Record<string, unknown>))
  if (!response.ok) {
    const errorPayload = (payload as { error?: { code?: string; message?: string } }).error
    const code = errorPayload?.code ?? 'UNKNOWN_ERROR'
    const message = errorPayload?.message ?? response.statusText
    throw new ApiError(code, message, response.status)
  }
  return (payload as { data: T }).data
}

async function downloadBlob(path: string, suggestedFilename: string): Promise<void> {
  const response = await fetch(`${BASE_URL}${path}`, { credentials: 'include' })
  if (!response.ok) {
    let code = `HTTP_${response.status}`
    let message = response.statusText
    try {
      const j = await response.json()
      code = j?.error?.code ?? code
      message = j?.error?.message ?? message
    } catch {
      // not JSON
    }
    throw new ApiError(code, message, response.status)
  }
  // Prefer filename dari Content-Disposition kalau ada
  const disp = response.headers.get('Content-Disposition') ?? ''
  const match = /filename\s*=\s*"?([^";]+)"?/i.exec(disp)
  const filename = match?.[1] ?? suggestedFilename

  const blob = await response.blob()
  const url = URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url
  a.download = filename
  document.body.appendChild(a)
  a.click()
  document.body.removeChild(a)
  URL.revokeObjectURL(url)
}

export const api = {
  get: <T>(path: string) => request<T>('GET', path),
  post: <T>(path: string, body?: unknown) => request<T>('POST', path, body),
  downloadBlob,
}
