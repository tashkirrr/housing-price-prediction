// Countries page functionality

document.addEventListener('DOMContentLoaded', function() {
    const container = document.getElementById('countriesGrid');
    if (!container) return;
    
    globalData.countries.forEach(country => {
        const cityCount = globalData.cities[country.code]?.length || 0;
        
        const card = document.createElement('a');
        card.className = 'country-card';
        card.href = `explore.html?country=${country.code}`;
        
        card.innerHTML = `
            <h3>${country.name}</h3>
            <div class="stats">
                ${cityCount} cities • Currency: ${country.currency}<br>
                Avg: ${formatCurrency(country.avgPricePerSqft, country.currency)}/sq ft
            </div>
        `;
        
        container.appendChild(card);
    });
});
