// Honest roadmap surface. Status is explicit — nothing here pretends to work.
//   live    = shipped & verified
//   soon    = actively planned / next up (NOT clickable anywhere yet)
//   planned = future / vision

type Status = 'live' | 'soon' | 'planned'

interface Item {
  title: string
  detail: string
  status: Status
}

const ITEMS: Item[] = [
  // --- Live today ---
  { status: 'live', title: 'Source-grounded answers + citations', detail: 'Every answer is assembled from retrieved RBI/NPCI/bank passages and cites them.' },
  { status: 'live', title: 'Issue classification + risk level', detail: '16 categories with a deterministic risk label (fraud / stuck money = high).' },
  { status: 'live', title: 'Escalation route + evidence checklist', detail: 'Who to contact, in what order, and what documents to gather.' },
  { status: 'live', title: 'Refusal on unsupported / advice questions', detail: 'No financial advice, no answers without source support.' },
  { status: 'live', title: 'Audit log of every query', detail: 'Question, category, risk, sources, model, latency — reviewable.' },
  { status: 'live', title: 'Evaluation dashboard', detail: 'Golden question set scored for category / refusal / citation quality.' },
  { status: 'live', title: 'Runs fully offline (no API key)', detail: 'Extractive, cited answers with zero third-party calls.' },

  // --- Coming soon (next) ---
  { status: 'live', title: 'Fluent AI answers (optional)', detail: 'Groq / Gemini with automatic failover to offline mode — add a free key to enable.' },
  { status: 'live', title: 'Live document updates', detail: 'Detects new RBI notifications via RSS and refreshes the knowledge base (manual/API today) — no retraining.' },
  { status: 'soon', title: 'Sign in + your own history', detail: 'Magic-link accounts so your past queries are saved privately to you (enable via Supabase).' },
  { status: 'soon', title: 'Public cloud deployment', detail: 'A shareable link anyone can open (Render + Vercel configs are ready).' },
  { status: 'soon', title: 'Bigger knowledge base', detail: 'KYC, insurance, and more banks (already collected, being ingested).' },
  { status: 'soon', title: 'Scheduled auto-refresh', detail: 'A daily job that checks the RBI feed and re-embeds new documents automatically.' },
  { status: 'soon', title: 'Answer feedback', detail: 'Rate an answer 👍/👎 to help the system improve.' },

  // --- Planned (vision) ---
  { status: 'planned', title: 'Insurance module', detail: 'IRDAI / Bima Bharosa / Insurance Ombudsman workflows as a separate index.' },
  { status: 'planned', title: 'Enterprise / multi-bank', detail: 'Per-institution corpora, admin dashboard, roles.' },
  { status: 'planned', title: 'Government API enrichment', detail: 'Verified reference data via API Setu / data.gov.in.' },
  { status: 'planned', title: 'Streaming + conversation memory', detail: 'Faster, more natural multi-turn interactions.' },
]

const BADGE: Record<Status, { label: string; cls: string }> = {
  live: { label: 'Live', cls: 'bg-emerald-100 text-emerald-700 ring-emerald-600/20' },
  soon: { label: 'Coming soon', cls: 'bg-amber-100 text-amber-700 ring-amber-600/20' },
  planned: { label: 'Planned', cls: 'bg-slate-100 text-slate-500 ring-slate-500/20' },
}

const COLUMNS: { status: Status; heading: string; blurb: string }[] = [
  { status: 'live', heading: 'Available now', blurb: 'Shipped and verified in this build.' },
  { status: 'soon', heading: 'Coming soon', blurb: 'Actively planned — not yet available.' },
  { status: 'planned', heading: 'Later', blurb: 'On the longer-term roadmap.' },
]

export function Roadmap() {
  return (
    <div className="space-y-5">
      <div>
        <h2 className="text-lg font-semibold text-slate-800">Roadmap</h2>
        <p className="text-sm text-slate-500">
          An honest view of what works today and what&apos;s next. Items marked{' '}
          <span className="font-medium text-amber-700">Coming soon</span> /{' '}
          <span className="font-medium text-slate-500">Planned</span> are not clickable yet — we don&apos;t show controls that don&apos;t work.
        </p>
      </div>

      <div className="grid gap-4 md:grid-cols-3">
        {COLUMNS.map((col) => (
          <div key={col.status} className="space-y-3">
            <div>
              <h3 className="text-sm font-semibold text-slate-700">{col.heading}</h3>
              <p className="text-xs text-slate-400">{col.blurb}</p>
            </div>
            {ITEMS.filter((i) => i.status === col.status).map((i) => (
              <div key={i.title} className="rounded-xl border border-slate-200 bg-white p-3 shadow-sm">
                <div className="mb-1 flex items-start justify-between gap-2">
                  <span className="text-sm font-medium text-slate-800">{i.title}</span>
                  <span
                    className={`shrink-0 rounded-full px-2 py-0.5 text-[10px] font-semibold uppercase tracking-wide ring-1 ring-inset ${BADGE[i.status].cls}`}
                  >
                    {BADGE[i.status].label}
                  </span>
                </div>
                <p className="text-xs text-slate-500">{i.detail}</p>
              </div>
            ))}
          </div>
        ))}
      </div>
    </div>
  )
}
