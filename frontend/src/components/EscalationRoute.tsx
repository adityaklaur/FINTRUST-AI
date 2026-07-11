export function EscalationRoute({ steps }: { steps: string[] }) {
  if (!steps?.length) return null
  return (
    <ol className="space-y-2">
      {steps.map((s, i) => {
        const url = s.match(/https?:\/\/\S+/)?.[0]
        const text = s.replace(/^Step \d+:\s*/, '')
        return (
          <li key={i} className="flex gap-3 rounded-lg border border-slate-200 bg-white p-3 text-sm">
            <span className="flex h-6 w-6 shrink-0 items-center justify-center rounded-full bg-indigo-600 text-xs font-bold text-white">
              {i + 1}
            </span>
            <span className="text-slate-700">
              {text}
              {url && (
                <a href={url} target="_blank" rel="noreferrer" className="ml-1 font-medium text-indigo-600 hover:underline">
                  ↗
                </a>
              )}
            </span>
          </li>
        )
      })}
    </ol>
  )
}
