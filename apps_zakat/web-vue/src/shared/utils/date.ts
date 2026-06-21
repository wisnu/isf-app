// Format tanggal ISO 'YYYY-MM-DD' → tampilan 'DD-MM-YYYY'.
export function dmy(v?: string | null): string {
  if (!v) return ''
  const m = /^(\d{4})-(\d{2})-(\d{2})/.exec(v)
  return m ? `${m[3]}-${m[2]}-${m[1]}` : v
}

// Format datetime ISO → tampilan 'DD-MM-YYYY HH:MM'. Konversi ke waktu lokal.
export function dmyt(v?: string | null): string {
  if (!v) return ''
  const d = new Date(v)
  if (isNaN(d.getTime())) return dmy(v)
  const dd = String(d.getDate()).padStart(2, '0')
  const mm = String(d.getMonth() + 1).padStart(2, '0')
  const yyyy = d.getFullYear()
  const hh = String(d.getHours()).padStart(2, '0')
  const min = String(d.getMinutes()).padStart(2, '0')
  return `${dd}-${mm}-${yyyy} ${hh}:${min}`
}
