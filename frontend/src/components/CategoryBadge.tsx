export function CategoryBadge({ label }: { label: string }) {
  if (!label) return null
  return (
    <span className="inline-flex items-center rounded-full bg-indigo-50 px-2.5 py-1 text-xs font-semibold text-indigo-700 ring-1 ring-inset ring-indigo-600/20">
      {label}
    </span>
  )
}
