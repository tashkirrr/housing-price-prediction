// Prediction page functionality

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
    const income = parseFloat(document.getElementById('income').value) || 50000;
    
    const country = globalData.countries.find(c => c.code === countryCode);
    const cityData = globalData.cities[countryCode]?.find(c => c.name === city);
    
    if (!country || !cityData) return;
    
    // Base price calculation
    let basePrice = sqft * country.avgPricePerSqft * cityData.priceMultiplier;
    
    // Adjustments
    const bedroomBonus = bedrooms * 10000;
    const bathroomBonus = bathrooms * 8000;
    const ageDiscount = Math.max(0, (age - 5) * 0.005 * basePrice);
    const garageBonus = garage ? 15000 : 0;
    const poolBonus = pool ? 25000 : 0;
    const incomeFactor = (income / 50000) * 0.2;
    
    let estimatedPrice = basePrice + bedroomBonus + bathroomBonus - ageDiscount + garageBonus + poolBonus;
    estimatedPrice = estimatedPrice * (1 + incomeFactor);
    
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
