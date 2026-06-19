import { useSelector } from 'react-redux'

export default function Header({ currentView, onViewChange }) {
  const summary = useSelector(state => state.data.summary)

  return (
    <header className="bg-slate-900 border-b border-slate-700 shadow-lg">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
        <div className="flex justify-between items-center">
          <div>
            <h1 className="text-3xl font-bold text-white">🔌 Power Grid Dashboard</h1>
            <p className="text-slate-400 mt-1">US Energy Real-time Monitoring System</p>
          </div>
          <div className="flex items-center gap-4">
            <div className="flex gap-2">
              <button
                onClick={() => onViewChange('dashboard')}
                className={`px-4 py-2 rounded-lg font-medium transition-colors ${
                  currentView === 'dashboard'
                    ? 'bg-blue-600 text-white'
                    : 'bg-slate-700 text-slate-300 hover:bg-slate-600'
                }`}
              >
                Dashboard
              </button>
              <button
                onClick={() => onViewChange('analytics')}
                className={`px-4 py-2 rounded-lg font-medium transition-colors ${
                  currentView === 'analytics'
                    ? 'bg-blue-600 text-white'
                    : 'bg-slate-700 text-slate-300 hover:bg-slate-600'
                }`}
              >
                Analytics
              </button>
            </div>
            {summary && (
              <div className="text-right">
                <p className="text-slate-300 text-sm">
                  Updated: <span className="text-white font-semibold">{new Date(summary.last_update).toLocaleString()}</span>
                </p>
              </div>
            )}
          </div>
        </div>
      </div>
    </header>
  )
}
