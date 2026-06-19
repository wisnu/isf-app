export interface ApprovalLogEntry {
  level: number
  authorizer_id: string
  status: 'APPROVED' | 'REJECTED'
  notes: string | null
  logged_at: string
}

export type SubmissionStatus = 'DRAFT' | 'PENDING' | 'PROCESSING' | 'AUTHORIZED' | 'REJECTED'

export interface SubmissionRow {
  id: number
  entity_type: string
  entity_label: string
  branch_code: string
  payload: Record<string, unknown>
  status: SubmissionStatus
  level_current: number
  level_required: number
  submitted_by: string
  submitted_at: string | null
  approval_log: ApprovalLogEntry[]
  dispatch_error?: string | null
}
