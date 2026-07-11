import { useState } from 'react'

import type { Citation } from '../api/types'

const AUTH: Record<string, string> = {
  RBI: 'bg-blue-100 text-blue-700',
  NPCI: 'bg-emerald-100 text-emerald-700',
  BANK: 'bg-purple-100 text-purple-700',
  IRDAI: 'bg-orange-100 text-orange-700',
  DICGC: 'bg-teal-100 text-teal-700',
  RESEARCH: 'bg-slate-100 text-slate-600',
}

export function CitationCard({ c, index }: { c: Citation; index: number }) {
  const [open, setOpen] = useState(false)
  const authCls = AUTH[c.authority] ?? 'bg-slate-100 text-slate-600'
  const quote = c.quote ?? ''
  const isLong = quote.length > 220
  const shown = open || !isLong ? quote : quote.slice(0, 220) + '…'

  return (
    <div className="rounded-lg border border-slate-200 bg-white p-3 text-sm shadow-sm">
      <div className="flex items-center justify-between gap-2">
        <div className="flex min-w-0 items-center gap-2">
          <span className="font-mono text-xs text-slate-400">[{index}]</span>
          {c.authority && (
            <span className={`rounded px-1.5 py-0.5 text-[10px] font-bold uppercase ${authCls}`}>
              {c.authority}
            </span>
          )}
          <span className="truncate font-medium text-slate-800">{c.source_title || c.source_file}</span>
        </div>
        {c.source_url && (
          <a
            href={c.source_url}
            target="_blank"
            rel="noreferrer"
            className="shrink-0 text-xs text-indigo-600 hover:underline"
          >
            source ↗
          </a>
        )}
      </div>
      {c.section_title && <div className="mt-1 text-xs text-slate-500">§ {c.section_title}</div>}
      {quote && (
        <p className="mt-2 whitespace-pre-wrap text-slate-600">
          “{shown}”
          {isLong && (
            <button onClick={() => setOpen(!open)} className="ml-1 text-xs text-indigo-600 hover:underline">
              {open ? 'less' : 'more'}
            </button>
          )}
        </p>
      )}
      <div className="mt-2 truncate font-mono text-[11px] text-slate-400">{c.source_file}</div>
    </div>
  )
}
