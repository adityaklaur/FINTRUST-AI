// Mirrors the backend Pydantic schemas (app/schemas/*).

export interface Citation {
  chunk_id: string
  source_title: string
  source_file: string
  source_url: string
  section_title: string
  authority: string
  quote: string
}

export interface RetrievedChunk {
  chunk_id: string
  source_id: string
  text: string
  score: number
  section_title: string
  source_file: string
  source_url: string
  title: string
  authority: string
  institution: string
  domain: string
}

export interface QueryRequest {
  question: string
  domain?: string | null
  institution?: string | null
  top_k?: number
  include_debug?: boolean
}

export interface QueryResponse {
  answer: string
  category: string
  category_label: string
  risk_level: string
  escalation_route: string[]
  evidence_checklist: string[]
  citations: Citation[]
  is_unsupported: boolean
  low_confidence: boolean
  disclaimer: string
  retrieved_chunks: RetrievedChunk[] | null
  model_name: string
  latency_ms: number
  audit_id: string | null
}

export interface AuditEntry {
  audit_id: string
  timestamp: string
  question: string
  domain: string | null
  institution: string | null
  category: string
  risk_level: string
  is_unsupported: boolean
  answer_preview: string
  citation_count: number
  source_ids_used: string[]
  model_name: string
  latency_ms: number
}

export interface SourceDoc {
  source_id: string
  file_path: string
  title: string
  source_url: string
  domain: string
  subdomain: string
  authority: string
  institution: string
  is_authoritative: boolean
  is_bank_specific: boolean
  is_insurance_only: boolean
  effective_year: number
  ingestion_status: string
  notes: string
}

export interface EvalReport {
  total: number
  category_accuracy: number
  risk_accuracy: number
  citation_coverage: number
  source_hit_rate: number
  refusal_accuracy: number
  disclaimer_coverage: number
  per_question: Record<string, unknown>[]
  failed_questions: string[]
  generated_at: string
  provider: string
  model_name: string
}
