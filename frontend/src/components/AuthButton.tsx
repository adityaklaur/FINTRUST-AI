import type { Session } from '@supabase/supabase-js'
import { useEffect, useState } from 'react'

import { setAccessToken } from '../api/client'
import { authEnabled, supabase } from '../lib/supabase'

export function AuthButton() {
  const [session, setSession] = useState<Session | null>(null)
  const [open, setOpen] = useState(false)
  const [email, setEmail] = useState('')
  const [sent, setSent] = useState(false)

  useEffect(() => {
    if (!supabase) return
    supabase.auth.getSession().then(({ data }) => {
      setSession(data.session)
      setAccessToken(data.session?.access_token ?? null)
    })
    const { data } = supabase.auth.onAuthStateChange((_event, next) => {
      setSession(next)
      setAccessToken(next?.access_token ?? null)
    })
    return () => data.subscription.unsubscribe()
  }, [])

  // Not configured → honest disabled "soon" chip (unchanged default behavior).
  if (!authEnabled) {
    return (
      <button
        type="button"
        disabled
        title="Accounts are coming soon (configure Supabase to enable)"
        className="flex cursor-not-allowed items-center gap-1.5 rounded-lg border border-slate-200 px-3 py-1.5 text-sm font-medium text-slate-400"
      >
        Sign in
        <span className="rounded-full bg-amber-100 px-1.5 py-0.5 text-[10px] font-semibold uppercase text-amber-700">
          soon
        </span>
      </button>
    )
  }

  if (session) {
    return (
      <div className="flex items-center gap-2 text-sm">
        <span className="hidden max-w-[160px] truncate text-slate-500 sm:inline">{session.user.email}</span>
        <button
          onClick={() => supabase!.auth.signOut()}
          className="rounded-lg border border-slate-200 px-3 py-1.5 font-medium text-slate-600 hover:bg-slate-50"
        >
          Sign out
        </button>
      </div>
    )
  }

  const sendLink = async () => {
    if (!email.trim() || !supabase) return
    await supabase.auth.signInWithOtp({
      email: email.trim(),
      options: { emailRedirectTo: window.location.origin },
    })
    setSent(true)
  }

  return (
    <div className="relative">
      <button
        onClick={() => setOpen(!open)}
        className="rounded-lg border border-slate-200 px-3 py-1.5 text-sm font-medium text-slate-600 hover:bg-slate-50"
      >
        Sign in
      </button>
      {open && (
        <div className="absolute right-0 z-10 mt-2 w-64 rounded-lg border border-slate-200 bg-white p-3 shadow-lg">
          {sent ? (
            <p className="text-sm text-slate-600">Check your email for a sign-in link.</p>
          ) : (
            <>
              <label className="mb-1 block text-xs font-medium text-slate-500">Email (magic link)</label>
              <input
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                type="email"
                placeholder="you@example.com"
                className="mb-2 w-full rounded-md border border-slate-300 p-2 text-sm outline-none focus:border-indigo-500"
              />
              <button
                onClick={sendLink}
                className="w-full rounded-md bg-indigo-600 px-3 py-1.5 text-sm font-semibold text-white hover:bg-indigo-700"
              >
                Send link
              </button>
            </>
          )}
        </div>
      )}
    </div>
  )
}
