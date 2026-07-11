import { useState } from 'react'

export interface AskParams {
  question: string
  domain: string
  institution: string | null
}

const BANKS = [
  { v: '', label: 'Any / not specified' },
  { v: 'hdfc', label: 'HDFC' },
  { v: 'icici', label: 'ICICI' },
  { v: 'axis', label: 'Axis' },
  { v: 'sbi', label: 'SBI' },
  { v: 'kotak', label: 'Kotak' },
  { v: 'idfc', label: 'IDFC FIRST' },
]

const SAMPLES = [
  'What happens if a credit card complaint is not resolved in 30 days?',
  'My UPI payment failed but money was debited. What should I do?',
  'There is an unauthorized transaction on my account. How do I report it?',
  'Should I invest in crypto?',
]

export function QueryPanel({ onSubmit, loading }: { onSubmit: (p: AskParams) => void; loading: boolean }) {
  const [question, setQuestion] = useState('')
  const [domain, setDomain] = useState('banking_payments')
  const [bank, setBank] = useState('')

  const submit = () => {
    if (!question.trim() || loading) return
    onSubmit({ question: question.trim(), domain, institution: bank || null })
  }

  return (
    <div className="space-y-4">
      <div>
        <label className="mb-1 block text-sm font-medium text-slate-700">Your question</label>
        <textarea
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          onKeyDown={(e) => {
            if ((e.metaKey || e.ctrlKey) && e.key === 'Enter') submit()
          }}
          rows={5}
          maxLength={500}
          placeholder="Ask a banking or payments question…"
          className="w-full resize-none rounded-lg border border-slate-300 p-3 text-sm shadow-sm outline-none focus:border-indigo-500 focus:ring-2 focus:ring-indigo-200"
        />
        <div className="mt-1 text-right text-xs text-slate-400">{question.length}/500 · ⌘/Ctrl+Enter to send</div>
      </div>

      <div className="grid grid-cols-2 gap-3">
        <div>
          <label className="mb-1 block text-sm font-medium text-slate-700">Domain</label>
          <select
            value={domain}
            onChange={(e) => setDomain(e.target.value)}
            className="w-full rounded-lg border border-slate-300 p-2 text-sm shadow-sm outline-none focus:border-indigo-500"
          >
            <option value="banking_payments">Banking &amp; Payments</option>
            <option value="insurance">Insurance</option>
          </select>
        </div>
        <div>
          <label className="mb-1 block text-sm font-medium text-slate-700">Bank (optional)</label>
          <select
            value={bank}
            onChange={(e) => setBank(e.target.value)}
            className="w-full rounded-lg border border-slate-300 p-2 text-sm shadow-sm outline-none focus:border-indigo-500"
          >
            {BANKS.map((b) => (
              <option key={b.v} value={b.v}>
                {b.label}
              </option>
            ))}
          </select>
        </div>
      </div>

      <div className="flex gap-2">
        <button
          onClick={submit}
          disabled={loading || !question.trim()}
          className="flex-1 rounded-lg bg-indigo-600 px-4 py-2.5 text-sm font-semibold text-white shadow-sm transition hover:bg-indigo-700 disabled:cursor-not-allowed disabled:opacity-50"
        >
          {loading ? 'Analyzing…' : 'Ask FinTrust AI'}
        </button>
        <button
          onClick={() => setQuestion('')}
          disabled={loading}
          className="rounded-lg border border-slate-300 px-4 py-2.5 text-sm font-medium text-slate-600 hover:bg-slate-50 disabled:opacity-50"
        >
          Clear
        </button>
      </div>

      <div>
        <div className="mb-1.5 text-xs font-medium uppercase tracking-wide text-slate-400">Try an example</div>
        <div className="flex flex-wrap gap-2">
          {SAMPLES.map((s) => (
            <button
              key={s}
              onClick={() => setQuestion(s)}
              disabled={loading}
              className="rounded-full border border-slate-200 bg-white px-3 py-1 text-left text-xs text-slate-600 hover:border-indigo-300 hover:text-indigo-700 disabled:opacity-50"
            >
              {s.length > 46 ? s.slice(0, 46) + '…' : s}
            </button>
          ))}
        </div>
      </div>
    </div>
  )
}
