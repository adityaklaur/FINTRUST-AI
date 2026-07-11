import type { ReactNode } from 'react'

import { AnswerPanel } from '../components/AnswerPanel'
import { CategoryBadge } from '../components/CategoryBadge'
import { CitationCard } from '../components/CitationCard'
import { DisclaimerBanner } from '../components/DisclaimerBanner'
import { EscalationRoute } from '../components/EscalationRoute'
import { EvidenceChecklist } from '../components/EvidenceChecklist'
import { QueryPanel, type AskParams } from '../components/QueryPanel'
import { RiskBadge } from '../components/RiskBadge'
import { useAskQuery } from '../hooks/useAskQuery'

function Section({ title, children }: { title: string; children: ReactNode }) {
  return (
    <section className="space-y-2">
      <h3 className="text-xs font-semibold uppercase tracking-wide text-slate-400">{title}</h3>
      {children}
    </section>
  )
}

function Skeleton() {
  return (
    <div className="space-y-3">
      <div className="h-6 w-40 animate-pulse rounded bg-slate-200" />
      <div className="h-32 animate-pulse rounded-xl bg-slate-200" />
      <div className="h-16 animate-pulse rounded-xl bg-slate-200" />
    </div>
  )
}

function EmptyState() {
  return (
    <div className="flex h-full min-h-64 flex-col items-center justify-center rounded-xl border border-dashed border-slate-300 bg-white p-8 text-center">
      <div className="text-3xl">🛈</div>
      <p className="mt-2 max-w-sm text-sm text-slate-500">
        Ask a banking or payments question. You&apos;ll get a source-grounded answer with a category,
        risk level, evidence checklist, escalation route, and citations.
      </p>
    </div>
  )
}

export function Home() {
  const ask = useAskQuery()
  const data = ask.data
  const onSubmit = (p: AskParams) =>
    ask.mutate({ question: p.question, domain: p.domain, institution: p.institution, include_debug: true })
  const answerBody = data ? data.answer.replace(data.disclaimer, '').trim() : ''

  return (
    <div className="grid gap-6 md:grid-cols-5">
      <div className="md:col-span-2">
        <div className="rounded-xl border border-slate-200 bg-white p-5 shadow-sm">
          <QueryPanel onSubmit={onSubmit} loading={ask.isPending} />
        </div>
      </div>

      <div className="md:col-span-3">
        {ask.isPending && <Skeleton />}
        {ask.isError && (
          <div className="rounded-lg border border-red-300 bg-red-50 px-4 py-3 text-sm text-red-700">
            Request failed: {String(ask.error?.message)}. Is the backend running on port 8000?
          </div>
        )}
        {!ask.isPending && !data && <EmptyState />}

        {data && !ask.isPending && (
          <div className="space-y-5">
            <div className="flex flex-wrap items-center gap-2">
              <CategoryBadge label={data.category_label || data.category} />
              <RiskBadge risk={data.risk_level} />
              {data.low_confidence && (
                <span className="rounded-full bg-yellow-100 px-2 py-0.5 text-xs font-medium text-yellow-700">
                  low confidence
                </span>
              )}
              <span className="ml-auto text-xs text-slate-400">
                {data.model_name} · {data.latency_ms} ms
              </span>
            </div>

            {data.is_unsupported && (
              <div className="rounded-lg border border-slate-200 bg-slate-50 px-3 py-2 text-sm text-slate-600">
                This request was declined or lacked sufficient source support.
              </div>
            )}

            <div className="rounded-xl border border-slate-200 bg-white p-5 shadow-sm">
              <AnswerPanel answer={answerBody} />
            </div>

            <DisclaimerBanner text={data.disclaimer} />

            {data.evidence_checklist.length > 0 && (
              <Section title="Evidence to collect">
                <div className="rounded-xl border border-slate-200 bg-white p-4 shadow-sm">
                  <EvidenceChecklist items={data.evidence_checklist} />
                </div>
              </Section>
            )}

            {data.escalation_route.length > 0 && (
              <Section title="Escalation route">
                <EscalationRoute steps={data.escalation_route} />
              </Section>
            )}

            {data.citations.length > 0 && (
              <Section title={`Citations (${data.citations.length})`}>
                <div className="space-y-2">
                  {data.citations.map((c, i) => (
                    <CitationCard key={c.chunk_id + i} c={c} index={i + 1} />
                  ))}
                </div>
              </Section>
            )}

            {data.retrieved_chunks && data.retrieved_chunks.length > 0 && (
              <details className="rounded-xl border border-slate-200 bg-white p-4 text-sm shadow-sm">
                <summary className="cursor-pointer font-medium text-slate-600">
                  Retrieved chunks (debug · {data.retrieved_chunks.length})
                </summary>
                <div className="mt-3 space-y-2">
                  {data.retrieved_chunks.map((ch) => (
                    <div key={ch.chunk_id} className="rounded border border-slate-100 bg-slate-50 p-2">
                      <div className="flex justify-between gap-2 text-xs text-slate-500">
                        <span className="truncate">
                          {ch.authority} · {ch.title || ch.source_file}
                        </span>
                        <span className="shrink-0 font-mono">score {ch.score.toFixed(3)}</span>
                      </div>
                      <p className="mt-1 text-slate-600">{ch.text.slice(0, 240)}…</p>
                    </div>
                  ))}
                </div>
              </details>
            )}
          </div>
        )}
      </div>
    </div>
  )
}
