import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts'

export default function VolatilityAnalysis({ data, region }) {
  if (!data?.volatility_analysis) {
    return (
      <div className="bg-slate-800 rounded-lg p-6">
        <p className="text-slate-400">No data available</p>
      </div>
    )
  }

  const { volatility_analysis, grid_stability } = data

  const volatilityData = [
    {
      name: 'Solar',
      volatility: volatility_analysis.solar?.volatility || 0,
    },
    {
      name: 'Wind',
      volatility: volatility_analysis.wind?.volatility || 0,
    },
    {
      name: 'Hydro',
      volatility: volatility_analysis.hydro?.volatility || 0,
    },
    {
      name: 'Renewable',
      volatility: volatility_analysis.renewable_total?.volatility || 0,
    },
  ]

  const SourceCard = ({ source, data: sourceData }) => (
    <div className="bg-slate-700 rounded-lg p-4">
      <h4 className="font-semibold text-white mb-3">{source}</h4>
      <div className="space-y-2">
        <div>
          <p className="text-slate-400 text-xs">Current Percentage</p>
          <p className="text-2xl font-bold text-blue-400">
            {sourceData?.current?.toFixed(1)}%
          </p>
        </div>
        <div>
          <p className="text-slate-400 text-xs">Volatility (σ)</p>
          <p className={`text-lg font-bold ${
            (sourceData?.volatility || 0) > 2 ? 'text-yellow-400' : 'text-green-400'
          }`}>
            {sourceData?.volatility?.toFixed(2)}%
          </p>
        </div>
        <div>
          <p className="text-slate-400 text-xs">Stability</p>
          <p className="text-sm text-slate-300">
            {sourceData?.interpretation || 'Unknown'}
          </p>
        </div>
        <div>
          <p className="text-slate-400 text-xs">Primary Driver</p>
          <p className="text-sm text-slate-300">
            {sourceData?.primary_driver || 'N/A'}
          </p>
        </div>
      </div>
    </div>
  )

  return (
    <div className="space-y-6">
      <div className="bg-slate-800 rounded-lg p-6">
        <h2 className="text-xl font-semibold text-white mb-4">Volatility Analysis - {region}</h2>
        <ResponsiveContainer width="100%" height={350}>
          <BarChart data={volatilityData}>
            <CartesianGrid strokeDasharray="3 3" stroke="#475569" />
            <XAxis dataKey="name" stroke="#94a3b8" />
            <YAxis stroke="#94a3b8" label={{ value: 'Volatility %', angle: -90, position: 'insideLeft' }} />
            <Tooltip
              contentStyle={{ backgroundColor: '#1e293b', border: '1px solid #475569' }}
              labelStyle={{ color: '#e2e8f0' }}
            />
            <Bar dataKey="volatility" fill="#f59e0b" name="Volatility (σ)" />
          </BarChart>
        </ResponsiveContainer>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <SourceCard
          source="Solar"
          data={volatility_analysis.solar}
        />
        <SourceCard
          source="Wind"
          data={volatility_analysis.wind}
        />
        <SourceCard
          source="Hydro"
          data={volatility_analysis.hydro}
        />
        <SourceCard
          source="Renewable Total"
          data={volatility_analysis.renewable_total}
        />
      </div>

      <div className="bg-slate-800 rounded-lg p-6">
        <h3 className="text-lg font-semibold text-white mb-4">Grid Stability Assessment</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div className="bg-slate-700 rounded-lg p-4">
            <p className="text-slate-400 text-sm mb-2">Stability Score</p>
            <p className={`text-4xl font-bold ${
              grid_stability?.stability_score > 80 ? 'text-green-400' :
              grid_stability?.stability_score > 60 ? 'text-yellow-400' : 'text-red-400'
            }`}>
              {grid_stability?.stability_score?.toFixed(0)}
            </p>
            <p className="text-xs text-slate-400 mt-2">Out of 100</p>
          </div>
          <div className="bg-slate-700 rounded-lg p-4">
            <p className="text-slate-400 text-sm mb-2">Status</p>
            <p className={`text-2xl font-bold ${
              grid_stability?.status === 'Healthy' ? 'text-green-400' : 'text-yellow-400'
            }`}>
              {grid_stability?.status}
            </p>
            <p className="text-xs text-slate-400 mt-2">Based on renewable volatility</p>
          </div>
        </div>
      </div>

      <div className="bg-blue-900/20 border border-blue-700/50 rounded-lg p-6">
        <h3 className="text-lg font-semibold text-white mb-3">📌 Volatility Interpretation</h3>
        <div className="space-y-2 text-sm text-slate-300">
          <p>
            <span className="text-blue-400 font-semibold">Volatility (σ)</span> measures the
            standard deviation of generation percentages over the selected period. Higher volatility
            indicates more unpredictable generation patterns.
          </p>
          <p className="mt-3">
            <span className="text-yellow-400 font-semibold">Solar</span> shows daily cycles from sunrise/sunset
            and weather variations.
          </p>
          <p>
            <span className="text-blue-400 font-semibold">Wind</span> reflects weather patterns that can vary
            significantly day-to-day.
          </p>
          <p>
            <span className="text-cyan-400 font-semibold">Hydro</span> is typically the most stable as it's
            controlled by reservoir management.
          </p>
        </div>
      </div>
    </div>
  )
}
