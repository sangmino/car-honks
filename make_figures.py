"""
Generate figures for the car horn blog post.
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Set style
plt.style.use('seaborn-v0_8-whitegrid')
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.size'] = 11
plt.rcParams['axes.labelsize'] = 12
plt.rcParams['axes.titlesize'] = 13

# Load data
df = pd.read_csv('horn_data_cleaned.csv')

# Colors
colors = {
    'Germany': '#1f77b4',
    'Japan': '#ff7f0e',
    'Korea': '#2ca02c',
    'USA': '#d62728'
}

make_colors = {
    'BMW': '#1f77b4',
    'Mercedes-Benz': '#1f77b4',
    'Toyota': '#ff7f0e',
    'Honda': '#ff7f0e',
    'Nissan': '#ff7f0e',
    'Hyundai': '#2ca02c',
    'Kia': '#2ca02c',
    'Ford': '#d62728',
    'Chevrolet': '#d62728',
    'Tesla': '#d62728'
}

# Figure 1: By Country
fig, ax = plt.subplots(figsize=(8, 5))
country_stats = df.groupby('country')['fundamental_hz'].agg(['mean', 'std', 'count']).reset_index()
country_stats = country_stats.sort_values('mean')

bars = ax.barh(country_stats['country'], country_stats['mean'],
               xerr=country_stats['std'], capsize=5,
               color=[colors[c] for c in country_stats['country']])
ax.set_xlabel('Mean Fundamental Frequency (Hz)')
ax.set_title('Car Horn Frequency by Country of Origin')
ax.axvline(440, color='gray', linestyle='--', alpha=0.5, label='A4 (440 Hz)')

# Add sample size annotations
for i, (_, row) in enumerate(country_stats.iterrows()):
    ax.annotate(f'n={int(row["count"])}', xy=(row['mean'] + row['std'] + 20, i),
                va='center', fontsize=9, color='gray')

ax.legend()
plt.tight_layout()
plt.savefig('figures/fig1_by_country.png', dpi=150)
plt.close()

# Figure 2: By Manufacturer (horizontal bar)
fig, ax = plt.subplots(figsize=(9, 6))
make_stats = df.groupby('make')['fundamental_hz'].agg(['mean', 'std', 'count']).reset_index()
make_stats = make_stats.sort_values('mean')

bar_colors = [make_colors.get(m, 'gray') for m in make_stats['make']]
bars = ax.barh(make_stats['make'], make_stats['mean'],
               xerr=make_stats['std'], capsize=4,
               color=bar_colors, alpha=0.8)
ax.set_xlabel('Mean Fundamental Frequency (Hz)')
ax.set_title('Car Horn Frequency by Manufacturer')
ax.axvline(440, color='gray', linestyle='--', alpha=0.5, label='A4 (440 Hz)')

# Add country legend
from matplotlib.patches import Patch
legend_elements = [Patch(facecolor=colors['Germany'], label='Germany'),
                   Patch(facecolor=colors['Japan'], label='Japan'),
                   Patch(facecolor=colors['Korea'], label='Korea'),
                   Patch(facecolor=colors['USA'], label='USA')]
ax.legend(handles=legend_elements, loc='lower right')

plt.tight_layout()
plt.savefig('figures/fig2_by_manufacturer.png', dpi=150)
plt.close()

# Figure 3: Luxury vs Mass Market
fig, ax = plt.subplots(figsize=(7, 5))
luxury_stats = df.groupby('is_luxury')['fundamental_hz'].agg(['mean', 'std', 'count']).reset_index()
luxury_stats['label'] = luxury_stats['is_luxury'].map({True: 'Luxury\n(BMW, Mercedes)', False: 'Mass Market'})

bars = ax.bar(luxury_stats['label'], luxury_stats['mean'],
              yerr=luxury_stats['std'], capsize=8,
              color=['#4a90d9', '#7f7f7f'], width=0.6)
ax.set_ylabel('Mean Fundamental Frequency (Hz)')
ax.set_title('The Luxury Gap: Horn Frequency by Market Segment')
ax.axhline(440, color='gray', linestyle='--', alpha=0.5)
ax.annotate('A4 (440 Hz)', xy=(1.5, 445), fontsize=9, color='gray')

# Add difference annotation
luxury_mean = luxury_stats[luxury_stats['is_luxury'] == True]['mean'].values[0]
mass_mean = luxury_stats[luxury_stats['is_luxury'] == False]['mean'].values[0]
diff = mass_mean - luxury_mean
ax.annotate(f'Δ = {diff:.0f} Hz\n(~major third)',
            xy=(0.5, (luxury_mean + mass_mean)/2),
            fontsize=10, ha='center',
            bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

plt.tight_layout()
plt.savefig('figures/fig3_luxury_gap.png', dpi=150)
plt.close()

# Figure 4: Distribution with individual points
fig, ax = plt.subplots(figsize=(10, 6))

# Jitter plot by manufacturer
makes_ordered = df.groupby('make')['fundamental_hz'].mean().sort_values().index.tolist()
make_to_x = {m: i for i, m in enumerate(makes_ordered)}

for _, row in df.iterrows():
    x = make_to_x[row['make']] + np.random.uniform(-0.15, 0.15)
    color = make_colors.get(row['make'], 'gray')
    ax.scatter(x, row['fundamental_hz'], color=color, alpha=0.7, s=60, edgecolor='white', linewidth=0.5)

ax.set_xticks(range(len(makes_ordered)))
ax.set_xticklabels(makes_ordered, rotation=45, ha='right')
ax.set_ylabel('Fundamental Frequency (Hz)')
ax.set_title('Individual Vehicle Horn Frequencies')
ax.axhline(440, color='gray', linestyle='--', alpha=0.5, label='A4 (440 Hz)')

# Highlight range
ax.fill_between([-0.5, len(makes_ordered)-0.5], 400, 500, alpha=0.1, color='blue', label='Common range (400-500 Hz)')
ax.set_xlim(-0.5, len(makes_ordered)-0.5)
ax.legend(loc='upper left')

plt.tight_layout()
plt.savefig('figures/fig4_distribution.png', dpi=150)
plt.close()

# Figure 5: New manufacturer decision framework
fig, ax = plt.subplots(figsize=(9, 6))

# Show distribution of existing frequencies
ax.hist(df['fundamental_hz'], bins=15, alpha=0.6, color='gray', edgecolor='black', label='Current distribution')
ax.axvline(df['fundamental_hz'].median(), color='black', linestyle='-', linewidth=2, label=f'Median: {df["fundamental_hz"].median():.0f} Hz')

# Annotate strategic options
strategies = [
    (350, 'Go Low\n(BMW strategy)', 'blue'),
    (450, 'Join Cluster\n(blend in)', 'green'),
    (650, 'Go High\n(stand out)', 'red'),
]

for freq, label, color in strategies:
    ax.axvline(freq, color=color, linestyle='--', linewidth=2, alpha=0.7)
    ax.annotate(label, xy=(freq, ax.get_ylim()[1]*0.85),
                fontsize=10, ha='center', color=color,
                bbox=dict(boxstyle='round', facecolor='white', edgecolor=color, alpha=0.8))

ax.set_xlabel('Fundamental Frequency (Hz)')
ax.set_ylabel('Number of Vehicles')
ax.set_title('Strategic Positioning for a New Car Manufacturer')
ax.legend(loc='upper right')

plt.tight_layout()
plt.savefig('figures/fig5_strategy.png', dpi=150)
plt.close()

print("Figures saved to figures/ directory")
