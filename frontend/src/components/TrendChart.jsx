import {
  LineChart,
  Line,
  AreaChart,
  Area,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from 'recharts'

export default function TrendChart({ data, region }) {
  if (!data?.daily_breakdown || data.daily_breakdown.length === 0) {
    return (
      <div className="bg-slate-800 rounded-lg p-6">
        <p className="text-slate-400">No data available</p>
      </div>
    )
  }

  const chartData = data.daily_breakdown.map((day) => ({
    date: new Date(day.date).toLocaleDateString('en-US', {
      month: 'short',
      day: 'numeric',
    }),
    solar: day.solar,
    wind: day.wind,
    hydro: day.hydro,
    fossil: day.fossil,
    nuclear: day.nuclear,
    renewable: day.renewable,
  }))

  return (
    <div className="bg-slate-800 rounded-lg p-6">
      <h2 className="text-xl font-semibold text-white mb-4">
        Generation Mix Trend - {region}
      </h2>
      <ResponsiveContainer width="100%" height={400}>
        <AreaChart data={chartData}>
          <CartesianGrid strokeDasharray="3 3" stroke="#475569" />
          <XAxis dataKey="date" stroke="#94a3b8" />
          <YAxis stroke="#94a3b8" label={{ value: 'Percentage (%)', angle: -90, position: 'insideLeft' }} />
          <Tooltip
            contentStyle={{ backgroundColor: '#1e293b', border: '1px solid #475569' }}
            labelStyle={{ color: '#e2e8f0' }}
          />
          <Legend />
          <Area
            type="monotone"
            dataKey="solar"
            stackId="1"
            stroke="#fbbf24"
            fill="#fbbf24"
            name="Solar"
          />
          <Area
            type="monotone"
            dataKey="wind"
            stackId="1"
            stroke="#3b82f6"
            fill="#3b82f6"
            name="Wind"
          />
          <Area
            type="monotone"
            dataKey="hydro"
            stackId="1"
            stroke="#06b6d4"
            fill="#06b6d4"
            name="Hydro"
          />
          <Area
            type="monotone"
            dataKey="fossil"
            stackId="1"
            stroke="#ef4444"
            fill="#ef4444"
            name="Fossil"
          />
          <Area
            type="monotone"
            dataKey="nuclear"
            stackId="1"
            stroke="#8b5cf6"
            fill="#8b5cf6"
            name="Nuclear"
          />
        </AreaChart>
      </ResponsiveContainer>
    </div>
  )
}
