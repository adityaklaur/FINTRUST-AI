import { useMutation } from '@tanstack/react-query'

import { api } from '../api/client'
import type { QueryRequest, QueryResponse } from '../api/types'

export function useAskQuery() {
  return useMutation<QueryResponse, Error, QueryRequest>({
    mutationFn: async (req) => {
      const { data } = await api.post<QueryResponse>('/api/query', {
        include_debug: true,
        ...req,
      })
      return data
    },
  })
}
