export function formatIdr(n: number): string {
  return new Intl.NumberFormat('id-ID', {
    style: 'currency',
    currency: 'IDR',
    maximumFractionDigits: 0,
  }).format(n)
}

export function formatIdrShort(n: number): string {
  if (n >= 1e9) return 'Rp ' + (n / 1e9).toFixed(1) + ' M'
  if (n >= 1e6) return 'Rp ' + (n / 1e6).toFixed(0) + ' jt'
  if (n >= 1e3) return 'Rp ' + (n / 1e3).toFixed(0) + ' rb'
  return 'Rp ' + n
}

export function formatDate(input: string | Date): string {
  const d = typeof input === 'string' ? new Date(input) : input
  return new Intl.DateTimeFormat('id-ID', {
    day: '2-digit',
    month: 'short',
    year: 'numeric',
  }).format(d)
}

export function formatNumber(n: number): string {
  return new Intl.NumberFormat('id-ID').format(n)
}
