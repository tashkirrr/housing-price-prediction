// ML Model data embedded for client-side prediction
const webModel = {
  baseline_price: 207194.6937378876,
  weights: {
    longitude: -2298.330755899085,
    latitude: -7208.013843732871,
    housing_median_age: 5281.170624660533,
    total_rooms: 6707.655690328134,
    total_bedrooms: 2484.30901236731,
    population: -1232.4839444447432,
    households: 3292.1325285028197,
    median_income: 34403.76039792789,
    rooms_per_household: 7597.414487073006,
    bedrooms_per_room: -12794.007470974933,
    population_per_household: -1186.8706478067095,
    distance_to_sf: -2046.588759418886,
    distance_to_la: -5843.685708060976,
    income_per_room: 33263.70867701238
  },
  ocean_multipliers: {
    "<1H OCEAN": 1.1587376159730112,
    "INLAND": 0.6023580515006176,
    "ISLAND": 1.8361474086844956,
    "NEAR BAY": 1.2510567095811367,
    "NEAR OCEAN": 1.2038627675580529
  },
  feature_means: {
    longitude: -119.58229045542636,
    latitude: 35.643149224806194,
    housing_median_age: 28.60828488372093,
    total_rooms: 2642.0047843992247,
    total_bedrooms: 538.4968507751938,
    population: 1426.453003875969,
    households: 499.9869186046512,
    median_income: 3.88075425750969,
    rooms_per_household: 5.4352350204875295,
    bedrooms_per_room: 0.21285797439441098,
    population_per_household: 3.0969611946687525,
    distance_to_sf: 3.8646218300138138,
    distance_to_la: 2.6572660252151286,
    income_per_room: 0.716203651422843
  }
};

export const predictPrice = (features) => {
  const {
    longitude,
    latitude,
    housing_median_age,
    total_rooms,
    total_bedrooms,
    population,
    households,
    median_income,
    ocean_proximity
  } = features;

  // Calculate engineered features
  const rooms_per_household = total_rooms / Math.max(households, 1);
  const bedrooms_per_room = total_bedrooms / Math.max(total_rooms, 1);
  const population_per_household = population / Math.max(households, 1);
  const distance_to_sf = Math.sqrt(
    Math.pow(latitude - 37.7749, 2) + 
    Math.pow(longitude - (-122.4194), 2)
  );
  const distance_to_la = Math.sqrt(
    Math.pow(latitude - 34.0522, 2) + 
    Math.pow(longitude - (-118.2437), 2)
  );
  const income_per_room = median_income / Math.max(rooms_per_household, 0.1);

  const calculatedFeatures = {
    longitude,
    latitude,
    housing_median_age,
    total_rooms,
    total_bedrooms,
    population,
    households,
    median_income,
    rooms_per_household,
    bedrooms_per_room,
    population_per_household,
    distance_to_sf,
    distance_to_la,
    income_per_room
  };

  // Calculate weighted sum of differences from mean
  let priceAdjustment = 0;
  for (const [feature, value] of Object.entries(calculatedFeatures)) {
    const mean = webModel.feature_means[feature];
    const weight = webModel.weights[feature];
    priceAdjustment += (value - mean) * weight * 0.001;
  }

  // Apply ocean proximity multiplier
  const oceanMultiplier = webModel.ocean_multipliers[ocean_proximity] || 1.0;
  
  // Calculate final price
  let predictedPrice = (webModel.baseline_price + priceAdjustment) * oceanMultiplier;
  
  // Ensure reasonable bounds
  predictedPrice = Math.max(15000, Math.min(500000, predictedPrice));

  return {
    price: Math.round(predictedPrice),
    features: calculatedFeatures,
    confidence: 0.85,
  };
};

export const getPriceRange = (basePrice) => {
  return {
    low: Math.round(basePrice * 0.85),
    high: Math.round(basePrice * 1.15),
  };
};
