// Explore page functionality

document.addEventListener('DOMContentLoaded', function() {
    const searchInput = document.getElementById('searchInput');
    const initialSearch = new URLSearchParams(window.location.search).get('search');
    if (searchInput && initialSearch) {
        searchInput.value = initialSearch;
    }

    const regionFilter = document.getElementById('regionFilter');
    if (regionFilter) {
        regionFilter.addEventListener('change', searchLocations);
    }

    if (searchInput) {
        searchInput.addEventListener('input', searchLocations);
        searchInput.addEventListener('keydown', function(event) {
            if (event.key === 'Enter') {
                event.preventDefault();
                searchLocations();
            }
        });
    }

    searchLocations();
});

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
    const searchInput = document.getElementById('searchInput');
    const regionFilter = document.getElementById('regionFilter');
    const searchTerm = searchInput ? searchInput.value.trim().toLowerCase() : '';
    const selectedRegion = regionFilter ? regionFilter.value : '';
    const container = document.getElementById('resultsContainer');
    const noResults = document.getElementById('noResults');
    
    if (!container) return;
    
    container.innerHTML = '';
    let hasResults = false;
    
    Object.keys(globalData.cities).forEach(countryCode => {
        const country = globalData.countries.find(c => c.code === countryCode);
        if (!country) return;
        if (selectedRegion && country.region !== selectedRegion) return;
        
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
