import { motion } from 'framer-motion';
import { TrendingUp, TrendingDown, Minus, DollarSign } from 'lucide-react';

export const PriceDisplay = ({ price, range, confidence, isLoading }) => {
  if (isLoading) {
    return (
      <div className="glass-card bg-gradient-to-br from-ocean-600 to-teal-600 p-8 text-center">
        <div className="animate-pulse">
          <div className="h-4 bg-white/20 rounded w-32 mx-auto mb-4"></div>
          <div className="h-16 bg-white/20 rounded w-48 mx-auto mb-4"></div>
          <div className="h-4 bg-white/20 rounded w-24 mx-auto"></div>
        </div>
      </div>
    );
  }

  const formatPrice = (value) => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD',
      maximumFractionDigits: 0,
    }).format(value);
  };

  return (
    <motion.div
      initial={{ opacity: 0, scale: 0.95 }}
      animate={{ opacity: 1, scale: 1 }}
      className="glass-card bg-gradient-to-br from-ocean-600 to-teal-600 p-8 text-white overflow-hidden relative"
    >
      {/* Background decoration */}
      <div className="absolute top-0 right-0 w-64 h-64 bg-white/10 rounded-full -translate-y-1/2 translate-x-1/2 blur-3xl"></div>
      <div className="absolute bottom-0 left-0 w-48 h-48 bg-teal-400/20 rounded-full translate-y-1/2 -translate-x-1/2 blur-2xl"></div>

      <div className="relative z-10">
        <div className="flex items-center justify-center gap-2 text-white/80 mb-2">
          <DollarSign className="w-5 h-5" />
          <span className="text-sm font-medium uppercase tracking-wider">Estimated Value</span>
        </div>

        <motion.div
          key={price}
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="text-5xl md:text-6xl font-bold font-display mb-4"
        >
          {formatPrice(price)}
        </motion.div>

        <div className="flex items-center justify-center gap-4 text-white/70 text-sm mb-4">
          <span>Range: {formatPrice(range.low)} - {formatPrice(range.high)}</span>
        </div>

        <div className="inline-flex items-center gap-2 px-4 py-2 bg-white/20 rounded-full text-sm">
          <div className="w-2 h-2 bg-teal-400 rounded-full animate-pulse"></div>
          {confidence * 100}% Confidence
        </div>

        <div className="mt-6 pt-6 border-t border-white/20">
          <p className="text-sm text-white/70">
            Based on 1990 census data. For current estimates, multiply by ~2.5x
          </p>
        </div>
      </div>
    </motion.div>
  );
};
