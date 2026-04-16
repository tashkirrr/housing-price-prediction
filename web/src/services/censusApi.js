import axios from 'axios';

const CENSUS_BASE_URL = 'https://api.census.gov/data/2022/acs/acs5';
const CENSUS_API_KEY = ''; // Free tier works without key but is rate limited

// California FIPS code is 06
// Common variables we want to fetch
const VARIABLES = {
  medianIncome: 'B19013_001E',      // Median household income
  medianHomeValue: 'B25077_001E',   // Median home value
  totalPopulation: 'B01003_001E',   // Total population
  medianAge: 'B01002_001E',         // Median age
};

export const fetchCensusDataForLocation = async (lat, lon) => {
  try {
    // First, we need to find which census tract this location belongs to
    // For simplicity, we'll use county-level data based on coordinates
    // In a production app, you'd use a geocoding service to get the FIPS codes
    
    // California counties approximate mapping based on coordinates
    const county = getCountyFromCoordinates(lat, lon);
    
    if (!county) {
      return null;
    }

    const response = await axios.get(CENSUS_BASE_URL, {
      params: {
        get: Object.values(VARIABLES).join(','),
        for: `county:${county.fips}`,
        in: 'state:06',
      },
    });

    if (response.data && response.data.length > 1) {
      const data = response.data[1];
      const headers = response.data[0];
      
      return {
        medianIncome: parseInt(data[headers.indexOf(VARIABLES.medianIncome)]) || null,
        medianHomeValue: parseInt(data[headers.indexOf(VARIABLES.medianHomeValue)]) || null,
        totalPopulation: parseInt(data[headers.indexOf(VARIABLES.totalPopulation)]) || null,
        medianAge: parseFloat(data[headers.indexOf(VARIABLES.medianAge)]) || null,
        county: county.name,
      };
    }
    
    return null;
  } catch (error) {
    console.error('Census API error:', error);
    return null;
  }
};

// Simplified county detection based on coordinates
// In production, use a proper geocoding service
const getCountyFromCoordinates = (lat, lon) => {
  // San Francisco Bay Area
  if (lat > 37.2 && lat < 38.0 && lon > -123.0 && lon < -121.5) {
    return { fips: '075', name: 'San Francisco' };
  }
  // Los Angeles Area
  if (lat > 33.5 && lat < 34.5 && lon > -118.8 && lon < -117.5) {
    return { fips: '037', name: 'Los Angeles' };
  }
  // San Diego Area
  if (lat > 32.5 && lat < 33.5 && lon > -117.5 && lon < -116.5) {
    return { fips: '073', name: 'San Diego' };
  }
  // Sacramento Area
  if (lat > 38.3 && lat < 39.0 && lon > -121.8 && lon < -121.0) {
    return { fips: '067', name: 'Sacramento' };
  }
  // Santa Clara (Silicon Valley)
  if (lat > 37.0 && lat < 37.5 && lon > -122.2 && lon < -121.5) {
    return { fips: '085', name: 'Santa Clara' };
  }
  
  // Default to California state average
  return { fips: '*', name: 'California (State Average)' };
};

export const fetchCaliforniaStats = async () => {
  try {
    const response = await axios.get(CENSUS_BASE_URL, {
      params: {
        get: Object.values(VARIABLES).join(','),
        for: 'state:06',
      },
    });

    if (response.data && response.data.length > 1) {
      const data = response.data[1];
      const headers = response.data[0];
      
      return {
        medianIncome: parseInt(data[headers.indexOf(VARIABLES.medianIncome)]) || 80000,
        medianHomeValue: parseInt(data[headers.indexOf(VARIABLES.medianHomeValue)]) || 650000,
        totalPopulation: parseInt(data[headers.indexOf(VARIABLES.totalPopulation)]) || 39500000,
      };
    }
    
    return {
      medianIncome: 80000,
      medianHomeValue: 650000,
      totalPopulation: 39500000,
    };
  } catch (error) {
    console.error('Census API error:', error);
    return {
      medianIncome: 80000,
      medianHomeValue: 650000,
      totalPopulation: 39500000,
    };
  }
};
