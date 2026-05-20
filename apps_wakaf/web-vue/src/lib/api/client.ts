const BASE_URL = import.meta.env.VITE_API_BASE_URL ?? 'http://localhost:7000'

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

export const api = {
  get: <T>(path: string) => request<T>('GET', path),
  post: <T>(path: string, body?: unknown) => request<T>('POST', path, body),
}
