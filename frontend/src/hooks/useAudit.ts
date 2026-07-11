import { useQuery } from '@tanstack/react-query'

import { api } from '../api/client'
import type { AuditEntry } from '../api/types'

export function useAudit(params: { category?: string; risk?: string; limit?: number }) {
  return useQuery<AuditEntry[]>({
    queryKey: ['audit', params],
    queryFn: async () => {
      const { data } = await api.get<AuditEntry[]>('/api/audit', {
        params: {
          limit: params.limit ?? 50,
          category: params.category || undefined,
          risk_level: params.risk || undefined,
        },
      })
      return data
    },
  })
}
