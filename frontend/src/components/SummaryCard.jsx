import { useSelector } from 'react-redux'

export default function SummaryCard() {
  const summary = useSelector(state => state.data.summary)

  if (!summary) return null

  const cards = [
    {
      title: 'Total Capacity',
      value: `${summary.total_capacity_mw?.toFixed(0)}`,
      unit: 'MW',
      icon: '⚡',
      color: 'from-blue-500 to-blue-600'
    },
    {
      title: 'Renewable %',
      value: `${summary.renewable_percentage?.toFixed(1)}`,
      unit: '%',
      icon: '🌱',
      color: 'from-green-500 to-green-600'
    },
    {
      title: 'Avg Price',
      value: `$${summary.average_price_per_mwh?.toFixed(2)}`,
      unit: '/MWh',
      icon: '💰',
      color: 'from-yellow-500 to-yellow-600'
    },
    {
      title: 'Regions',
      value: summary.regions_count,
      unit: 'Active',
      icon: '🗺️',
      color: 'from-purple-500 to-purple-600'
    },
  ]

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
      {cards.map((card, idx) => (
        <div key={idx} className={`bg-gradient-to-br ${card.color} rounded-lg shadow-lg p-6 text-white`}>
          <div className="flex justify-between items-start">
            <div>
              <p className="text-sm font-medium opacity-90">{card.title}</p>
              <p className="text-3xl font-bold mt-2">{card.value}</p>
              <p className="text-sm opacity-75 mt-1">{card.unit}</p>
            </div>
            <span className="text-3xl">{card.icon}</span>
          </div>
        </div>
      ))}
    </div>
  )
}
