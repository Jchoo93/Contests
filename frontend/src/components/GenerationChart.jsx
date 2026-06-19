import { useSelector } from 'react-redux'
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer
} from 'recharts'

export default function GenerationChart() {
  const generation = useSelector(state => state.data.generation)

  if (!generation || generation.length === 0) {
    return <div className="text-center text-slate-400">No generation data available</div>
  }

  const data = generation
    .slice(0, 10)
    .map(item => ({
      region: item.region.split('-')[0],
      solar: item.solar_capacity_mw || 0,
      wind: item.wind_capacity_mw || 0,
      hydro: item.hydro_capacity_mw || 0,
      fossil: item.fossil_capacity_mw || 0,
      nuclear: item.nuclear_capacity_mw || 0,
    }))

  return (
    <div className="bg-slate-800 rounded-lg shadow-lg p-6">
      <h2 className="text-xl font-bold text-white mb-4">Generation Capacity by Source</h2>
      <ResponsiveContainer width="100%" height={400}>
        <BarChart data={data}>
          <CartesianGrid strokeDasharray="3 3" stroke="#444" />
          <XAxis dataKey="region" stroke="#999" />
          <YAxis stroke="#999" />
          <Tooltip
            contentStyle={{ backgroundColor: '#1e293b', border: '1px solid #444' }}
            labelStyle={{ color: '#fff' }}
          />
          <Legend />
          <Bar dataKey="solar" stackId="a" fill="#FFA500" name="Solar" />
          <Bar dataKey="wind" stackId="a" fill="#87CEEB" name="Wind" />
          <Bar dataKey="hydro" stackId="a" fill="#1E90FF" name="Hydro" />
          <Bar dataKey="fossil" stackId="a" fill="#696969" name="Fossil" />
          <Bar dataKey="nuclear" stackId="a" fill="#FFD700" name="Nuclear" />
        </BarChart>
      </ResponsiveContainer>
    </div>
  )
}
