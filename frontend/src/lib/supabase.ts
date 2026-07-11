import { createClient, type SupabaseClient } from '@supabase/supabase-js'

// Auth is OPTIONAL. Without these two env vars the client is null and the app
// runs in anonymous mode (identical to today). Set them to enable accounts.
const url = import.meta.env.VITE_SUPABASE_URL as string | undefined
const anon = import.meta.env.VITE_SUPABASE_ANON_KEY as string | undefined

export const supabase: SupabaseClient | null = url && anon ? createClient(url, anon) : null
export const authEnabled = supabase !== null
