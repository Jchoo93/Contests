import { useEffect } from 'react'
import { useDispatch, useSelector } from 'react-redux'
import Dashboard from './components/Dashboard'
import Header from './components/Header'
import {
  fetchGenerationData,
  fetchPricingData,
  fetchRenewableData,
  fetchSummary
} from './store/slices/dataSlice'

function App() {
  const dispatch = useDispatch()
  const { loading, error } = useSelector(state => state.data)

  useEffect(() => {
    dispatch(fetchGenerationData())
    dispatch(fetchPricingData())
    dispatch(fetchRenewableData())
    dispatch(fetchSummary())

    const interval = setInterval(() => {
      dispatch(fetchGenerationData())
      dispatch(fetchPricingData())
      dispatch(fetchRenewableData())
      dispatch(fetchSummary())
    }, 60000)

    return () => clearInterval(interval)
  }, [dispatch])

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 to-slate-800">
      <Header />
      {error && (
        <div className="bg-red-500/20 border border-red-500 text-red-200 px-4 py-3 rounded">
          {error}
        </div>
      )}
      {loading && (
        <div className="flex justify-center items-center py-20">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-white"></div>
        </div>
      )}
      {!loading && <Dashboard />}
    </div>
  )
}

export default App
