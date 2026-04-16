# Data Directory

This directory contains the California Housing dataset used for training and evaluation.

## Files

- **housing.csv** - The California Housing Prices dataset from the 1990 census

## Dataset Information

**Source:** California Housing Prices dataset (1990 Census)  
**Records:** 20,640 housing blocks  
**Features:** 10 (9 predictive + 1 target)

### Features

| Feature | Type | Description |
|---------|------|-------------|
| longitude | float | A measure of how far west a house is |
| latitude | float | A measure of how far north a house is |
| housing_median_age | float | Median age of houses in the block |
| total_rooms | float | Total rooms in the block |
| total_bedrooms | float | Total bedrooms in the block |
| population | float | Population of the block |
| households | float | Number of households |
| median_income | float | Median income in $10,000s |
| ocean_proximity | categorical | Location relative to ocean |
| median_house_value | float | **Target**: Median house value in USD |

### Data Quality

- **Missing Values:** Only `total_bedrooms` has missing values (~1%)
- **Duplicates:** No duplicate records
- **Outliers:** Present in several features (handled in preprocessing)

### Usage

```python
import pandas as pd

# Load the data
df = pd.read_csv("data/housing.csv")

# Explore
print(df.shape)  # (20640, 10)
print(df.head())
```

### Citation

If you use this dataset in your research, please cite:

>Pace, R. Kelley, and Ronald Barry. "Sparse spatial autoregressions." 
>Statistics & Probability Letters 33.3 (1997): 291-297.

### License

This dataset is in the public domain.
