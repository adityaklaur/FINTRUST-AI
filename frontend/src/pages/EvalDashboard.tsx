import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query'

import { api } from '../api/client'
import type { EvalReport } from '../api/types'

const METRICS: { key: keyof EvalReport; label: string; gate?: number }[] = [
  { key: 'category_accuracy', label: 'Category accuracy', gate: 0.7 },
  { key: 'risk_accuracy', label: 'Risk accuracy' },
  { key: 'citation_coverage', label: 'Citation coverage' },
  { key: 'source_hit_rate', label: 'Source hit rate' },
  { key: 'refusal_accuracy', label: 'Refusal accuracy', gate: 1 },
  { key: 'disclaimer_coverage', label: 'Disclaimer coverage', gate: 1 },
]

export function EvalDashboard() {
  const qc = useQueryClient()
  const latest = useQuery<EvalReport | null>({
    queryKey: ['eval-latest'],
    queryFn: async () => {
      try {
        const { data } = await api.get<EvalReport>('/api/evaluation/latest')
        return data
      } catch {
        return null
      }
    },
  })

  const run = useMutation<EvalReport, Error>({
    mutationFn: async () => {
      const { data } = await api.post<EvalReport>('/api/evaluation/run')
      return data
    },
    onSuccess: (data) => qc.setQueryData(['eval-latest'], data),
  })

  const report = latest.data

  return (
    <div className="space-y-5">
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-lg font-semibold text-slate-800">Evaluation</h2>
          <p className="text-sm text-slate-500">
            Runs the golden question set through the full pipeline and scores quality.
          </p>
        </div>
        <button
          onClick={() => run.mutate()}
          disabled={run.isPending}
          className="rounded-lg bg-indigo-600 px-4 py-2 text-sm font-semibold text-white hover:bg-indigo-700 disabled:opacity-50"
        >
          {run.isPending ? 'Running…' : 'Run evaluation'}
        </button>
      </div>

      {run.isError && (
        <div className="rounded-lg border border-red-300 bg-red-50 px-4 py-3 text-sm text-red-700">
          Evaluation failed: {String(run.error?.message)}
        </div>
      )}

      {!report && !latest.isLoading && (
        <div className="rounded-xl border border-dashed border-slate-300 bg-white p-8 text-center text-sm text-slate-500">
          No evaluation has been run yet. Click “Run evaluation”.
        </div>
      )}

      {report && (
        <>
          <div className="grid grid-cols-2 gap-3 sm:grid-cols-3">
            {METRICS.map((m) => {
              const val = report[m.key] as number
              const pass = m.gate == null ? null : val >= m.gate
              return (
                <div key={m.key} className="rounded-xl border border-slate-200 bg-white p-4 shadow-sm">
                  <div className="text-xs font-medium uppercase tracking-wide text-slate-400">{m.label}</div>
                  <div className="mt-1 flex items-baseline gap-2">
                    <span className="text-2xl font-bold text-slate-800">{(val * 100).toFixed(1)}%</span>
                    {pass != null && (
                      <span className={pass ? 'text-sm text-emerald-600' : 'text-sm text-red-600'}>
                        {pass ? '✅' : '❌'}
                      </span>
                    )}
                  </div>
                  {m.gate != null && <div className="mt-0.5 text-[11px] text-slate-400">target ≥ {(m.gate * 100).toFixed(0)}%</div>}
                </div>
              )
            })}
          </div>

          <div className="rounded-xl border border-slate-200 bg-white p-4 text-sm text-slate-600 shadow-sm">
            <div className="flex flex-wrap gap-x-6 gap-y-1">
              <span>Total questions: <b>{report.total}</b></span>
              <span>Provider: <b>{report.provider}</b></span>
              <span>Model: <b>{report.model_name}</b></span>
              <span>
                Failures:{' '}
                <b>{report.failed_questions.length ? report.failed_questions.join(', ') : 'none 🎉'}</b>
              </span>
            </div>
            {report.generated_at && (
              <div className="mt-1 text-xs text-slate-400">generated {report.generated_at}</div>
            )}
          </div>
        </>
      )}
    </div>
  )
}
