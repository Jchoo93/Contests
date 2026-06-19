import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts'

export default function RegionalComparison({ data }) {
  if (!data?.regions) {
    return (
      <div className="bg-slate-800 rounded-lg p-6">
        <p className="text-slate-400">No data available</p>
      </div>
    )
  }

  const chartData = data.regions.map((region) => ({
    name: region.region,
    renewable: region.renewable_percentage,
    fossil: region.fossil_pct,
    diversity: region.energy_diversity_score * 10, // Scale to 0-100
  }))

  return (
    <div className="space-y-6">
      <div className="bg-slate-800 rounded-lg p-6">
        <h2 className="text-xl font-semibold text-white mb-4">Regional Comparison</h2>
        <ResponsiveContainer width="100%" height={350}>
          <BarChart data={chartData}>
            <CartesianGrid strokeDasharray="3 3" stroke="#475569" />
            <XAxis dataKey="name" stroke="#94a3b8" />
            <YAxis stroke="#94a3b8" />
            <Tooltip
              contentStyle={{ backgroundColor: '#1e293b', border: '1px solid #475569' }}
              labelStyle={{ color: '#e2e8f0' }}
            />
            <Legend />
            <Bar dataKey="renewable" fill="#10b981" name="Renewable %" />
            <Bar dataKey="fossil" fill="#ef4444" name="Fossil %" />
          </BarChart>
        </ResponsiveContainer>
      </div>

      <div className="bg-slate-800 rounded-lg p-6">
        <h3 className="text-lg font-semibold text-white mb-4">Rankings</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          <div className="bg-slate-700 rounded-lg p-4">
            <p className="text-slate-400 text-sm">Highest Renewable</p>
            <p className="text-2xl font-bold text-green-400 mt-2">
              {data.summary?.highest_renewable}
            </p>
          </div>
          <div className="bg-slate-700 rounded-lg p-4">
            <p className="text-slate-400 text-sm">Highest Fossil</p>
            <p className="text-2xl font-bold text-red-400 mt-2">
              {data.summary?.highest_fossil}
            </p>
          </div>
          <div className="bg-slate-700 rounded-lg p-4">
            <p className="text-slate-400 text-sm">Best Diversity</p>
            <p className="text-2xl font-bold text-blue-400 mt-2">
              {data.summary?.highest_diversity}
            </p>
          </div>
          <div className="bg-slate-700 rounded-lg p-4">
            <p className="text-slate-400 text-sm">Fastest Growth</p>
            <p className="text-2xl font-bold text-purple-400 mt-2">
              {data.summary?.fastest_renewable_growth}
            </p>
          </div>
        </div>
      </div>

      <div className="bg-slate-800 rounded-lg p-6">
        <h3 className="text-lg font-semibold text-white mb-4">Detailed Breakdown</h3>
        <div className="overflow-x-auto">
          <table className="w-full text-sm">
            <thead className="border-b border-slate-700">
              <tr>
                <th className="text-left py-2 px-4 text-slate-300">Region</th>
                <th className="text-right py-2 px-4 text-slate-300">Renewable %</th>
                <th className="text-right py-2 px-4 text-slate-300">Solar</th>
                <th className="text-right py-2 px-4 text-slate-300">Wind</th>
                <th className="text-right py-2 px-4 text-slate-300">Diversity</th>
                <th className="text-right py-2 px-4 text-slate-300">Growth (7d)</th>
              </tr>
            </thead>
            <tbody>
              {data.regions.map((region) => (
                <tr key={region.region} className="border-b border-slate-700/50 hover:bg-slate-700/30">
                  <td className="py-3 px-4 font-semibold text-white">{region.region}</td>
                  <td className="text-right py-3 px-4 text-green-400">
                    {region.renewable_percentage.toFixed(1)}%
                  </td>
                  <td className="text-right py-3 px-4 text-yellow-400">
                    {region.solar?.toFixed(1) || 'N/A'}%
                  </td>
                  <td className="text-right py-3 px-4 text-blue-400">
                    {region.wind?.toFixed(1) || 'N/A'}%
                  </td>
                  <td className="text-right py-3 px-4 text-blue-400">
                    {region.energy_diversity_score?.toFixed(1) || 'N/A'}/10
                  </td>
                  <td className={`text-right py-3 px-4 font-semibold ${
                    (region.renewable_change_7d || 0) > 0 ? 'text-green-400' : 'text-red-400'
                  }`}>
                    {(region.renewable_change_7d || 0) > 0 ? '+' : ''}
                    {region.renewable_change_7d?.toFixed(2) || '0'}%
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  )
}
