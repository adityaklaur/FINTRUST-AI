const MAP: Record<string, { cls: string; tip: string }> = {
  high: { cls: 'bg-red-100 text-red-700 ring-red-600/20', tip: 'High risk — act quickly (fraud, money stuck, deceased claim).' },
  medium: { cls: 'bg-amber-100 text-amber-700 ring-amber-600/20', tip: 'Medium risk — a grievance worth escalating if unresolved.' },
  low: { cls: 'bg-emerald-100 text-emerald-700 ring-emerald-600/20', tip: 'Low risk — informational or a standard process.' },
  not_applicable: { cls: 'bg-slate-100 text-slate-500 ring-slate-500/20', tip: 'Not applicable (advice / unsupported request).' },
  pending: { cls: 'bg-slate-100 text-slate-400 ring-slate-400/20', tip: 'Not yet classified.' },
}

export function RiskBadge({ risk }: { risk: string }) {
  const m = MAP[risk] ?? MAP.pending
  const label = risk === 'not_applicable' ? 'N/A' : risk
  return (
    <span
      title={m.tip}
      className={`inline-flex items-center gap-1 rounded-full px-2.5 py-1 text-xs font-semibold uppercase tracking-wide ring-1 ring-inset ${m.cls}`}
    >
      ● {label}
    </span>
  )
}
