// Global Housing Predictor - Main JavaScript

// Mobile navigation toggle
function toggleNav() {
    const navLinks = document.getElementById('navLinks');
    navLinks.classList.toggle('active');
}

// Hero search function
function heroSearch() {
    const location = document.getElementById('heroSearch').value;
    if (location) {
        window.location.href = `explore.html?search=${encodeURIComponent(location)}`;
    } else {
        window.location.href = 'explore.html';
    }
}

// Global data for countries and cities
const globalData = {
    countries: [
        { code: 'US', name: 'United States', currency: 'USD', avgPricePerSqft: 250, region: 'North America' },
        { code: 'CA', name: 'Canada', currency: 'CAD', avgPricePerSqft: 300, region: 'North America' },
        { code: 'GB', name: 'United Kingdom', currency: 'GBP', avgPricePerSqft: 450, region: 'Europe' },
        { code: 'AU', name: 'Australia', currency: 'AUD', avgPricePerSqft: 350, region: 'Asia Pacific' },
        { code: 'DE', name: 'Germany', currency: 'EUR', avgPricePerSqft: 280, region: 'Europe' },
        { code: 'FR', name: 'France', currency: 'EUR', avgPricePerSqft: 320, region: 'Europe' },
        { code: 'JP', name: 'Japan', currency: 'JPY', avgPricePerSqft: 400, region: 'Asia Pacific' },
        { code: 'SG', name: 'Singapore', currency: 'SGD', avgPricePerSqft: 1200, region: 'Asia Pacific' },
        { code: 'IN', name: 'India', currency: 'INR', avgPricePerSqft: 80, region: 'Asia Pacific' },
        { code: 'BR', name: 'Brazil', currency: 'BRL', avgPricePerSqft: 60, region: 'South America' },
        { code: 'MX', name: 'Mexico', currency: 'MXN', avgPricePerSqft: 50, region: 'North America' },
        { code: 'ES', name: 'Spain', currency: 'EUR', avgPricePerSqft: 180, region: 'Europe' },
        { code: 'IT', name: 'Italy', currency: 'EUR', avgPricePerSqft: 170, region: 'Europe' },
        { code: 'NL', name: 'Netherlands', currency: 'EUR', avgPricePerSqft: 290, region: 'Europe' },
        { code: 'SE', name: 'Sweden', currency: 'SEK', avgPricePerSqft: 220, region: 'Europe' },
        { code: 'CH', name: 'Switzerland', currency: 'CHF', avgPricePerSqft: 550, region: 'Europe' },
        { code: 'AE', name: 'UAE', currency: 'AED', avgPricePerSqft: 350, region: 'Middle East' },
        { code: 'CN', name: 'China', currency: 'CNY', avgPricePerSqft: 150, region: 'Asia Pacific' },
        { code: 'KR', name: 'South Korea', currency: 'KRW', avgPricePerSqft: 200, region: 'Asia Pacific' },
        { code: 'TH', name: 'Thailand', currency: 'THB', avgPricePerSqft: 70, region: 'Asia Pacific' },
    ],
    
    cities: {
        'US': [
            { name: 'New York', priceMultiplier: 2.5, emoji: '🗽' },
            { name: 'Los Angeles', priceMultiplier: 2.0, emoji: '🌴' },
            { name: 'San Francisco', priceMultiplier: 3.0, emoji: '🌉' },
            { name: 'Chicago', priceMultiplier: 1.3, emoji: '🏙️' },
            { name: 'Boston', priceMultiplier: 1.8, emoji: '🎓' },
            { name: 'Seattle', priceMultiplier: 1.6, emoji: '☕' },
            { name: 'Miami', priceMultiplier: 1.4, emoji: '🏖️' },
            { name: 'Austin', priceMultiplier: 1.2, emoji: '🎸' },
        ],
        'CA': [
            { name: 'Toronto', priceMultiplier: 1.8, emoji: '🍁' },
            { name: 'Vancouver', priceMultiplier: 2.0, emoji: '🏔️' },
            { name: 'Montreal', priceMultiplier: 1.0, emoji: '🥖' },
            { name: 'Calgary', priceMultiplier: 0.8, emoji: '🛢️' },
        ],
        'GB': [
            { name: 'London', priceMultiplier: 2.5, emoji: '💂' },
            { name: 'Manchester', priceMultiplier: 0.9, emoji: '⚽' },
            { name: 'Birmingham', priceMultiplier: 0.8, emoji: '🏭' },
            { name: 'Edinburgh', priceMultiplier: 1.0, emoji: '🏰' },
        ],
        'AU': [
            { name: 'Sydney', priceMultiplier: 2.2, emoji: '🦘' },
            { name: 'Melbourne', priceMultiplier: 1.8, emoji: '🎭' },
            { name: 'Brisbane', priceMultiplier: 1.2, emoji: '☀️' },
            { name: 'Perth', priceMultiplier: 1.0, emoji: '🏖️' },
        ],
        'DE': [
            { name: 'Berlin', priceMultiplier: 1.2, emoji: '🍺' },
            { name: 'Munich', priceMultiplier: 1.8, emoji: '🥨' },
            { name: 'Hamburg', priceMultiplier: 1.3, emoji: '⚓' },
            { name: 'Frankfurt', priceMultiplier: 1.4, emoji: '🏦' },
        ],
        'FR': [
            { name: 'Paris', priceMultiplier: 2.8, emoji: '🗼' },
            { name: 'Lyon', priceMultiplier: 1.1, emoji: '🍷' },
            { name: 'Marseille', priceMultiplier: 0.9, emoji: '⚓' },
            { name: 'Nice', priceMultiplier: 1.5, emoji: '🏖️' },
        ],
        'JP': [
            { name: 'Tokyo', priceMultiplier: 2.0, emoji: '🗼' },
            { name: 'Osaka', priceMultiplier: 1.1, emoji: '🏯' },
            { name: 'Yokohama', priceMultiplier: 1.2, emoji: '🚢' },
            { name: 'Kyoto', priceMultiplier: 1.0, emoji: '⛩️' },
        ],
        'SG': [
            { name: 'Singapore', priceMultiplier: 1.0, emoji: '🦁' },
        ],
        'IN': [
            { name: 'Mumbai', priceMultiplier: 1.5, emoji: '🎬' },
            { name: 'Delhi', priceMultiplier: 1.0, emoji: '🕌' },
            { name: 'Bangalore', priceMultiplier: 1.1, emoji: '💻' },
            { name: 'Hyderabad', priceMultiplier: 0.8, emoji: '🍐' },
        ],
        'ES': [
            { name: 'Madrid', priceMultiplier: 1.4, emoji: '🐂' },
            { name: 'Barcelona', priceMultiplier: 1.5, emoji: '⛪' },
            { name: 'Valencia', priceMultiplier: 0.9, emoji: '🍊' },
            { name: 'Seville', priceMultiplier: 0.8, emoji: '💃' },
        ],
        'IT': [
            { name: 'Rome', priceMultiplier: 1.3, emoji: '🏛️' },
            { name: 'Milan', priceMultiplier: 1.6, emoji: '👗' },
            { name: 'Naples', priceMultiplier: 0.7, emoji: '🍕' },
            { name: 'Florence', priceMultiplier: 1.2, emoji: '🎨' },
        ],
        'CN': [
            { name: 'Shanghai', priceMultiplier: 2.0, emoji: '🌃' },
            { name: 'Beijing', priceMultiplier: 1.8, emoji: '🏯' },
            { name: 'Shenzhen', priceMultiplier: 1.9, emoji: '💻' },
            { name: 'Guangzhou', priceMultiplier: 1.4, emoji: '🍜' },
        ],
        'AE': [
            { name: 'Dubai', priceMultiplier: 1.4, emoji: '🏗️' },
            { name: 'Abu Dhabi', priceMultiplier: 1.2, emoji: '🛢️' },
        ],
    },
    
    // Featured properties for homepage
    featuredProperties: [
        { city: 'New York', country: 'US', countryName: 'United States', price: 850000, trend: 5.2, type: 'Apartment', beds: 2, baths: 2, sqft: 850 },
        { city: 'London', country: 'GB', countryName: 'United Kingdom', price: 750000, trend: 3.1, type: 'House', beds: 3, baths: 2, sqft: 1200 },
        { city: 'Tokyo', country: 'JP', countryName: 'Japan', price: 480000, trend: 1.8, type: 'Apartment', beds: 1, baths: 1, sqft: 450 },
        { city: 'Sydney', country: 'AU', countryName: 'Australia', price: 920000, trend: 4.5, type: 'House', beds: 4, baths: 3, sqft: 1800 },
        { city: 'Paris', country: 'FR', countryName: 'France', price: 720000, trend: 2.9, type: 'Apartment', beds: 2, baths: 1, sqft: 650 },
        { city: 'Singapore', country: 'SG', countryName: 'Singapore', price: 1200000, trend: 6.1, type: 'Condo', beds: 3, baths: 2, sqft: 1100 },
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
    if (amount >= 1000000) {
        return symbol + (amount / 1000000).toFixed(2) + 'M';
    } else if (amount >= 1000) {
        return symbol + (amount / 1000).toFixed(0) + 'k';
    }
    return symbol + amount.toLocaleString();
}

// Format full currency
function formatCurrencyFull(amount, currency) {
    const symbol = currencySymbols[currency] || currency;
    return symbol + amount.toLocaleString();
}

// Get emoji for city
function getCityEmoji(cityName, countryCode) {
    const cities = globalData.cities[countryCode] || [];
    const city = cities.find(c => c.name === cityName);
    return city?.emoji || '🏠';
}

// Populate featured properties on homepage
document.addEventListener('DOMContentLoaded', function() {
    const propertiesGrid = document.getElementById('propertiesGrid');
    if (propertiesGrid) {
        globalData.featuredProperties.forEach(prop => {
            const country = globalData.countries.find(c => c.code === prop.country);
            const currency = country ? country.currency : 'USD';
            const emoji = getCityEmoji(prop.city, prop.country);
            const trendClass = prop.trend >= 0 ? 'trend-up' : 'trend-down';
            const trendIcon = prop.trend >= 0 ? '↑' : '↓';
            
            const card = document.createElement('div');
            card.className = 'property-card';
            card.innerHTML = `
                <div class="property-image">
                    ${emoji}
                    <span class="property-badge">${prop.trend > 0 ? '+' : ''}${prop.trend}%</span>
                </div>
                <div class="property-content">
                    <div class="property-price">${formatCurrencyFull(prop.price, currency)}</div>
                    <h3 class="property-title">${prop.type} in ${prop.city}</h3>
                    <div class="property-location">${prop.countryName}</div>
                    <div class="property-features">
                        <span>🛏️ ${prop.beds}</span>
                        <span>🛁 ${prop.baths}</span>
                        <span>📐 ${prop.sqft} sqft</span>
                    </div>
                </div>
            `;
            propertiesGrid.appendChild(card);
        });
    }
    
    // Tab filtering
    const tabs = document.querySelectorAll('.tab');
    tabs.forEach(tab => {
        tab.addEventListener('click', function() {
            tabs.forEach(t => t.classList.remove('active'));
            this.classList.add('active');
            // Filter logic would go here
        });
    });
});
