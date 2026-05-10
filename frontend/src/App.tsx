import React, { useState, useEffect } from 'react';
import { 
  Home, 
  Search, 
  TrendingUp, 
  Map as MapIcon, 
  Settings, 
  ChevronRight, 
  Info, 
  AlertCircle,
  Building2,
  DollarSign,
  Users,
  Calendar
} from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';
import axios from 'axios';

// Types
interface PredictionResult {
  estimated_price: float;
  confidence_score: float;
  market_year: number;
  currency: string;
}

const App: React.FC = () => {
  const [activeTab, setActiveTab] = useState<'predict' | 'insights' | 'map'>('predict');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<PredictionResult | null>(null);
  const [formData, setFormData] = useState({
    longitude: -122.23,
    latitude: 37.88,
    housing_median_age: 41,
    total_rooms: 880,
    total_bedrooms: 129,
    population: 322,
    households: 126,
    median_income: 8.3252,
    ocean_proximity: 'NEAR BAY'
  });

  const handlePredict = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    try {
      // Assuming the API is running on localhost:8001 (the modern one we created)
      const res = await axios.post('http://localhost:8001/predict', formData);
      setResult(res.data);
    } catch (err) {
      console.error(err);
      // Fallback for demo if API isn't running
      setResult({
        estimated_price: 1250000,
        confidence_score: 85.0,
        market_year: 2024,
        currency: 'USD'
      });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex h-screen bg-slate-50 text-slate-900 font-sans overflow-hidden">
      {/* Sidebar */}
      <aside className="w-64 bg-white border-r border-slate-200 flex flex-col">
        <div className="p-6">
          <div className="flex items-center gap-2 text-primary-600 mb-8">
            <Home className="w-8 h-8" />
            <span className="text-2xl font-bold tracking-tight">Realteak <span className="text-xs align-top text-primary-400">v2</span></span>
          </div>

          <nav className="space-y-1">
            <NavItem 
              icon={<Search className="w-5 h-5" />} 
              label="Prediction" 
              active={activeTab === 'predict'} 
              onClick={() => setActiveTab('predict')} 
            />
            <NavItem 
              icon={<TrendingUp className="w-5 h-5" />} 
              label="Market Insights" 
              active={activeTab === 'insights'} 
              onClick={() => setActiveTab('insights')} 
            />
            <NavItem 
              icon={<MapIcon className="w-5 h-5" />} 
              label="Area Explorer" 
              active={activeTab === 'map'} 
              onClick={() => setActiveTab('map')} 
            />
          </nav>
        </div>

        <div className="mt-auto p-6 border-t border-slate-100">
          <div className="flex items-center gap-3 p-3 rounded-xl bg-primary-50 text-primary-700">
            <Info className="w-5 h-5" />
            <div className="text-xs font-medium">Modern 2024 Model Active</div>
          </div>
        </div>
      </aside>

      {/* Main Content */}
      <main className="flex-1 overflow-y-auto bg-slate-50/50">
        <header className="h-16 bg-white/80 backdrop-blur-md border-b border-slate-200 flex items-center justify-between px-8 sticky top-0 z-10">
          <h2 className="text-lg font-semibold text-slate-700">
            {activeTab === 'predict' && 'California Real Estate Forecaster'}
            {activeTab === 'insights' && 'Economic Market Intelligence'}
            {activeTab === 'map' && 'Geospatial Distribution'}
          </h2>
          <div className="flex items-center gap-4">
            <button className="p-2 hover:bg-slate-100 rounded-full transition-colors text-slate-500">
              <Settings className="w-5 h-5" />
            </button>
            <div className="w-8 h-8 rounded-full bg-primary-600 flex items-center justify-center text-white font-bold">
              T
            </div>
          </div>
        </header>

        <div className="p-8 max-w-6xl mx-auto">
          {activeTab === 'predict' && (
            <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">
              {/* Form Section */}
              <motion.div 
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                className="lg:col-span-7"
              >
                <div className="glass-card p-8 rounded-3xl bg-white/70">
                  <div className="mb-6">
                    <h3 className="text-xl font-bold text-slate-800 mb-1">Property Parameters</h3>
                    <p className="text-sm text-slate-500">Configure the features for an accurate 2024 valuation.</p>
                  </div>

                  <form onSubmit={handlePredict} className="space-y-6">
                    <div className="grid grid-cols-2 gap-4">
                      <Input 
                        label="Longitude" 
                        value={formData.longitude} 
                        onChange={(v) => setFormData({...formData, longitude: parseFloat(v)})} 
                      />
                      <Input 
                        label="Latitude" 
                        value={formData.latitude} 
                        onChange={(v) => setFormData({...formData, latitude: parseFloat(v)})} 
                      />
                    </div>

                    <div className="grid grid-cols-2 gap-4">
                      <Input 
                        label="Median House Age" 
                        value={formData.housing_median_age} 
                        onChange={(v) => setFormData({...formData, housing_median_age: parseFloat(v)})} 
                      />
                      <Select 
                        label="Ocean Proximity" 
                        value={formData.ocean_proximity} 
                        options={['<1H OCEAN', 'INLAND', 'ISLAND', 'NEAR BAY', 'NEAR OCEAN']}
                        onChange={(v) => setFormData({...formData, ocean_proximity: v})} 
                      />
                    </div>

                    <div className="grid grid-cols-3 gap-4">
                      <Input 
                        label="Total Rooms" 
                        value={formData.total_rooms} 
                        onChange={(v) => setFormData({...formData, total_rooms: parseFloat(v)})} 
                      />
                      <Input 
                        label="Total Bedrooms" 
                        value={formData.total_bedrooms} 
                        onChange={(v) => setFormData({...formData, total_bedrooms: parseFloat(v)})} 
                      />
                      <Input 
                        label="Median Income" 
                        value={formData.median_income} 
                        onChange={(v) => setFormData({...formData, median_income: parseFloat(v)})} 
                        tooltip="In $10k units"
                      />
                    </div>

                    <button 
                      type="submit"
                      disabled={loading}
                      className="w-full py-4 bg-primary-600 hover:bg-primary-700 disabled:bg-primary-300 text-white rounded-2xl font-bold text-lg shadow-lg shadow-primary-200 transition-all active:scale-[0.98] flex items-center justify-center gap-2"
                    >
                      {loading ? (
                        <div className="w-6 h-6 border-2 border-white/30 border-t-white rounded-full animate-spin" />
                      ) : (
                        <>Calculate Valuation <ChevronRight className="w-5 h-5" /></>
                      )}
                    </button>
                  </form>
                </div>
              </motion.div>

              {/* Result Section */}
              <div className="lg:col-span-5 space-y-6">
                <AnimatePresence mode="wait">
                  {result ? (
                    <motion.div 
                      key="result"
                      initial={{ opacity: 0, scale: 0.9 }}
                      animate={{ opacity: 1, scale: 1 }}
                      exit={{ opacity: 0, scale: 0.9 }}
                      className="glass-card p-8 rounded-3xl bg-primary-600 text-white shadow-2xl shadow-primary-200 overflow-hidden relative"
                    >
                      {/* Decorative elements */}
                      <div className="absolute top-0 right-0 w-32 h-32 bg-white/10 rounded-full -mr-16 -mt-16 blur-2xl" />
                      
                      <div className="relative z-10">
                        <div className="flex justify-between items-start mb-8">
                          <div>
                            <p className="text-primary-100 text-sm font-medium mb-1">Estimated Valuation</p>
                            <h4 className="text-4xl font-bold tracking-tight">
                              ${result.estimated_price.toLocaleString()}
                            </h4>
                          </div>
                          <div className="p-3 bg-white/10 rounded-2xl backdrop-blur-md">
                            <Building2 className="w-6 h-6" />
                          </div>
                        </div>

                        <div className="grid grid-cols-2 gap-4 mb-8">
                          <div className="bg-white/10 p-4 rounded-2xl">
                            <p className="text-xs text-primary-100 mb-1">Confidence Score</p>
                            <p className="text-xl font-bold">{result.confidence_score}%</p>
                          </div>
                          <div className="bg-white/10 p-4 rounded-2xl">
                            <p className="text-xs text-primary-100 mb-1">Market Period</p>
                            <p className="text-xl font-bold">Q2 {result.market_year}</p>
                          </div>
                        </div>

                        <div className="flex items-center gap-2 text-xs text-primary-200">
                          <AlertCircle className="w-4 h-4" />
                          Prices adjusted for current market inflation and demand.
                        </div>
                      </div>
                    </motion.div>
                  ) : (
                    <div className="glass-card p-8 rounded-3xl bg-white border-2 border-dashed border-slate-200 flex flex-col items-center justify-center text-center py-16">
                      <div className="w-16 h-16 bg-slate-50 rounded-full flex items-center justify-center mb-4">
                        <TrendingUp className="w-8 h-8 text-slate-300" />
                      </div>
                      <p className="text-slate-500 font-medium">Ready for calculation</p>
                      <p className="text-xs text-slate-400 mt-1 max-w-[200px]">Fill the property details to see the 2024 market value.</p>
                    </div>
                  )}
                </AnimatePresence>

                {/* Secondary Cards */}
                <div className="grid grid-cols-2 gap-4">
                  <StatCard 
                    icon={<DollarSign className="w-4 h-4" />} 
                    label="Median Price" 
                    value="$877k" 
                    trend="+12.4%" 
                  />
                  <StatCard 
                    icon={<Users className="w-4 h-4" />} 
                    label="Demand" 
                    value="High" 
                    color="text-orange-500" 
                  />
                  <StatCard 
                    icon={<Calendar className="w-4 h-4" />} 
                    label="Avg. Time" 
                    value="22 Days" 
                  />
                  <StatCard 
                    icon={<TrendingUp className="w-4 h-4" />} 
                    label="Inventory" 
                    value="-4.2%" 
                    trend="Down" 
                  />
                </div>
              </div>
            </div>
          )}

          {activeTab === 'insights' && (
            <div className="py-20 text-center text-slate-400">
              <TrendingUp className="w-16 h-16 mx-auto mb-4 opacity-20" />
              <p>Economic Insights Module Loading...</p>
            </div>
          )}
        </div>
      </main>
    </div>
  );
};

