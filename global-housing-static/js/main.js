// Global Housing Predictor - Main JavaScript

// Mobile navigation toggle
function toggleNav() {
    const navLinks = document.getElementById('navLinks');
    navLinks.classList.toggle('active');
}

// Global data for countries and cities
const globalData = {
    countries: [
        { code: 'US', name: 'United States', currency: 'USD', avgPricePerSqft: 250 },
        { code: 'CA', name: 'Canada', currency: 'CAD', avgPricePerSqft: 300 },
        { code: 'GB', name: 'United Kingdom', currency: 'GBP', avgPricePerSqft: 450 },
        { code: 'AU', name: 'Australia', currency: 'AUD', avgPricePerSqft: 350 },
        { code: 'DE', name: 'Germany', currency: 'EUR', avgPricePerSqft: 280 },
        { code: 'FR', name: 'France', currency: 'EUR', avgPricePerSqft: 320 },
        { code: 'JP', name: 'Japan', currency: 'JPY', avgPricePerSqft: 400 },
        { code: 'SG', name: 'Singapore', currency: 'SGD', avgPricePerSqft: 1200 },
        { code: 'IN', name: 'India', currency: 'INR', avgPricePerSqft: 80 },
        { code: 'BR', name: 'Brazil', currency: 'BRL', avgPricePerSqft: 60 },
        { code: 'MX', name: 'Mexico', currency: 'MXN', avgPricePerSqft: 50 },
        { code: 'ES', name: 'Spain', currency: 'EUR', avgPricePerSqft: 180 },
        { code: 'IT', name: 'Italy', currency: 'EUR', avgPricePerSqft: 170 },
        { code: 'NL', name: 'Netherlands', currency: 'EUR', avgPricePerSqft: 290 },
        { code: 'SE', name: 'Sweden', currency: 'SEK', avgPricePerSqft: 220 },
        { code: 'CH', name: 'Switzerland', currency: 'CHF', avgPricePerSqft: 550 },
        { code: 'AE', name: 'UAE', currency: 'AED', avgPricePerSqft: 350 },
        { code: 'CN', name: 'China', currency: 'CNY', avgPricePerSqft: 150 },
        { code: 'KR', name: 'South Korea', currency: 'KRW', avgPricePerSqft: 200 },
        { code: 'TH', name: 'Thailand', currency: 'THB', avgPricePerSqft: 70 },
    ],
    
    cities: {
        'US': [
            { name: 'New York', priceMultiplier: 2.5 },
            { name: 'Los Angeles', priceMultiplier: 2.0 },
            { name: 'San Francisco', priceMultiplier: 3.0 },
            { name: 'Chicago', priceMultiplier: 1.3 },
            { name: 'Boston', priceMultiplier: 1.8 },
            { name: 'Seattle', priceMultiplier: 1.6 },
            { name: 'Miami', priceMultiplier: 1.4 },
            { name: 'Austin', priceMultiplier: 1.2 },
            { name: 'Denver', priceMultiplier: 1.1 },
            { name: 'Atlanta', priceMultiplier: 0.9 },
        ],
        'CA': [
            { name: 'Toronto', priceMultiplier: 1.8 },
            { name: 'Vancouver', priceMultiplier: 2.0 },
            { name: 'Montreal', priceMultiplier: 1.0 },
            { name: 'Calgary', priceMultiplier: 0.8 },
            { name: 'Ottawa', priceMultiplier: 0.9 },
        ],
        'GB': [
            { name: 'London', priceMultiplier: 2.5 },
            { name: 'Manchester', priceMultiplier: 0.9 },
            { name: 'Birmingham', priceMultiplier: 0.8 },
            { name: 'Edinburgh', priceMultiplier: 1.0 },
            { name: 'Glasgow', priceMultiplier: 0.7 },
        ],
        'AU': [
            { name: 'Sydney', priceMultiplier: 2.2 },
            { name: 'Melbourne', priceMultiplier: 1.8 },
            { name: 'Brisbane', priceMultiplier: 1.2 },
            { name: 'Perth', priceMultiplier: 1.0 },
            { name: 'Adelaide', priceMultiplier: 0.9 },
        ],
        'DE': [
            { name: 'Berlin', priceMultiplier: 1.2 },
            { name: 'Munich', priceMultiplier: 1.8 },
            { name: 'Hamburg', priceMultiplier: 1.3 },
            { name: 'Frankfurt', priceMultiplier: 1.4 },
            { name: 'Cologne', priceMultiplier: 1.0 },
        ],
        'FR': [
            { name: 'Paris', priceMultiplier: 2.8 },
            { name: 'Lyon', priceMultiplier: 1.1 },
            { name: 'Marseille', priceMultiplier: 0.9 },
            { name: 'Nice', priceMultiplier: 1.5 },
            { name: 'Toulouse', priceMultiplier: 0.8 },
        ],
        'JP': [
            { name: 'Tokyo', priceMultiplier: 2.0 },
            { name: 'Osaka', priceMultiplier: 1.1 },
            { name: 'Yokohama', priceMultiplier: 1.2 },
            { name: 'Nagoya', priceMultiplier: 0.9 },
            { name: 'Fukuoka', priceMultiplier: 0.8 },
        ],
        'SG': [
            { name: 'Singapore', priceMultiplier: 1.0 },
        ],
        'IN': [
            { name: 'Mumbai', priceMultiplier: 1.5 },
            { name: 'Delhi', priceMultiplier: 1.0 },
            { name: 'Bangalore', priceMultiplier: 1.1 },
            { name: 'Hyderabad', priceMultiplier: 0.8 },
            { name: 'Chennai', priceMultiplier: 0.8 },
        ],
        'BR': [
            { name: 'Sao Paulo', priceMultiplier: 1.2 },
            { name: 'Rio de Janeiro', priceMultiplier: 1.1 },
            { name: 'Brasilia', priceMultiplier: 0.9 },
            { name: 'Salvador', priceMultiplier: 0.7 },
            { name: 'Fortaleza', priceMultiplier: 0.6 },
        ],
        'MX': [
            { name: 'Mexico City', priceMultiplier: 1.2 },
            { name: 'Guadalajara', priceMultiplier: 0.8 },
            { name: 'Monterrey', priceMultiplier: 0.9 },
            { name: 'Cancun', priceMultiplier: 1.0 },
            { name: 'Tijuana', priceMultiplier: 0.7 },
        ],
        'ES': [
            { name: 'Madrid', priceMultiplier: 1.4 },
            { name: 'Barcelona', priceMultiplier: 1.5 },
            { name: 'Valencia', priceMultiplier: 0.9 },
            { name: 'Seville', priceMultiplier: 0.8 },
            { name: 'Malaga', priceMultiplier: 1.0 },
        ],
        'IT': [
            { name: 'Rome', priceMultiplier: 1.3 },
            { name: 'Milan', priceMultiplier: 1.6 },
            { name: 'Naples', priceMultiplier: 0.7 },
            { name: 'Turin', priceMultiplier: 0.8 },
            { name: 'Florence', priceMultiplier: 1.2 },
        ],
        'NL': [
            { name: 'Amsterdam', priceMultiplier: 1.8 },
            { name: 'Rotterdam', priceMultiplier: 1.1 },
            { name: 'The Hague', priceMultiplier: 1.2 },
            { name: 'Utrecht', priceMultiplier: 1.1 },
            { name: 'Eindhoven', priceMultiplier: 0.9 },
        ],
        'SE': [
            { name: 'Stockholm', priceMultiplier: 1.6 },
            { name: 'Gothenburg', priceMultiplier: 1.0 },
            { name: 'Malmö', priceMultiplier: 0.9 },
            { name: 'Uppsala', priceMultiplier: 0.8 },
            { name: 'Linkoping', priceMultiplier: 0.7 },
        ],
        'CH': [
            { name: 'Zurich', priceMultiplier: 1.5 },
            { name: 'Geneva', priceMultiplier: 1.6 },
            { name: 'Basel', priceMultiplier: 1.2 },
            { name: 'Bern', priceMultiplier: 1.0 },
            { name: 'Lausanne', priceMultiplier: 1.3 },
        ],
        'AE': [
            { name: 'Dubai', priceMultiplier: 1.4 },
            { name: 'Abu Dhabi', priceMultiplier: 1.2 },
            { name: 'Sharjah', priceMultiplier: 0.7 },
            { name: 'Ajman', priceMultiplier: 0.5 },
            { name: 'Ras Al Khaimah', priceMultiplier: 0.4 },
        ],
        'CN': [
            { name: 'Shanghai', priceMultiplier: 2.0 },
            { name: 'Beijing', priceMultiplier: 1.8 },
            { name: 'Shenzhen', priceMultiplier: 1.9 },
            { name: 'Guangzhou', priceMultiplier: 1.4 },
            { name: 'Hangzhou', priceMultiplier: 1.3 },
        ],
        'KR': [
            { name: 'Seoul', priceMultiplier: 1.8 },
            { name: 'Busan', priceMultiplier: 1.0 },
            { name: 'Incheon', priceMultiplier: 0.9 },
            { name: 'Daegu', priceMultiplier: 0.7 },
            { name: 'Daejeon', priceMultiplier: 0.7 },
        ],
        'TH': [
            { name: 'Bangkok', priceMultiplier: 1.2 },
            { name: 'Chiang Mai', priceMultiplier: 0.6 },
            { name: 'Phuket', priceMultiplier: 1.0 },
            { name: 'Pattaya', priceMultiplier: 0.7 },
            { name: 'Koh Samui', priceMultiplier: 0.9 },
        ],
    },
    
    // Sample featured markets
    featuredMarkets: [
        { city: 'New York', country: 'US', countryName: 'United States', avgPrice: 625000, trend: 5.2 },
        { city: 'London', country: 'GB', countryName: 'United Kingdom', avgPrice: 750000, trend: 3.1 },
        { city: 'Tokyo', country: 'JP', countryName: 'Japan', avgPrice: 480000, trend: 1.8 },
        { city: 'Sydney', country: 'AU', countryName: 'Australia', avgPrice: 850000, trend: 4.5 },
        { city: 'Paris', country: 'FR', countryName: 'France', avgPrice: 720000, trend: 2.9 },
        { city: 'Singapore', country: 'SG', countryName: 'Singapore', avgPrice: 1200000, trend: 6.1 },
    ]
};

