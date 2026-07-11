import axios from 'axios'

// Empty baseURL => same-origin; the Vite dev server proxies /api to the backend.
// For a standalone production build, set VITE_API_URL to the backend origin.
export const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL ?? '',
  headers: { 'Content-Type': 'application/json' },
})

// The auth layer keeps this updated with the current Supabase access token; the
// interceptor attaches it so the backend can resolve the user (or stay anon).
let accessToken: string | null = null

export function setAccessToken(token: string | null) {
  accessToken = token
}

api.interceptors.request.use((config) => {
  if (accessToken) {
    config.headers.Authorization = `Bearer ${accessToken}`
  }
  return config
})
