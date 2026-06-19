import { createSlice, createAsyncThunk } from '@reduxjs/toolkit'
import {
  generationAPI,
  pricingAPI,
  renewableAPI,
  summaryAPI
} from '../../services/api'

export const fetchGenerationData = createAsyncThunk(
  'data/fetchGeneration',
  async (_, { rejectWithValue }) => {
    try {
      const response = await generationAPI.getAll(1)
      return response.data
    } catch (error) {
      return rejectWithValue(error.response?.data || 'Failed to fetch generation data')
    }
  }
)

export const fetchPricingData = createAsyncThunk(
  'data/fetchPricing',
  async (_, { rejectWithValue }) => {
    try {
      const response = await pricingAPI.getAll(1)
      return response.data
    } catch (error) {
      return rejectWithValue(error.response?.data || 'Failed to fetch pricing data')
    }
  }
)

export const fetchRenewableData = createAsyncThunk(
  'data/fetchRenewable',
  async (_, { rejectWithValue }) => {
    try {
      const response = await renewableAPI.getAll(1)
      return response.data
    } catch (error) {
      return rejectWithValue(error.response?.data || 'Failed to fetch renewable data')
    }
  }
)

export const fetchSummary = createAsyncThunk(
  'data/fetchSummary',
  async (_, { rejectWithValue }) => {
    try {
      const response = await summaryAPI.get()
      return response.data
    } catch (error) {
      return rejectWithValue(error.response?.data || 'Failed to fetch summary')
    }
  }
)

const initialState = {
  generation: [],
  pricing: [],
  renewable: [],
  summary: null,
  loading: false,
  error: null,
}

const dataSlice = createSlice({
  name: 'data',
  initialState,
  extraReducers: (builder) => {
    builder
      .addCase(fetchGenerationData.pending, (state) => {
        state.loading = true
        state.error = null
      })
      .addCase(fetchGenerationData.fulfilled, (state, action) => {
        state.loading = false
        state.generation = action.payload
      })
      .addCase(fetchGenerationData.rejected, (state, action) => {
        state.loading = false
        state.error = action.payload
      })

      .addCase(fetchPricingData.pending, (state) => {
        state.loading = true
        state.error = null
      })
      .addCase(fetchPricingData.fulfilled, (state, action) => {
        state.loading = false
        state.pricing = action.payload
      })
      .addCase(fetchPricingData.rejected, (state, action) => {
        state.loading = false
        state.error = action.payload
      })

      .addCase(fetchRenewableData.pending, (state) => {
        state.loading = true
        state.error = null
      })
      .addCase(fetchRenewableData.fulfilled, (state, action) => {
        state.loading = false
        state.renewable = action.payload
      })
      .addCase(fetchRenewableData.rejected, (state, action) => {
        state.loading = false
        state.error = action.payload
      })

      .addCase(fetchSummary.pending, (state) => {
        state.loading = true
        state.error = null
      })
      .addCase(fetchSummary.fulfilled, (state, action) => {
        state.loading = false
        state.summary = action.payload
      })
      .addCase(fetchSummary.rejected, (state, action) => {
        state.loading = false
        state.error = action.payload
      })
  }
})

export default dataSlice.reducer