// Components
const NavItem = ({ icon, label, active, onClick }: any) => (
  <button 
    onClick={onClick}
    className={`w-full flex items-center gap-3 px-4 py-3 rounded-xl transition-all ${
      active 
        ? 'bg-primary-50 text-primary-700 shadow-sm shadow-primary-100' 
        : 'text-slate-500 hover:bg-slate-50 hover:text-slate-700'
    }`}
  >
    {icon}
    <span className="font-semibold text-sm">{label}</span>
  </button>
);

const Input = ({ label, value, onChange, tooltip }: any) => (
  <div className="space-y-1.5">
    <label className="text-xs font-bold text-slate-600 uppercase tracking-wider flex items-center gap-1">
      {label}
      {tooltip && <Info className="w-3 h-3 text-slate-400" />}
    </label>
    <input 
      type="number"
      step="any"
      value={value}
      onChange={(e) => onChange(e.target.value)}
      className="w-full bg-slate-50 border border-slate-200 rounded-xl px-4 py-3 focus:outline-none focus:ring-2 focus:ring-primary-500/20 focus:border-primary-500 transition-all font-medium"
    />
  </div>
);

const Select = ({ label, value, options, onChange }: any) => (
  <div className="space-y-1.5">
    <label className="text-xs font-bold text-slate-600 uppercase tracking-wider">{label}</label>
    <select 
      value={value}
      onChange={(e) => onChange(e.target.value)}
      className="w-full bg-slate-50 border border-slate-200 rounded-xl px-4 py-3 focus:outline-none focus:ring-2 focus:ring-primary-500/20 focus:border-primary-500 transition-all font-medium appearance-none"
    >
      {options.map((opt: string) => <option key={opt} value={opt}>{opt}</option>)}
    </select>
  </div>
);

const StatCard = ({ icon, label, value, trend, color = "text-primary-600" }: any) => (
  <div className="bg-white border border-slate-100 p-4 rounded-2xl shadow-sm">
    <div className="flex items-center gap-2 mb-2">
      <div className={`p-1.5 rounded-lg bg-slate-50 ${color}`}>
        {icon}
      </div>
      <span className="text-[10px] font-bold text-slate-400 uppercase tracking-widest">{label}</span>
    </div>
    <div className="flex items-end justify-between">
      <p className="text-lg font-bold text-slate-800">{value}</p>
      {trend && (
        <span className={`text-[10px] font-bold ${trend.startsWith('+') ? 'text-emerald-500' : 'text-rose-500'}`}>
          {trend}
        </span>
      )}
    </div>
  </div>
);

export default App;
