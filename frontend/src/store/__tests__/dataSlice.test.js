import { describe, it, expect } from 'vitest'
import dataReducer, {
  fetchGenerationData,
  fetchPricingData,
  fetchRenewableData,
  fetchSummary
} from '../slices/dataSlice'

describe('dataSlice', () => {
  const initialState = {
    generation: [],
    pricing: [],
    renewable: [],
    summary: null,
    loading: false,
    error: null,
  }

  it('should return initial state', () => {
    expect(dataReducer(undefined, { type: 'unknown' })).toEqual(initialState)
  })

  it('should handle fetchGenerationData.pending', () => {
    const action = { type: fetchGenerationData.pending.type }
    const state = dataReducer(initialState, action)
    expect(state.loading).toBe(true)
    expect(state.error).toBeNull()
  })

  it('should handle fetchGenerationData.fulfilled', () => {
    const mockData = [{ id: 1, region: 'CAISO' }]
    const action = { type: fetchGenerationData.fulfilled.type, payload: mockData }
    const state = dataReducer(initialState, action)
    expect(state.loading).toBe(false)
    expect(state.generation).toEqual(mockData)
  })

  it('should handle fetchGenerationData.rejected', () => {
    const error = 'Failed to fetch'
    const action = { type: fetchGenerationData.rejected.type, payload: error }
    const state = dataReducer(initialState, action)
    expect(state.loading).toBe(false)
    expect(state.error).toBe(error)
  })

  it('should handle fetchSummary.fulfilled', () => {
    const mockSummary = { total_capacity_mw: 5000, renewable_percentage: 45 }
    const action = { type: fetchSummary.fulfilled.type, payload: mockSummary }
    const state = dataReducer(initialState, action)
    expect(state.summary).toEqual(mockSummary)
  })
})
