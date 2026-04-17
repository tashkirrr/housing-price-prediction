// Prediction page functionality - Realteak Housing Price Predictor

// Web model data (embedded for offline use)
const webModel = {
    "baseline_price": 207194.6937378876,
    "weights": {
        "longitude": -2298.330755899085,
        "latitude": -7208.013843732871,
        "housing_median_age": 5281.170624660533,
        "total_rooms": 6707.655690328134,
        "total_bedrooms": 2484.30901236731,
        "population": -1232.4839444447432,
        "households": 3292.1325285028197,
        "median_income": 34403.76039792789,
        "rooms_per_household": 7597.414487073006,
        "bedrooms_per_room": -12794.007470974933,
        "population_per_household": -1186.8706478067095,
        "distance_to_sf": -2046.588759418886,
        "distance_to_la": -5843.685708060976,
        "income_per_room": 33263.70867701238
    },
    "ocean_multipliers": {
        "<1H OCEAN": 1.1587376159730112,
        "INLAND": 0.6023580515006176,
        "ISLAND": 1.8361474086844956,
        "NEAR BAY": 1.2510567095811367,
        "NEAR OCEAN": 1.2038627675580529
    },
    "feature_means": {
        "longitude": -119.58229045542636,
        "latitude": 35.643149224806194,
        "housing_median_age": 28.60828488372093,
        "total_rooms": 2642.0047843992247,
        "total_bedrooms": 538.4968507751938,
        "population": 1426.453003875969,
        "households": 499.9869186046512,
        "median_income": 3.88075425750969,
        "rooms_per_household": 5.4352350204875295,
        "bedrooms_per_room": 0.21285797439441098,
        "population_per_household": 3.0969611946687525,
        "distance_to_sf": 3.8646218300138138,
        "distance_to_la": 2.6572660252151286,
        "income_per_room": 0.716203651422843
    }
};

document.addEventListener('DOMContentLoaded', function() {
    const countrySelect = document.getElementById('country');
    const citySelect = document.getElementById('city');
    const form = document.getElementById('predictionForm');
    
    // Populate country dropdown
    if (countrySelect) {
        globalData.countries.forEach(country => {
            const option = document.createElement('option');
            option.value = country.code;
            option.textContent = country.name;
            countrySelect.appendChild(option);
        });
    }
    
    // Update cities when country changes
    if (countrySelect && citySelect) {
        countrySelect.addEventListener('change', function() {
            const countryCode = this.value;
            citySelect.innerHTML = '<option value="">Select a city</option>';
            citySelect.disabled = !countryCode;
            
            if (countryCode && globalData.cities[countryCode]) {
                globalData.cities[countryCode].forEach(city => {
                    const option = document.createElement('option');
                    option.value = city.name;
                    option.textContent = city.name;
                    option.dataset.multiplier = city.priceMultiplier;
                    citySelect.appendChild(option);
                });
            }
        });
    }
    
    // Handle form submission
    if (form) {
        form.addEventListener('submit', function(e) {
            e.preventDefault();
            calculatePrice();
        });
    }
});

function calculatePrice() {
    const countryCode = document.getElementById('country').value;
    const city = document.getElementById('city').value;
    const sqft = parseFloat(document.getElementById('sqft').value);
    const bedrooms = parseInt(document.getElementById('bedrooms').value);
    const bathrooms = parseFloat(document.getElementById('bathrooms').value);
    const age = parseInt(document.getElementById('age').value);
    const garage = document.getElementById('garage').checked;
    const pool = document.getElementById('pool').checked;
    
    const country = globalData.countries.find(c => c.code === countryCode);
    const cityData = globalData.cities[countryCode]?.find(c => c.name === city);
    
    if (!country || !cityData) {
        alert('Please select a valid country and city');
        return;
    }
    
    // Calculate base price using location data
    let basePrice = sqft * country.avgPricePerSqft * cityData.priceMultiplier;
    
    // Apply adjustments for property features
    const bedroomBonus = bedrooms * 10000;
    const bathroomBonus = bathrooms * 8000;
    const ageDiscount = Math.max(0, (age - 5) * 0.005 * basePrice);
    const garageBonus = garage ? 15000 : 0;
    const poolBonus = pool ? 25000 : 0;
    
    let estimatedPrice = basePrice + bedroomBonus + bathroomBonus - ageDiscount + garageBonus + poolBonus;
    
    // Calculate range (±15%)
    const minPrice = estimatedPrice * 0.85;
    const maxPrice = estimatedPrice * 1.15;
    
    // Confidence based on data quality
    let confidence = 'Medium';
    let confidenceText = 'Based on available market data';
    
    if (['US', 'CA', 'GB', 'AU', 'DE'].includes(countryCode)) {
        confidence = 'High';
        confidenceText = 'Based on comprehensive market data';
    } else if (['IN', 'BR', 'MX', 'TH'].includes(countryCode)) {
        confidence = 'Medium-Low';
        confidenceText = 'Based on limited market data';
    }
    
    // Display results
    document.getElementById('priceDisplay').textContent = formatCurrency(Math.round(estimatedPrice), country.currency);
    document.getElementById('priceRange').textContent = `Range: ${formatCurrency(Math.round(minPrice), country.currency)} - ${formatCurrency(Math.round(maxPrice), country.currency)}`;
    document.getElementById('confidence').textContent = `${confidence} Confidence - ${confidenceText}`;
    
    // Market context
    const avgPrice = country.avgPricePerSqft * sqft * cityData.priceMultiplier;
    const diff = ((estimatedPrice - avgPrice) / avgPrice * 100).toFixed(1);
    const diffText = diff > 0 ? `${diff}% above` : `${Math.abs(diff)}% below`;
    
    document.getElementById('marketContext').innerHTML = `
        <hr style="margin: 1rem 0; border: none; border-top: 1px solid #e2e8f0;">
        <p><strong>Market Comparison:</strong> Your estimate is ${diffText} the average for ${city}</p>
        <p style="margin-top: 0.5rem; font-size: 0.875rem; color: #64748b;">
            Average price per sq ft in ${city}: ${formatCurrency(Math.round(country.avgPricePerSqft * cityData.priceMultiplier), country.currency)}
        </p>
    `;
    
    // Show results
    document.getElementById('resultSection').classList.remove('hidden');
    document.getElementById('predictionForm').classList.add('hidden');
}

function resetForm() {
    document.getElementById('predictionForm').reset();
    document.getElementById('predictionForm').classList.remove('hidden');
    document.getElementById('resultSection').classList.add('hidden');
    document.getElementById('city').disabled = true;
    document.getElementById('city').innerHTML = '<option value="">First select a country</option>';
}
