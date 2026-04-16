# Realteak - Global Real Estate Price Predictor

A modern, professional real estate website for predicting property prices across 50+ countries worldwide. Built with pure HTML, CSS, and JavaScript for easy deployment on GitHub Pages.

![Realteak Design](https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?w=1200&q=80)

## Features

- **Modern Design**: Clean, professional real estate aesthetic with light blue hero section
- **Global Coverage**: 20+ countries and 95+ cities in our database
- **Price Prediction**: Client-side calculation based on property features
- **Responsive**: Works perfectly on desktop, tablet, and mobile
- **Fast Loading**: Static site with no backend required
- **Beautiful Typography**: Great Vibes script font + Inter sans-serif

## Design Highlights

- **Hero Section**: Full-width city skyline with elegant "Buy. Sell. Rent." typography
- **Search Bar**: White pill-shaped search with location, type, and price filters
- **Property Cards**: Real photos with hover effects and pricing
- **Filter Tabs**: Category filtering (All, Villa, Apartments, etc.)
- **Stats Section**: Happy families, years experience, satisfaction rate
- **Testimonials**: Client reviews with ratings
- **CTA Section**: Blue gradient call-to-action

## Pages

| Page | Description |
|------|-------------|
| `index.html` | Homepage with hero, search, properties, stats |
| `explore.html` | Browse all markets with search and filters |
| `predict.html` | Price prediction calculator |
| `countries.html` | List of all countries |
| `about.html` | About us, methodology, data sources |

## File Structure

```
├── index.html          # Homepage
├── explore.html        # Explore markets
├── predict.html        # Prediction form
├── countries.html      # Countries list
├── about.html          # About page
├── css/
│   └── style.css       # Main stylesheet
├── js/
│   ├── main.js         # Shared functions & data
│   ├── explore.js      # Explore page logic
│   ├── predict.js      # Prediction calculator
│   └── countries.js    # Countries page logic
├── .github/
│   └── workflows/
│       └── pages.yml   # GitHub Actions deployment
└── README.md           # This file
```

## Technologies Used

- **HTML5**: Semantic markup
- **CSS3**: Modern styling with CSS variables
- **JavaScript**: Vanilla JS, no frameworks
- **Google Fonts**: Great Vibes + Inter
- **Unsplash**: High-quality property images

## Deployment to GitHub Pages

### Method 1: Manual Upload

1. Go to your GitHub repository
2. Click **"Add file"** → **"Upload files"**
3. Upload all files from this folder
4. Commit changes
5. Go to **Settings** → **Pages**
6. Select **Deploy from a branch** → **main** → **/(root)**
7. Click **Save**

### Method 2: Git Commands

```bash
# Clone your repo
git clone https://github.com/YOUR_USERNAME/housing-price-prediction.git
cd housing-price-prediction

# Copy new files (replace old ones)
cp -r /path/to/global-housing-static/* .

# Push to GitHub
git add .
git commit -m "Update to Realteak design"
git push origin main
```

### Method 3: Using PowerShell Script

```powershell
# Run the deploy script
./deploy.ps1 -RepoUrl "https://github.com/YOUR_USERNAME/housing-price-prediction.git"
```

## Customization

### Change Colors

Edit `css/style.css` and modify the CSS variables:

```css
:root {
    --primary: #1a1a2e;        /* Main dark color */
    --accent: #e8b923;         /* Gold/yellow accent */
    /* ... other colors */
}
```

### Add More Countries

Edit `js/main.js` and add to the `globalData` object:

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

### Update Images

Replace Unsplash URLs in `index.html` with your own images:

```html
<img src="your-image-url.jpg" alt="Description">
```

## Data Sources

The application includes sample data for demonstration:
- Average prices per square foot by country
- City-specific multipliers based on market conditions
- Currency information for local display

## Browser Support

- Chrome (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)

## License

Open source - feel free to use and modify for your projects.

## Credits

- Design inspiration: Modern real estate websites
- Images: Unsplash
- Fonts: Google Fonts (Great Vibes, Inter)
- Icons: Emoji

---

**Live Demo**: https://tashkirrr.github.io/housing-price-prediction/

**Note**: If you're seeing the old California design, make sure you've replaced all files in the root of your repository with the new files from this folder.
