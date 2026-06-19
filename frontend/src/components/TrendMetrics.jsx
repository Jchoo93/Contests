export default function TrendMetrics({ data, region }) {
  if (!data?.current_mix) {
    return (
      <div className="bg-slate-800 rounded-lg p-6">
        <p className="text-slate-400">No data available</p>
      </div>
    )
  }

  const { current_mix, trend_7_days, market_metrics } = data

  const MetricCard = ({ label, value, trend, changeValue, color }) => (
    <div className="bg-slate-700 rounded-lg p-4">
      <p className="text-slate-400 text-sm font-medium">{label}</p>
      <div className="flex items-center justify-between mt-2">
        <div>
          <p className={`text-2xl font-bold ${color}`}>{value.toFixed(1)}%</p>
          {changeValue !== undefined && (
            <p className={`text-xs mt-1 ${changeValue >= 0 ? 'text-green-400' : 'text-red-400'}`}>
              {changeValue > 0 ? '+' : ''}{changeValue.toFixed(2)}% (7d)
            </p>
          )}
        </div>
        <div className="text-4xl">{trend}</div>
      </div>
    </div>
  )

  return (
    <div className="space-y-6">
      <div className="bg-slate-800 rounded-lg p-6">
        <h2 className="text-xl font-semibold text-white mb-6">Current Mix - {region}</h2>
        <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-5 gap-4">
          <MetricCard
            label="Solar"
            value={current_mix.solar.percentage}
            trend={current_mix.solar.trend}
            changeValue={trend_7_days?.solar?.change_pct}
            color="text-yellow-400"
          />
          <MetricCard
            label="Wind"
            value={current_mix.wind.percentage}
            trend={current_mix.wind.trend}
            changeValue={trend_7_days?.wind?.change_pct}
            color="text-blue-400"
          />
          <MetricCard
            label="Hydro"
            value={current_mix.hydro.percentage}
            trend={current_mix.hydro.trend}
            color="text-cyan-400"
          />
          <MetricCard
            label="Fossil"
            value={current_mix.fossil.percentage}
            trend={current_mix.fossil.trend}
            changeValue={trend_7_days?.fossil?.change_pct}
            color="text-red-400"
          />
          <MetricCard
            label="Nuclear"
            value={current_mix.nuclear.percentage}
            trend={current_mix.nuclear.trend}
            color="text-purple-400"
          />
        </div>
      </div>

      <div className="bg-slate-800 rounded-lg p-6">
        <h3 className="text-lg font-semibold text-white mb-4">Renewable Analysis</h3>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="bg-slate-700 rounded-lg p-4">
            <p className="text-slate-400 text-sm">Total Renewable</p>
            <p className="text-3xl font-bold text-green-400 mt-2">
              {current_mix.renewable_total.percentage.toFixed(1)}%
            </p>
            <p className="text-xs text-slate-400 mt-1">{current_mix.renewable_total.trend}</p>
          </div>
          <div className="bg-slate-700 rounded-lg p-4">
            <p className="text-slate-400 text-sm">Energy Diversity Score</p>
            <p className="text-3xl font-bold text-blue-400 mt-2">
              {market_metrics?.energy_diversity_score?.toFixed(1)}/10
            </p>
          </div>
          <div className="bg-slate-700 rounded-lg p-4">
            <p className="text-slate-400 text-sm">Grid Stability</p>
            <p className={`text-2xl font-bold mt-2 ${
              market_metrics?.grid_stability === 'healthy' ? 'text-green-400' : 'text-yellow-400'
            }`}>
              {market_metrics?.grid_stability?.charAt(0).toUpperCase() +
                market_metrics?.grid_stability?.slice(1)}
            </p>
          </div>
        </div>
      </div>
    </div>
  )
}
