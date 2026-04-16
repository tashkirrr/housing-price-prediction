// Explore page functionality

document.addEventListener('DOMContentLoaded', function() {
    const countryFilter = document.getElementById('countryFilter');
    
    // Populate country filter
    if (countryFilter) {
        globalData.countries.forEach(country => {
            const option = document.createElement('option');
            option.value = country.code;
            option.textContent = country.name;
            countryFilter.appendChild(option);
        });
    }
    
    // Initial load of all cities
    displayAllCities();
});

function displayAllCities() {
    const container = document.getElementById('resultsContainer');
    if (!container) return;
    
    container.innerHTML = '';
    
    Object.keys(globalData.cities).forEach(countryCode => {
        const country = globalData.countries.find(c => c.code === countryCode);
        if (!country) return;
        
        globalData.cities[countryCode].forEach(city => {
            const card = createCityCard(city, country);
            container.appendChild(card);
        });
    });
}

function createCityCard(city, country) {
    const avgPrice = country.avgPricePerSqft * city.priceMultiplier * 1000; // Example 1000 sqft property
    
    const card = document.createElement('div');
    card.className = 'market-card';
    card.dataset.city = city.name.toLowerCase();
    card.dataset.country = country.code.toLowerCase();
    card.dataset.countryName = country.name.toLowerCase();
    
    card.innerHTML = `
        <h3>${city.name}</h3>
        <div class="country">${country.name}</div>
        <div class="price">${formatCurrency(Math.round(avgPrice), country.currency)}</div>
        <div style="margin-top: 0.5rem; font-size: 0.875rem; color: #64748b;">
            Avg: ${formatCurrency(Math.round(country.avgPricePerSqft * city.priceMultiplier), country.currency)}/sq ft
        </div>
        <a href="predict.html" style="display: inline-block; margin-top: 1rem; color: #0369a1; text-decoration: none;">
            Get estimate →
        </a>
    `;
    
    return card;
}

function searchLocations() {
    const searchTerm = document.getElementById('searchInput').value.toLowerCase();
    const countryFilter = document.getElementById('countryFilter').value;
    const container = document.getElementById('resultsContainer');
    const noResults = document.getElementById('noResults');
    
    if (!container) return;
    
    container.innerHTML = '';
    let hasResults = false;
    
    Object.keys(globalData.cities).forEach(countryCode => {
        // Skip if country filter is set and doesn't match
        if (countryFilter && countryCode !== countryFilter) return;
        
        const country = globalData.countries.find(c => c.code === countryCode);
        if (!country) return;
        
        globalData.cities[countryCode].forEach(city => {
            const cityMatch = city.name.toLowerCase().includes(searchTerm);
            const countryMatch = country.name.toLowerCase().includes(searchTerm);
            
            if (!searchTerm || cityMatch || countryMatch) {
                const card = createCityCard(city, country);
                container.appendChild(card);
                hasResults = true;
            }
        });
    });
    
    if (noResults) {
        noResults.classList.toggle('hidden', hasResults);
    }
}

// Search on Enter key
document.addEventListener('DOMContentLoaded', function() {
    const searchInput = document.getElementById('searchInput');
    if (searchInput) {
        searchInput.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                searchLocations();
            }
        });
    }
});
