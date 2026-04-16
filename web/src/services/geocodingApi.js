import axios from 'axios';

const NOMINATIM_BASE_URL = 'https://nominatim.openstreetmap.org';

const geocodingApi = axios.create({
  baseURL: NOMINATIM_BASE_URL,
  headers: {
    'User-Agent': 'CaliforniaHousingPredictor/2.0 (tashkirrr@example.com)',
  },
});

export const searchAddress = async (query) => {
  if (!query || query.length < 3) return [];
  
  try {
    const response = await geocodingApi.get('/search', {
      params: {
        q: query + ', California, USA',
        format: 'json',
        limit: 5,
        addressdetails: 1,
        countrycodes: 'us',
      },
    });
    
    return response.data.map(item => ({
      id: item.place_id,
      name: item.display_name.split(',')[0],
      fullAddress: item.display_name,
      lat: parseFloat(item.lat),
      lon: parseFloat(item.lon),
      type: item.type,
    }));
  } catch (error) {
    console.error('Geocoding error:', error);
    return [];
  }
};

export const reverseGeocode = async (lat, lon) => {
  try {
    const response = await geocodingApi.get('/reverse', {
      params: {
        lat,
        lon,
        format: 'json',
      },
    });
    
    return {
      address: response.data.display_name,
      city: response.data.address?.city || response.data.address?.town || response.data.address?.village,
      county: response.data.address?.county,
    };
  } catch (error) {
    console.error('Reverse geocoding error:', error);
    return null;
  }
};
