import { useSelector } from 'react-redux'
import {
  PieChart,
  Pie,
  Cell,
  Legend,
  Tooltip,
  ResponsiveContainer,
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid
} from 'recharts'

export default function RenewableChart() {
  const renewable = useSelector(state => state.data.renewable)

  if (!renewable || renewable.length === 0) {
    return <div className="text-center text-slate-400">No renewable data available</div>
  }

  const aggregated = renewable.reduce((acc, item) => {
    const existing = acc.find(d => d.region === item.region)
    if (existing) {
      existing.renewable_percentage = (existing.renewable_percentage + item.renewable_percentage) / 2
    } else {
      acc.push({
        region: item.region.split('-')[0],
        renewable_percentage: item.renewable_percentage
      })
    }
    return acc
  }, []).sort((a, b) => b.renewable_percentage - a.renewable_percentage)

  const chartData = aggregated.slice(0, 10).map(item => ({
    name: item.region,
    value: parseFloat(item.renewable_percentage.toFixed(1))
  }))

  const COLORS = ['#10b981', '#06b6d4', '#3b82f6', '#8b5cf6', '#ec4899']

  const avgRenewable = (aggregated.reduce((sum, item) => sum + item.renewable_percentage, 0) / aggregated.length).toFixed(1)

  return (
    <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
      <div className="bg-slate-800 rounded-lg shadow-lg p-6">
        <h2 className="text-xl font-bold text-white mb-4">Renewable Energy Distribution</h2>
        <div className="mb-4 text-center">
          <p className="text-slate-300">Average Renewable Percentage</p>
          <p className="text-4xl font-bold text-green-400">{avgRenewable}%</p>
        </div>
        <ResponsiveContainer width="100%" height={300}>
          <PieChart>
            <Pie
              data={chartData}
              cx="50%"
              cy="50%"
              labelLine={false}
              label={({ name, value }) => `${name}: ${value}%`}
              outerRadius={100}
              fill="#8884d8"
              dataKey="value"
            >
              {chartData.map((entry, index) => (
                <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
              ))}
            </Pie>
            <Tooltip formatter={(value) => `${value}%`} />
          </PieChart>
        </ResponsiveContainer>
      </div>

      <div className="bg-slate-800 rounded-lg shadow-lg p-6">
        <h2 className="text-xl font-bold text-white mb-4">Top Renewable Regions</h2>
        <div className="space-y-3">
          {aggregated.slice(0, 8).map((item, idx) => (
            <div key={idx} className="flex items-center justify-between">
              <span className="text-slate-300">{item.region}</span>
              <div className="flex items-center gap-3 flex-1 ml-4">
                <div className="w-32 bg-slate-700 rounded-full h-2 overflow-hidden">
                  <div
                    className="bg-gradient-to-r from-green-400 to-blue-400 h-full"
                    style={{ width: `${item.renewable_percentage}%` }}
                  ></div>
                </div>
                <span className="text-green-400 font-semibold min-w-16 text-right">
                  {item.renewable_percentage.toFixed(1)}%
                </span>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}
