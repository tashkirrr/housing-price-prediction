import { useQuery } from '@tanstack/react-query';
import { searchAddress, reverseGeocode } from '../services/geocodingApi';

export const useAddressSearch = (query) => {
  return useQuery({
    queryKey: ['addressSearch', query],
    queryFn: () => searchAddress(query),
    enabled: query.length >= 3,
    staleTime: 1000 * 60 * 5, // 5 minutes
  });
};

export const useReverseGeocode = (lat, lon) => {
  return useQuery({
    queryKey: ['reverseGeocode', lat, lon],
    queryFn: () => reverseGeocode(lat, lon),
    enabled: !!lat && !!lon,
    staleTime: 1000 * 60 * 60, // 1 hour
  });
};
