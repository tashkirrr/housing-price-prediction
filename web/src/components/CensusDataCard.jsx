import { motion } from 'framer-motion';
import { DollarSign, Users, Home, MapPin } from 'lucide-react';
import { useCensusData } from '../hooks/useCensusData';
import { LoadingSpinner } from './LoadingSpinner';

export const CensusDataCard = ({ lat, lon }) => {
  const { data: censusData, isLoading } = useCensusData(lat, lon);

  if (isLoading) {
    return (
      <div className="glass-card p-6">
        <div className="flex items-center justify-center py-8">
          <LoadingSpinner />
        </div>
      </div>
    );
  }

  if (!censusData) {
    return (
      <div className="glass-card p-6 text-center text-slate-500">
        <MapPin className="w-8 h-8 mx-auto mb-2 opacity-50" />
        <p>Select a location to see Census data</p>
      </div>
    );
  }

  const formatCurrency = (value) => {
    if (!value) return 'N/A';
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD',
      maximumFractionDigits: 0,
    }).format(value);
  };

  const formatNumber = (value) => {
    if (!value) return 'N/A';
    return new Intl.NumberFormat('en-US').format(value);
  };

  const stats = [
    {
      icon: DollarSign,
      label: 'Median Income',
      value: formatCurrency(censusData.medianIncome),
      color: 'text-green-600',
      bg: 'bg-green-100',
    },
    {
      icon: Home,
      label: 'Median Home Value',
      value: formatCurrency(censusData.medianHomeValue),
      color: 'text-ocean-600',
      bg: 'bg-ocean-100',
    },
    {
      icon: Users,
      label: 'Population',
      value: formatNumber(censusData.totalPopulation),
      color: 'text-purple-600',
      bg: 'bg-purple-100',
    },
  ];

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className="glass-card p-6"
    >
      <div className="flex items-center gap-2 mb-4">
        <MapPin className="w-5 h-5 text-ocean-600" />
        <h3 className="font-semibold text-slate-800">Census Data: {censusData.county}</h3>
      </div>

      <div className="space-y-4">
        {stats.map((stat) => (
          <div key={stat.label} className="flex items-center gap-4 p-3 bg-slate-50 rounded-xl">
            <div className={`w-10 h-10 ${stat.bg} rounded-lg flex items-center justify-center`}>
              <stat.icon className={`w-5 h-5 ${stat.color}`} />
            </div>
            <div>
              <div className="text-sm text-slate-500">{stat.label}</div>
              <div className="font-semibold text-slate-800">{stat.value}</div>
            </div>
          </div>
        ))}
      </div>

      <p className="mt-4 text-xs text-slate-400">
        Data from US Census Bureau American Community Survey 2022
      </p>
    </motion.div>
  );
};
