import { motion } from 'framer-motion';

export const LoadingSpinner = ({ size = 'md' }) => {
  const sizes = {
    sm: 'w-5 h-5',
    md: 'w-8 h-8',
    lg: 'w-12 h-12',
  };

  return (
    <motion.div
      className={`${sizes[size]} border-4 border-ocean-200 border-t-ocean-600 rounded-full`}
      animate={{ rotate: 360 }}
      transition={{ duration: 1, repeat: Infinity, ease: 'linear' }}
    />
  );
};

export const SkeletonCard = () => (
  <div className="glass-card p-6 animate-pulse">
    <div className="h-4 bg-slate-200 rounded w-3/4 mb-4"></div>
    <div className="h-8 bg-slate-200 rounded w-1/2 mb-4"></div>
    <div className="h-4 bg-slate-200 rounded w-full"></div>
  </div>
);
