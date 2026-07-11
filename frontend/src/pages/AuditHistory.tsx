import { Fragment, useState } from 'react'

import { RiskBadge } from '../components/RiskBadge'
import { useAudit } from '../hooks/useAudit'

const CATEGORIES = [
  '',
  'credit_card_grievance',
  'upi_failed_transaction',
  'unauthorized_transaction',
  'failed_transaction_tat',
  'ombudsman_escalation',
  'loan_complaint',
  'unsupported_or_advice_request',
]
const RISKS = ['', 'high', 'medium', 'low', 'not_applicable']

function fmt(ts: string) {
  const d = new Date(ts.endsWith('Z') ? ts : ts + 'Z')
  return Number.isNaN(d.getTime()) ? ts : d.toLocaleString()
}

export function AuditHistory() {
  const [category, setCategory] = useState('')
  const [risk, setRisk] = useState('')
  const [open, setOpen] = useState<string | null>(null)
  const { data, isLoading, isError } = useAudit({ category, risk, limit: 100 })

  return (
    <div className="space-y-4">
      <div className="flex flex-wrap items-end gap-3">
        <div>
          <label className="mb-1 block text-xs font-medium text-slate-500">Category</label>
          <select
            value={category}
            onChange={(e) => setCategory(e.target.value)}
            className="rounded-lg border border-slate-300 p-2 text-sm"
          >
            {CATEGORIES.map((c) => (
              <option key={c} value={c}>
                {c || 'All categories'}
              </option>
            ))}
          </select>
        </div>
        <div>
          <label className="mb-1 block text-xs font-medium text-slate-500">Risk</label>
          <select
            value={risk}
            onChange={(e) => setRisk(e.target.value)}
            className="rounded-lg border border-slate-300 p-2 text-sm"
          >
            {RISKS.map((r) => (
              <option key={r} value={r}>
                {r || 'All risk levels'}
              </option>
            ))}
          </select>
        </div>
        <span className="ml-auto text-sm text-slate-400">{data?.length ?? 0} queries</span>
      </div>

      {isLoading && <div className="text-sm text-slate-500">Loading…</div>}
      {isError && <div className="text-sm text-red-600">Failed to load audit log.</div>}

      {data && (
        <div className="overflow-x-auto rounded-xl border border-slate-200 bg-white shadow-sm">
          <table className="w-full text-left text-sm">
            <thead className="border-b border-slate-200 bg-slate-50 text-xs uppercase tracking-wide text-slate-500">
              <tr>
                <th className="px-4 py-2">Time</th>
                <th className="px-4 py-2">Question</th>
                <th className="px-4 py-2">Category</th>
                <th className="px-4 py-2">Risk</th>
                <th className="px-4 py-2">Cites</th>
                <th className="px-4 py-2">Latency</th>
              </tr>
            </thead>
            <tbody>
              {data.map((a) => (
                <Fragment key={a.audit_id}>
                  <tr
                    onClick={() => setOpen(open === a.audit_id ? null : a.audit_id)}
                    className="cursor-pointer border-b border-slate-100 hover:bg-slate-50"
                  >
                    <td className="whitespace-nowrap px-4 py-2 text-xs text-slate-500">{fmt(a.timestamp)}</td>
                    <td className="max-w-xs truncate px-4 py-2 text-slate-700">{a.question}</td>
                    <td className="px-4 py-2 text-xs text-slate-600">{a.category}</td>
                    <td className="px-4 py-2">
                      <RiskBadge risk={a.risk_level} />
                    </td>
                    <td className="px-4 py-2 text-slate-600">{a.citation_count}</td>
                    <td className="px-4 py-2 text-xs text-slate-500">{a.latency_ms} ms</td>
                  </tr>
                  {open === a.audit_id && (
                    <tr className="border-b border-slate-100 bg-slate-50/60">
                      <td colSpan={6} className="px-4 py-3 text-sm text-slate-600">
                        <div className="mb-1 font-medium text-slate-700">{a.question}</div>
                        <p>{a.answer_preview}…</p>
                        <div className="mt-2 text-xs text-slate-400">
                          model {a.model_name} · {a.source_ids_used.length} source(s) ·{' '}
                          {a.is_unsupported ? 'refused/unsupported' : 'answered'}
                        </div>
                      </td>
                    </tr>
                  )}
                </Fragment>
              ))}
              {data.length === 0 && (
                <tr>
                  <td colSpan={6} className="px-4 py-6 text-center text-sm text-slate-400">
                    No queries logged yet.
                  </td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      )}
    </div>
  )
}
