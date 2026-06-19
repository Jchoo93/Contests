import { describe, it, expect } from 'vitest'
import { render, screen } from '@testing-library/react'
import { Provider } from 'react-redux'
import { configureStore } from '@reduxjs/toolkit'
import SummaryCard from '../SummaryCard'
import dataReducer from '../../store/slices/dataSlice'

describe('SummaryCard Component', () => {
  it('should render summary cards when data is available', () => {
    const mockSummary = {
      total_capacity_mw: 5000,
      renewable_percentage: 45.5,
      average_price_per_mwh: 50.25,
      regions_count: 12,
      last_update: new Date().toISOString()
    }

    const store = configureStore({
      reducer: {
        data: (state = { summary: mockSummary }, action) => state
      }
    })

    render(
      <Provider store={store}>
        <SummaryCard />
      </Provider>
    )

    expect(screen.getByText('Total Capacity')).toBeInTheDocument()
    expect(screen.getByText('Renewable %')).toBeInTheDocument()
    expect(screen.getByText('Avg Price')).toBeInTheDocument()
    expect(screen.getByText('Regions')).toBeInTheDocument()
  })

  it('should return null when summary is not available', () => {
    const store = configureStore({
      reducer: {
        data: (state = { summary: null }, action) => state
      }
    })

    const { container } = render(
      <Provider store={store}>
        <SummaryCard />
      </Provider>
    )

    expect(container.firstChild).toBeNull()
  })
})
