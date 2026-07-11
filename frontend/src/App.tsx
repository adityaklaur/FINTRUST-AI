import { useState } from 'react'

import { AuthButton } from './components/AuthButton'
import { AuditHistory } from './pages/AuditHistory'
import { EvalDashboard } from './pages/EvalDashboard'
import { Home } from './pages/Home'
import { Roadmap } from './pages/Roadmap'
import { SourceExplorer } from './pages/SourceExplorer'

type Tab = 'home' | 'audit' | 'sources' | 'eval' | 'roadmap'

const TABS: { id: Tab; label: string }[] = [
  { id: 'home', label: 'Assistant' },
  { id: 'audit', label: 'Audit History' },
  { id: 'sources', label: 'Source Explorer' },
  { id: 'eval', label: 'Evaluation' },
  { id: 'roadmap', label: 'Roadmap' },
]

export default function App() {
  const [tab, setTab] = useState<Tab>('home')

  return (
    <div className="min-h-full bg-slate-50">
      <header className="border-b border-slate-200 bg-white">
        <div className="mx-auto max-w-6xl px-4 py-4">
          <div className="flex items-center justify-between gap-3">
            <div className="flex items-center gap-3">
              <div className="flex h-9 w-9 items-center justify-center rounded-lg bg-indigo-600 font-bold text-white">
                F
              </div>
              <div>
                <h1 className="text-lg font-bold leading-tight text-slate-900">FinTrust AI</h1>
                <p className="text-xs text-slate-500">Source-grounded financial services copilot</p>
              </div>
            </div>
            <AuthButton />
          </div>
          <nav className="mt-4 flex gap-1">
            {TABS.map((t) => (
              <button
                key={t.id}
                onClick={() => setTab(t.id)}
                className={`rounded-md px-3 py-1.5 text-sm font-medium transition ${
                  tab === t.id
                    ? 'bg-indigo-50 text-indigo-700'
                    : 'text-slate-500 hover:bg-slate-100 hover:text-slate-700'
                }`}
              >
                {t.label}
              </button>
            ))}
          </nav>
        </div>
      </header>

      <main className="mx-auto max-w-6xl px-4 py-6">
        {tab === 'home' && <Home />}
        {tab === 'audit' && <AuditHistory />}
        {tab === 'sources' && <SourceExplorer />}
        {tab === 'eval' && <EvalDashboard />}
        {tab === 'roadmap' && <Roadmap />}
      </main>

      <footer className="mx-auto max-w-6xl px-4 py-6 text-center text-xs text-slate-400">
        Not legal or financial advice. Answers are grounded in public regulatory &amp; bank documents and always cite sources.
      </footer>
    </div>
  )
}
