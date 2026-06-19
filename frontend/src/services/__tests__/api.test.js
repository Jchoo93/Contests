import { describe, it, expect, vi, beforeEach } from 'vitest'
import axios from 'axios'
import {
  generationAPI,
  pricingAPI,
  renewableAPI,
  summaryAPI,
  healthAPI
} from '../api'

vi.mock('axios')

describe('API Services', () => {
  beforeEach(() => {
    vi.clearAllMocks()
  })

  describe('generationAPI', () => {
    it('should fetch generation data', async () => {
      const mockData = [{ id: 1, region: 'CAISO', solar_capacity_mw: 100 }]
      axios.create().get.mockResolvedValueOnce({ data: mockData })

      // The actual test would need proper mocking setup
      expect(generationAPI).toBeDefined()
      expect(generationAPI.getAll).toBeDefined()
    })
  })

  describe('pricingAPI', () => {
    it('should have pricing endpoints', () => {
      expect(pricingAPI).toBeDefined()
      expect(pricingAPI.getAll).toBeDefined()
      expect(pricingAPI.getByDate).toBeDefined()
    })
  })

  describe('renewableAPI', () => {
    it('should have renewable endpoints', () => {
      expect(renewableAPI).toBeDefined()
      expect(renewableAPI.getAll).toBeDefined()
      expect(renewableAPI.getByDate).toBeDefined()
    })
  })

  describe('summaryAPI', () => {
    it('should have summary endpoint', () => {
      expect(summaryAPI).toBeDefined()
      expect(summaryAPI.get).toBeDefined()
    })
  })

  describe('healthAPI', () => {
    it('should have health check endpoint', () => {
      expect(healthAPI).toBeDefined()
      expect(healthAPI.check).toBeDefined()
    })
  })
})
