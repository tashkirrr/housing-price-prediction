import { useState, useCallback } from 'react';
import { predictPrice, getPriceRange } from '../services/predictionApi';

export const usePrediction = () => {
  const [result, setResult] = useState(null);
  const [isCalculating, setIsCalculating] = useState(false);

  const calculatePrice = useCallback((features) => {
    setIsCalculating(true);
    
    // Simulate a brief calculation for UX
    setTimeout(() => {
      const prediction = predictPrice(features);
      const range = getPriceRange(prediction.price);
      
      setResult({
        ...prediction,
        range,
      });
      setIsCalculating(false);
    }, 300);
  }, []);

  const resetPrediction = useCallback(() => {
    setResult(null);
    setIsCalculating(false);
  }, []);

  return {
    result,
    isCalculating,
    calculatePrice,
    resetPrediction,
  };
};
