export function EvidenceChecklist({ items }: { items: string[] }) {
  if (!items?.length) return null
  return (
    <ul className="space-y-1.5">
      {items.map((it, i) => (
        <li key={i} className="flex items-start gap-2 text-sm text-slate-700">
          <span className="mt-0.5 text-emerald-600">☑</span>
          <span>{it}</span>
        </li>
      ))}
    </ul>
  )
}
