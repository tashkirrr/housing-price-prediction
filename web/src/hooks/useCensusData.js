import { useQuery } from '@tanstack/react-query';
import { fetchCensusDataForLocation, fetchCaliforniaStats } from '../services/censusApi';

export const useCensusData = (lat, lon) => {
  return useQuery({
    queryKey: ['censusData', lat, lon],
    queryFn: () => fetchCensusDataForLocation(lat, lon),
    enabled: !!lat && !!lon,
    staleTime: 1000 * 60 * 60 * 24, // 24 hours - census data doesn't change often
  });
};

export const useCaliforniaStats = () => {
  return useQuery({
    queryKey: ['californiaStats'],
    queryFn: fetchCaliforniaStats,
    staleTime: 1000 * 60 * 60 * 24,
  });
};