// Currency symbols
const currencySymbols = {
    'USD': '$', 'CAD': 'C$', 'GBP': '£', 'AUD': 'A$',
    'EUR': '€', 'JPY': '¥', 'SGD': 'S$', 'INR': '₹',
    'BRL': 'R$', 'MXN': 'Mex$', 'SEK': 'kr', 'CHF': 'Fr.',
    'AED': 'AED', 'CNY': '¥', 'KRW': '₩', 'THB': '฿'
};

// Format currency
function formatCurrency(amount, currency) {
    const symbol = currencySymbols[currency] || currency;
    return symbol + amount.toLocaleString();
}

// Populate featured markets on homepage
document.addEventListener('DOMContentLoaded', function() {
    const marketsGrid = document.getElementById('marketsGrid');
    if (marketsGrid) {
        globalData.featuredMarkets.forEach(market => {
            const country = globalData.countries.find(c => c.code === market.country);
            const currency = country ? country.currency : 'USD';
            const trendClass = market.trend >= 0 ? 'trend-up' : 'trend-down';
            const trendIcon = market.trend >= 0 ? '↑' : '↓';
            
            const card = document.createElement('div');
            card.className = 'market-card';
            card.innerHTML = `
                <h3>${market.city}</h3>
                <div class="country">${market.countryName}</div>
                <div class="price">${formatCurrency(market.avgPrice, currency)}</div>
                <div class="trend ${trendClass}">
                    ${trendIcon} ${Math.abs(market.trend)}% last year
                </div>
            `;
            marketsGrid.appendChild(card);
        });
    }
});
