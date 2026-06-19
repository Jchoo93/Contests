import axios from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api'

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  }
})

export const generationAPI = {
  getAll: (days = 1) => api.get(`/generation?days=${days}`),
  getByDate: (date) => api.get(`/generation/${date}`),
}

export const pricingAPI = {
  getAll: (days = 1) => api.get(`/pricing?days=${days}`),
  getByDate: (date) => api.get(`/pricing/${date}`),
}

export const renewableAPI = {
  getAll: (days = 1) => api.get(`/renewables?days=${days}`),
  getByDate: (date) => api.get(`/renewables/${date}`),
}

export const summaryAPI = {
  get: () => api.get('/summary'),
}

export const healthAPI = {
  check: () => api.get('/health'),
}

export const analyticsAPI = {
  getGenerationMixTrend: (region, days = 7) =>
    api.get(`/analytics/generation-mix-trend/${region}?days=${days}`),
  getGenerationMixComparison: () =>
    api.get('/analytics/generation-mix-comparison'),
  getMarketInsights: (region) =>
    api.get(`/analytics/market-insights/${region}`),
  getVolatilityAnalysis: (region, days = 7) =>
    api.get(`/analytics/volatility-analysis/${region}?days=${days}`),
}

export default api
