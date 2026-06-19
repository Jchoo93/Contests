import { useSelector } from 'react-redux'
import {
  ScatterChart,
  Scatter,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
  BarChart,
  Bar
} from 'recharts'

export default function PricingChart() {
  const pricing = useSelector(state => state.data.pricing)

  if (!pricing || pricing.length === 0) {
    return <div className="text-center text-slate-400">No pricing data available</div>
  }

  const data = pricing
    .slice(0, 15)
    .map(item => ({
      region: item.region.split('-')[0],
      price: parseFloat(item.price_per_mwh.toFixed(2))
    }))
    .sort((a, b) => b.price - a.price)

  const minPrice = Math.min(...data.map(d => d.price))
  const maxPrice = Math.max(...data.map(d => d.price))

  return (
    <div className="bg-slate-800 rounded-lg shadow-lg p-6">
      <h2 className="text-xl font-bold text-white mb-4">Average Price by Region ($/MWh)</h2>
      <div className="mb-4">
        <div className="flex justify-between text-sm text-slate-300">
          <span>Min: <span className="text-green-400 font-semibold">${minPrice.toFixed(2)}</span></span>
          <span>Max: <span className="text-red-400 font-semibold">${maxPrice.toFixed(2)}</span></span>
          <span>Avg: <span className="text-yellow-400 font-semibold">${(data.reduce((a, b) => a + b.price, 0) / data.length).toFixed(2)}</span></span>
        </div>
      </div>
      <ResponsiveContainer width="100%" height={400}>
        <BarChart data={data}>
          <CartesianGrid strokeDasharray="3 3" stroke="#444" />
          <XAxis dataKey="region" stroke="#999" angle={-45} textAnchor="end" height={80} />
          <YAxis stroke="#999" />
          <Tooltip
            contentStyle={{ backgroundColor: '#1e293b', border: '1px solid #444' }}
            labelStyle={{ color: '#fff' }}
            formatter={(value) => `$${value.toFixed(2)}/MWh`}
          />
          <Bar dataKey="price" fill="#3B82F6" name="Price" />
        </BarChart>
      </ResponsiveContainer>
    </div>
  )
}
