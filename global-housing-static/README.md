# Global Housing Predictor

A multi-page static website for predicting property prices across 20+ countries worldwide. Built with vanilla HTML, CSS, and JavaScript for easy deployment on GitHub Pages.

## Features

- **20+ Countries**: Coverage across North America, Europe, Asia, and more
- **95+ Cities**: Major metropolitan areas with local price multipliers
- **Price Prediction**: Client-side calculation based on property features
- **Search & Explore**: Find cities and compare markets
- **Responsive Design**: Works on desktop, tablet, and mobile
- **No Backend Required**: All data embedded in JavaScript

## Pages

| Page | Description |
|------|-------------|
| `index.html` | Homepage with featured markets and stats |
| `explore.html` | Search and browse all cities |
| `predict.html` | Price prediction calculator |
| `countries.html` | List of all countries in database |
| `about.html` | Methodology and data sources |

## How to Deploy on GitHub Pages

1. **Create a new repository** on GitHub
2. **Upload these files** to the repository
3. **Go to Settings** → Pages
4. **Select source**: Deploy from a branch
5. **Select branch**: main / (root)
6. **Save** and wait for deployment

Your site will be available at: `https://yourusername.github.io/repository-name/`

## File Structure

```
├── index.html          # Homepage
├── explore.html        # Search page
├── predict.html        # Prediction form
├── countries.html      # Countries list
├── about.html          # About page
├── css/
│   └── style.css       # Stylesheet
├── js/
│   ├── main.js         # Shared functions & data
│   ├── explore.js      # Explore page logic
│   ├── predict.js      # Prediction calculator
│   └── countries.js    # Countries page logic
└── .github/
    └── workflows/
        └── pages.yml   # GitHub Actions deployment
```

## Data Sources

The application includes sample data for demonstration purposes:
- Average prices per square foot by country
- City-specific multipliers based on market conditions
- Currency information for local display

## Customization

To add more countries or cities, edit the `globalData` object in `js/main.js`:

```javascript
countries: [
    { code: 'XX', name: 'New Country', currency: 'XXX', avgPricePerSqft: 100 },
    // ...
],

cities: {
    'XX': [
        { name: 'City Name', priceMultiplier: 1.5 },
        // ...
    ],
}
```

## License

Open source - feel free to use and modify.
