import SummaryCard from './SummaryCard'
import GenerationChart from './GenerationChart'
import PricingChart from './PricingChart'
import RenewableChart from './RenewableChart'

export default function Dashboard() {
  return (
    <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div className="space-y-8">
        {/* Summary Cards */}
        <section>
          <SummaryCard />
        </section>

        {/* Generation Chart */}
        <section>
          <GenerationChart />
        </section>

        {/* Pricing Chart */}
        <section>
          <PricingChart />
        </section>

        {/* Renewable Chart */}
        <section>
          <RenewableChart />
        </section>

        {/* Footer */}
        <footer className="text-center text-slate-400 text-sm py-8 border-t border-slate-700">
          <p>Data updated daily from US Energy Information Administration (EIA)</p>
          <p>Last 24-hour data shown</p>
        </footer>
      </div>
    </main>
  )
}
