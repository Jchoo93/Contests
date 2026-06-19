export default function MarketInsights({ data, region }) {
  if (!data?.insights) {
    return (
      <div className="bg-slate-800 rounded-lg p-6">
        <p className="text-slate-400">No insights available</p>
      </div>
    )
  }

  const { insights, current_state, key_metrics } = data

  const InsightSection = ({ title, items, bgColor, icon }) => (
    <div className={`${bgColor} rounded-lg p-4`}>
      <h3 className="font-semibold text-white mb-3 flex items-center gap-2">
        <span>{icon}</span>
        {title}
      </h3>
      {items && items.length > 0 ? (
        <ul className="space-y-2">
          {items.map((item, idx) => (
            <li key={idx} className="text-slate-300 text-sm flex gap-2">
              <span className="text-slate-500 flex-shrink-0">•</span>
              <span>{item}</span>
            </li>
          ))}
        </ul>
      ) : (
        <p className="text-slate-400 text-sm">No items to display</p>
      )}
    </div>
  )

  return (
    <div className="space-y-6">
      <div className="bg-slate-800 rounded-lg p-6">
        <h2 className="text-xl font-semibold text-white mb-4">Market Analysis - {region}</h2>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
          <div className="bg-slate-700 rounded-lg p-4">
            <p className="text-slate-400 text-sm">Renewable Percentage</p>
            <p className="text-3xl font-bold text-green-400 mt-2">
              {current_state?.renewable_percentage?.toFixed(1)}%
            </p>
          </div>
          <div className="bg-slate-700 rounded-lg p-4">
            <p className="text-slate-400 text-sm">Diversity Score</p>
            <p className="text-3xl font-bold text-blue-400 mt-2">
              {current_state?.diversity_score?.toFixed(1)}/10
            </p>
          </div>
          <div className="bg-slate-700 rounded-lg p-4">
            <p className="text-slate-400 text-sm">Volatility</p>
            <p className={`text-3xl font-bold mt-2 ${
              (current_state?.volatility || 0) > 1.5 ? 'text-yellow-400' : 'text-green-400'
            }`}>
              {current_state?.volatility?.toFixed(2)}%
            </p>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <InsightSection
          title="Positive Trends"
          items={insights.positive_trends}
          bgColor="bg-green-900/20 border border-green-700/50"
          icon="📈"
        />
        <InsightSection
          title="Concerns"
          items={insights.concerns}
          bgColor="bg-red-900/20 border border-red-700/50"
          icon="⚠️"
        />
      </div>

      <InsightSection
        title="Recommendations"
        items={insights.recommendations}
        bgColor="bg-blue-900/20 border border-blue-700/50"
        icon="💡"
      />

      <div className="bg-slate-800 rounded-lg p-6">
        <h3 className="text-lg font-semibold text-white mb-4">Key Metrics</h3>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          <div className="bg-slate-700 rounded-lg p-4">
            <p className="text-slate-400 text-xs uppercase tracking-wide">7-Day Growth</p>
            <p className={`text-2xl font-bold mt-2 ${
              (key_metrics?.renewable_growth_7d || 0) > 0 ? 'text-green-400' : 'text-red-400'
            }`}>
              {(key_metrics?.renewable_growth_7d || 0) > 0 ? '+' : ''}
              {key_metrics?.renewable_growth_7d?.toFixed(2)}%
            </p>
          </div>
          <div className="bg-slate-700 rounded-lg p-4">
            <p className="text-slate-400 text-xs uppercase tracking-wide">30-Day Growth</p>
            <p className={`text-2xl font-bold mt-2 ${
              (key_metrics?.renewable_growth_30d || 0) > 0 ? 'text-green-400' : 'text-red-400'
            }`}>
              {(key_metrics?.renewable_growth_30d || 0) > 0 ? '+' : ''}
              {key_metrics?.renewable_growth_30d?.toFixed(2)}%
            </p>
          </div>
          <div className="bg-slate-700 rounded-lg p-4">
            <p className="text-slate-400 text-xs uppercase tracking-wide">1-Year Growth</p>
            <p className={`text-2xl font-bold mt-2 ${
              (key_metrics?.renewable_growth_1y || 0) > 0 ? 'text-green-400' : 'text-red-400'
            }`}>
              {(key_metrics?.renewable_growth_1y || 0) > 0 ? '+' : ''}
              {key_metrics?.renewable_growth_1y?.toFixed(2)}%
            </p>
          </div>
          <div className="bg-slate-700 rounded-lg p-4">
            <p className="text-slate-400 text-xs uppercase tracking-wide">Market Index</p>
            <p className="text-2xl font-bold text-purple-400 mt-2">
              {key_metrics?.herfindahl_index?.toFixed(1)}
            </p>
          </div>
        </div>
      </div>
    </div>
  )
}
