// Label portal dinamis dari VITE_PORTAL_DOMAIN (diset per-portal di compose:
// zakat → "Portal Zakat", wakaf → "Portal Wakaf"). Hindari hardcode.
const DOMAIN = ((import.meta.env.VITE_PORTAL_DOMAIN as string | undefined) ?? '').toLowerCase()

const LABELS: Record<string, string> = {
  zakat: 'Portal Zakat',
  wakaf: 'Portal Wakaf',
}

export const portalDomain = DOMAIN
export const portalLabel = LABELS[DOMAIN] ?? 'Portal'
