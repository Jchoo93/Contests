import { useEffect, useState } from 'react'
import { useDispatch, useSelector } from 'react-redux'
import {
  fetchGenerationMixTrend,
  fetchGenerationMixComparison,
  fetchMarketInsights,
  fetchVolatilityAnalysis,
  setSelectedRegion,
  setSelectedDays,
} from '../store/slices/analyticsSlice'
import TrendMetrics from './TrendMetrics'
import TrendChart from './TrendChart'
import RegionalComparison from './RegionalComparison'
import MarketInsights from './MarketInsights'
import VolatilityAnalysis from './VolatilityAnalysis'

const REGIONS = ['CAISO', 'ERCOT', 'PJM', 'MISO', 'SPP', 'WECC']
const VIEWS = ['trend', 'comparison', 'insights', 'volatility']

export default function AnalyticsPage() {
  const dispatch = useDispatch()
  const {
    currentTrend,
    comparison,
    insights,
    volatility,
    selectedRegion,
    selectedDays,
    loading,
    error,
  } = useSelector((state) => state.analytics)

  const [activeView, setActiveView] = useState('trend')

  useEffect(() => {
    dispatch(fetchGenerationMixTrend({ region: selectedRegion, days: selectedDays }))
    dispatch(fetchMarketInsights(selectedRegion))
    dispatch(fetchVolatilityAnalysis({ region: selectedRegion, days: selectedDays }))
  }, [dispatch, selectedRegion, selectedDays])

  useEffect(() => {
    if (activeView === 'comparison') {
      dispatch(fetchGenerationMixComparison())
    }
  }, [dispatch, activeView])

  return (
    <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div className="space-y-6">
        {/* Controls */}
        <div className="bg-slate-800 rounded-lg p-6">
          <div className="flex flex-col gap-4">
            <div>
              <label className="block text-sm font-medium text-slate-300 mb-2">
                Select Region
              </label>
              <select
                value={selectedRegion}
                onChange={(e) => dispatch(setSelectedRegion(e.target.value))}
                className="w-full bg-slate-700 border border-slate-600 rounded-lg px-4 py-2 text-white focus:outline-none focus:border-blue-500"
              >
                {REGIONS.map((region) => (
                  <option key={region} value={region}>
                    {region}
                  </option>
                ))}
              </select>
            </div>

            <div>
              <label className="block text-sm font-medium text-slate-300 mb-2">
                Time Period
              </label>
              <div className="flex gap-2">
                {[7, 30, 90, 365].map((days) => (
                  <button
                    key={days}
                    onClick={() => dispatch(setSelectedDays(days))}
                    className={`px-4 py-2 rounded-lg font-medium transition-colors ${
                      selectedDays === days
                        ? 'bg-blue-600 text-white'
                        : 'bg-slate-700 text-slate-300 hover:bg-slate-600'
                    }`}
                  >
                    {days}d
                  </button>
                ))}
              </div>
            </div>
          </div>
        </div>

        {/* View Tabs */}
        <div className="flex gap-2 border-b border-slate-700">
          {VIEWS.map((view) => (
            <button
              key={view}
              onClick={() => setActiveView(view)}
              className={`px-4 py-3 font-medium border-b-2 transition-colors capitalize ${
                activeView === view
                  ? 'border-blue-500 text-blue-400'
                  : 'border-transparent text-slate-400 hover:text-slate-300'
              }`}
            >
              {view === 'trend' && '📊 Trend'}
              {view === 'comparison' && '🗺️ Regional'}
              {view === 'insights' && '💡 Insights'}
              {view === 'volatility' && '📈 Volatility'}
            </button>
          ))}
        </div>

        {/* Error Message */}
        {error && (
          <div className="bg-red-900/20 border border-red-700 rounded-lg p-4 text-red-200">
            {typeof error === 'string' ? error : 'An error occurred'}
          </div>
        )}

        {/* Loading State */}
        {loading && (
          <div className="flex justify-center items-center py-20">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500"></div>
          </div>
        )}

        {/* Content */}
        {!loading && (
          <>
            {activeView === 'trend' && currentTrend && (
              <div className="space-y-6">
                <TrendMetrics data={currentTrend} region={selectedRegion} />
                <TrendChart data={currentTrend} region={selectedRegion} />
              </div>
            )}

            {activeView === 'comparison' && comparison && (
              <RegionalComparison data={comparison} />
            )}

            {activeView === 'insights' && insights && (
              <MarketInsights data={insights} region={selectedRegion} />
            )}

            {activeView === 'volatility' && volatility && (
              <VolatilityAnalysis data={volatility} region={selectedRegion} />
            )}
          </>
        )}

        {/* Footer */}
        <footer className="text-center text-slate-400 text-sm py-8 border-t border-slate-700">
          <p>Market Analysis Dashboard - Real-time Generation Mix Analytics</p>
        </footer>
      </div>
    </main>
  )
}
