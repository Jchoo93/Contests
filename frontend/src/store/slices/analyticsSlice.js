import { createSlice, createAsyncThunk } from '@reduxjs/toolkit'
import { analyticsAPI } from '../../services/api'

export const fetchGenerationMixTrend = createAsyncThunk(
  'analytics/fetchGenerationMixTrend',
  async ({ region, days = 7 }, { rejectWithValue }) => {
    try {
      const response = await analyticsAPI.getGenerationMixTrend(region, days)
      return response.data
    } catch (error) {
      return rejectWithValue(error.response?.data || 'Failed to fetch trend data')
    }
  }
)

export const fetchGenerationMixComparison = createAsyncThunk(
  'analytics/fetchGenerationMixComparison',
  async (_, { rejectWithValue }) => {
    try {
      const response = await analyticsAPI.getGenerationMixComparison()
      return response.data
    } catch (error) {
      return rejectWithValue(error.response?.data || 'Failed to fetch comparison')
    }
  }
)

export const fetchMarketInsights = createAsyncThunk(
  'analytics/fetchMarketInsights',
  async (region, { rejectWithValue }) => {
    try {
      const response = await analyticsAPI.getMarketInsights(region)
      return response.data
    } catch (error) {
      return rejectWithValue(error.response?.data || 'Failed to fetch insights')
    }
  }
)

export const fetchVolatilityAnalysis = createAsyncThunk(
  'analytics/fetchVolatilityAnalysis',
  async ({ region, days = 7 }, { rejectWithValue }) => {
    try {
      const response = await analyticsAPI.getVolatilityAnalysis(region, days)
      return response.data
    } catch (error) {
      return rejectWithValue(error.response?.data || 'Failed to fetch volatility')
    }
  }
)

const initialState = {
  currentTrend: null,
  comparison: null,
  insights: null,
  volatility: null,
  selectedRegion: 'CAISO',
  selectedDays: 7,
  loading: false,
  error: null
}

const analyticsSlice = createSlice({
  name: 'analytics',
  initialState,
  reducers: {
    setSelectedRegion: (state, action) => {
      state.selectedRegion = action.payload
    },
    setSelectedDays: (state, action) => {
      state.selectedDays = action.payload
    }
  },
  extraReducers: (builder) => {
    builder
      .addCase(fetchGenerationMixTrend.pending, (state) => {
        state.loading = true
        state.error = null
      })
      .addCase(fetchGenerationMixTrend.fulfilled, (state, action) => {
        state.loading = false
        state.currentTrend = action.payload
      })
      .addCase(fetchGenerationMixTrend.rejected, (state, action) => {
        state.loading = false
        state.error = action.payload
      })
      .addCase(fetchGenerationMixComparison.pending, (state) => {
        state.loading = true
        state.error = null
      })
      .addCase(fetchGenerationMixComparison.fulfilled, (state, action) => {
        state.loading = false
        state.comparison = action.payload
      })
      .addCase(fetchGenerationMixComparison.rejected, (state, action) => {
        state.loading = false
        state.error = action.payload
      })
      .addCase(fetchMarketInsights.pending, (state) => {
        state.loading = true
        state.error = null
      })
      .addCase(fetchMarketInsights.fulfilled, (state, action) => {
        state.loading = false
        state.insights = action.payload
      })
      .addCase(fetchMarketInsights.rejected, (state, action) => {
        state.loading = false
        state.error = action.payload
      })
      .addCase(fetchVolatilityAnalysis.pending, (state) => {
        state.loading = true
        state.error = null
      })
      .addCase(fetchVolatilityAnalysis.fulfilled, (state, action) => {
        state.loading = false
        state.volatility = action.payload
      })
      .addCase(fetchVolatilityAnalysis.rejected, (state, action) => {
        state.loading = false
        state.error = action.payload
      })
  }
})

export const { setSelectedRegion, setSelectedDays } = analyticsSlice.actions
export default analyticsSlice.reducer
