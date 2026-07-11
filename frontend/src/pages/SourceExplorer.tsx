import { useQuery } from '@tanstack/react-query'
import { useState } from 'react'

import { api } from '../api/client'
import type { SourceDoc } from '../api/types'

const AUTH_CLS: Record<string, string> = {
  RBI: 'bg-blue-100 text-blue-700',
  NPCI: 'bg-emerald-100 text-emerald-700',
  BANK: 'bg-purple-100 text-purple-700',
  IRDAI: 'bg-orange-100 text-orange-700',
  DICGC: 'bg-teal-100 text-teal-700',
  SACHET: 'bg-pink-100 text-pink-700',
  RESEARCH: 'bg-slate-100 text-slate-600',
}

export function SourceExplorer() {
  const [domain, setDomain] = useState('')
  const [authority, setAuthority] = useState('')

  const { data, isLoading, isError } = useQuery<SourceDoc[]>({
    queryKey: ['sources', domain, authority],
    queryFn: async () => {
      const { data } = await api.get<SourceDoc[]>('/api/sources', {
        params: { domain: domain || undefined, authority: authority || undefined },
      })
      return data
    },
  })

  const ingested = data?.filter((d) => d.ingestion_status === 'ingested').length ?? 0

  return (
    <div className="space-y-4">
      <div className="flex flex-wrap items-end gap-3">
        <div>
          <label className="mb-1 block text-xs font-medium text-slate-500">Domain</label>
          <select value={domain} onChange={(e) => setDomain(e.target.value)} className="rounded-lg border border-slate-300 p-2 text-sm">
            <option value="">All domains</option>
            <option value="banking_payments">banking_payments</option>
            <option value="insurance">insurance</option>
            <option value="research_reference">research_reference</option>
            <option value="dataset">dataset</option>
          </select>
        </div>
        <div>
          <label className="mb-1 block text-xs font-medium text-slate-500">Authority</label>
          <select value={authority} onChange={(e) => setAuthority(e.target.value)} className="rounded-lg border border-slate-300 p-2 text-sm">
            <option value="">All authorities</option>
            {['RBI', 'NPCI', 'BANK', 'IRDAI', 'DICGC', 'SACHET', 'RESEARCH'].map((a) => (
              <option key={a} value={a}>
                {a}
              </option>
            ))}
          </select>
        </div>
        <span className="ml-auto text-sm text-slate-400">
          {data?.length ?? 0} sources · {ingested} ingested
        </span>
      </div>

      {isLoading && <div className="text-sm text-slate-500">Loading…</div>}
      {isError && <div className="text-sm text-red-600">Failed to load sources.</div>}

      {data && (
        <div className="overflow-x-auto rounded-xl border border-slate-200 bg-white shadow-sm">
          <table className="w-full text-left text-sm">
            <thead className="border-b border-slate-200 bg-slate-50 text-xs uppercase tracking-wide text-slate-500">
              <tr>
                <th className="px-4 py-2">Title</th>
                <th className="px-4 py-2">Domain</th>
                <th className="px-4 py-2">Authority</th>
                <th className="px-4 py-2">Institution</th>
                <th className="px-4 py-2">Status</th>
              </tr>
            </thead>
            <tbody>
              {data.map((s) => (
                <tr key={s.source_id} className="border-b border-slate-100 hover:bg-slate-50">
                  <td className="max-w-md px-4 py-2 text-slate-700">
                    <div className="truncate font-medium">{s.title || s.file_path.split('/').pop()}</div>
                    <div className="truncate font-mono text-[11px] text-slate-400">{s.file_path}</div>
                  </td>
                  <td className="px-4 py-2 text-xs text-slate-600">{s.domain}</td>
                  <td className="px-4 py-2">
                    <span className={`rounded px-1.5 py-0.5 text-[10px] font-bold uppercase ${AUTH_CLS[s.authority] ?? 'bg-slate-100 text-slate-600'}`}>
                      {s.authority}
                    </span>
                  </td>
                  <td className="px-4 py-2 text-xs text-slate-600">{s.institution}</td>
                  <td className="px-4 py-2">
                    <span
                      className={`rounded-full px-2 py-0.5 text-xs font-medium ${
                        s.ingestion_status === 'ingested'
                          ? 'bg-emerald-100 text-emerald-700'
                          : 'bg-slate-100 text-slate-500'
                      }`}
                    >
                      {s.ingestion_status}
                    </span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  )
}
