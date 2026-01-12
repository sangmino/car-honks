"""
Analyze car horn frequency data and generate summary statistics.
"""

import pandas as pd
import numpy as np

# Load data
df = pd.read_csv('horn_data.csv')

# Remove duplicates (keep .wav versions only)
df = df[df['filename'].str.endswith('.wav')].copy()

# Parse car info from filename
df['make'] = df['filename'].str.split('_').str[0].str.title()
df['model'] = df['filename'].str.replace('.wav', '').str.split('_').str[1:-1].str.join(' ').str.title()

# Fix make names
make_map = {
    'Bmw': 'BMW',
    'Mercedes': 'Mercedes-Benz',
    'Hyundai': 'Hyundai',
    'Kia': 'Kia',
    'Honda': 'Honda',
    'Toyota': 'Toyota',
    'Ford': 'Ford',
    'Chevrolet': 'Chevrolet',
    'Nissan': 'Nissan',
    'Tesla': 'Tesla'
}
df['make'] = df['make'].map(lambda x: make_map.get(x, x))

# Country of origin
country_map = {
    'BMW': 'Germany',
    'Mercedes-Benz': 'Germany',
    'Toyota': 'Japan',
    'Honda': 'Japan',
    'Nissan': 'Japan',
    'Hyundai': 'Korea',
    'Kia': 'Korea',
    'Ford': 'USA',
    'Chevrolet': 'USA',
    'Tesla': 'USA'
}
df['country'] = df['make'].map(country_map)

# Segment classification
segment_map = {
    'civic': 'compact', 'corolla': 'compact', 'elantra': 'compact', 'sentra': 'compact', 'forte': 'compact',
    'camry': 'midsize', 'accord': 'midsize', 'sonata': 'midsize', 'altima': 'midsize', 'k5': 'midsize', 'malibu': 'midsize',
    'rav4': 'compact_suv', 'cr-v': 'compact_suv', 'tucson': 'compact_suv', 'rogue': 'compact_suv', 'sportage': 'compact_suv',
    'highlander': 'midsize_suv', 'pilot': 'midsize_suv', 'santa fe': 'midsize_suv', 'pathfinder': 'midsize_suv', 'sorento': 'midsize_suv',
    'tahoe': 'full_suv', 'telluride': 'full_suv', 'x5': 'luxury_suv', 'gle': 'luxury_suv', 'x3': 'luxury_suv',
    'f-150': 'truck', 'silverado': 'truck', 'tacoma': 'truck', 'frontier': 'truck',
    '3 series': 'luxury_sedan', '5 series': 'luxury_sedan', 'c-class': 'luxury_sedan', 'e-class': 'luxury_sedan', 'a-class': 'compact_luxury',
    'mustang': 'sports', 'corvette': 'sports', 'bronco': 'suv',
    'model 3': 'ev', 'model y': 'ev_suv', 'model s': 'ev_luxury', 'model x': 'ev_suv', 'cybertruck': 'ev_truck',
    'i4': 'ev_luxury', 'escape': 'compact_suv', 'explorer': 'midsize_suv', 'equinox': 'compact_suv', 'hr-v': 'subcompact_suv', 'kona': 'subcompact_suv'
}

def get_segment(model):
    model_lower = model.lower()
    for key, seg in segment_map.items():
        if key in model_lower:
            return seg
    return 'other'

df['segment'] = df['model'].apply(get_segment)

# Luxury indicator
df['is_luxury'] = df['make'].isin(['BMW', 'Mercedes-Benz']) | df['segment'].str.contains('luxury')

print("=" * 60)
print("CAR HORN FREQUENCY ANALYSIS")
print("=" * 60)
print(f"\nTotal samples: {len(df)}")
print(f"Unique manufacturers: {df['make'].nunique()}")

print("\n" + "=" * 60)
print("SUMMARY STATISTICS")
print("=" * 60)
print(f"\nOverall frequency range: {df['fundamental_hz'].min():.0f} - {df['fundamental_hz'].max():.0f} Hz")
print(f"Mean frequency: {df['fundamental_hz'].mean():.0f} Hz")
print(f"Median frequency: {df['fundamental_hz'].median():.0f} Hz")
print(f"Std deviation: {df['fundamental_hz'].std():.0f} Hz")

print("\n" + "=" * 60)
print("BY MANUFACTURER")
print("=" * 60)
by_make = df.groupby('make')['fundamental_hz'].agg(['mean', 'std', 'count']).round(0)
by_make = by_make.sort_values('mean')
print(by_make.to_string())

print("\n" + "=" * 60)
print("BY COUNTRY OF ORIGIN")
print("=" * 60)
by_country = df.groupby('country')['fundamental_hz'].agg(['mean', 'std', 'count']).round(0)
print(by_country.to_string())

print("\n" + "=" * 60)
print("BY SEGMENT")
print("=" * 60)
by_segment = df.groupby('segment')['fundamental_hz'].agg(['mean', 'count']).round(0).sort_values('mean')
print(by_segment.to_string())

print("\n" + "=" * 60)
print("LUXURY vs NON-LUXURY")
print("=" * 60)
by_luxury = df.groupby('is_luxury')['fundamental_hz'].agg(['mean', 'std', 'count']).round(0)
by_luxury.index = ['Mass Market', 'Luxury']
print(by_luxury.to_string())

print("\n" + "=" * 60)
print("DUAL HORN VEHICLES")
print("=" * 60)
dual = df[df['dual_horn'].notna()][['make', 'model', 'fundamental_hz', 'dual_horn']]
if len(dual) > 0:
    dual['interval_ratio'] = dual['dual_horn'] / dual['fundamental_hz']
    print(dual.to_string(index=False))
else:
    print("No dual-horn vehicles detected")

print("\n" + "=" * 60)
print("NOTABLE FINDINGS")
print("=" * 60)
lowest = df.loc[df['fundamental_hz'].idxmin()]
highest = df.loc[df['fundamental_hz'].idxmax()]
print(f"Lowest pitch: {lowest['make']} {lowest['model']} at {lowest['fundamental_hz']:.0f} Hz")
print(f"Highest pitch: {highest['make']} {highest['model']} at {highest['fundamental_hz']:.0f} Hz")

# Save cleaned data
df.to_csv('horn_data_cleaned.csv', index=False)
print(f"\nCleaned data saved to horn_data_cleaned.csv")
