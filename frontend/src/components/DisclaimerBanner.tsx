export function DisclaimerBanner({ text }: { text: string }) {
  return (
    <div className="rounded-lg border border-amber-300 bg-amber-50 px-4 py-3 text-sm text-amber-900">
      {text ||
        '⚠️ This is not legal, financial, or regulatory advice. Always verify with the official source or a qualified professional.'}
    </div>
  )
}
