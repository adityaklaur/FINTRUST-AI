export function AnswerPanel({ answer }: { answer: string }) {
  return <div className="whitespace-pre-wrap text-[15px] leading-relaxed text-slate-700">{answer.trim()}</div>
}
