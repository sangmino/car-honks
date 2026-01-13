"""
Generate figures for the car horn blog post.
Three figures: individual distribution, country comparison, luxury gap.
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Set style - clean, publication-ready
plt.style.use('seaborn-v0_8-whitegrid')
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.size'] = 11
plt.rcParams['axes.labelsize'] = 12
plt.rcParams['axes.titlesize'] = 14
plt.rcParams['axes.spines.top'] = False
plt.rcParams['axes.spines.right'] = False

# Load data
df = pd.read_csv('horn_data_cleaned.csv')

# Sophisticated color palette (ColorBrewer-inspired)
colors = {
    'Germany': '#2171b5',    # Deep blue
    'Japan': '#cb181d',      # Deep red
    'Korea': '#238b45',      # Forest green
    'USA': '#6a51a3'         # Purple
}

make_colors = {
    # German (blues)
    'BMW': '#2171b5',
    'Mercedes-Benz': '#4292c6',
    'Audi': '#6baed6',
    'Volkswagen': '#9ecae1',
    # Japanese (reds/oranges)
    'Toyota': '#cb181d',
    'Honda': '#fb6a4a',
    'Nissan': '#ef3b2c',
    'Mazda': '#fc9272',
    'Subaru': '#fcbba1',
    'Lexus': '#fee0d2',
    # Korean (greens)
    'Hyundai': '#238b45',
    'Kia': '#41ab5d',
    # American (purples)
    'Ford': '#6a51a3',
    'Chevrolet': '#807dba',
    'Tesla': '#9e9ac8'
}

# EV indicator
ev_models = ['Model 3', 'Model Y', 'Model S', 'Model X', 'Cybertruck', 'I4',
             'Ioniq 5', 'Ioniq 6', 'EV6', 'Leaf', 'Ariya', 'Bolt', 'Mach-E',
             'iX', 'EQS', 'EQE', 'Prologue', 'Niro']

df['is_ev'] = df['model'].apply(lambda x: any(ev in str(x) for ev in ev_models) if pd.notna(x) else False)

# ============================================================
# Figure 1: Individual Vehicle Distribution (strip plot style)
# ============================================================
fig, ax = plt.subplots(figsize=(12, 7))

# Order manufacturers by mean frequency
makes_ordered = df.groupby('make')['fundamental_hz'].mean().sort_values().index.tolist()
make_to_x = {m: i for i, m in enumerate(makes_ordered)}

np.random.seed(42)  # Reproducibility
for _, row in df.iterrows():
    x = make_to_x[row['make']] + np.random.uniform(-0.25, 0.25)
    color = make_colors.get(row['make'], '#666666')
    # Larger markers, slight transparency
    ax.scatter(x, row['fundamental_hz'], color=color, alpha=0.8, s=80,
               edgecolor='white', linewidth=0.8, zorder=3)

# Add mean line for each manufacturer
for make, x_pos in make_to_x.items():
    mean_val = df[df['make'] == make]['fundamental_hz'].mean()
    ax.hlines(mean_val, x_pos - 0.35, x_pos + 0.35, color=make_colors.get(make, '#666666'),
              linewidth=2.5, alpha=0.9, zorder=2)

ax.set_xticks(range(len(makes_ordered)))
ax.set_xticklabels(makes_ordered, rotation=45, ha='right', fontsize=11)
ax.set_ylabel('Fundamental Frequency (Hz)', fontsize=12)
ax.set_xlabel('')
ax.set_title('Car Horn Frequencies by Manufacturer', fontsize=14, fontweight='bold', pad=15)

# Reference lines
ax.axhline(440, color='#999999', linestyle='--', alpha=0.7, linewidth=1.5, label='A4 (440 Hz, concert pitch)')
ax.fill_between([-0.5, len(makes_ordered)-0.5], 400, 500, alpha=0.08, color='#2171b5', zorder=1)

ax.set_xlim(-0.5, len(makes_ordered)-0.5)
ax.set_ylim(0, 850)
ax.legend(loc='upper left', framealpha=0.9)

plt.tight_layout()
plt.savefig('figures/fig1_individual.png', dpi=150, bbox_inches='tight', facecolor='white')
plt.close()

# ============================================================
# Figure 2: By Country of Origin (horizontal bar with gradient)
# ============================================================
fig, ax = plt.subplots(figsize=(10, 5))
country_stats = df.groupby('country')['fundamental_hz'].agg(['mean', 'std', 'count']).reset_index()
country_stats = country_stats.sort_values('mean')

# Create bars with error
bars = ax.barh(country_stats['country'], country_stats['mean'],
               xerr=country_stats['std'], capsize=6,
               color=[colors[c] for c in country_stats['country']],
               edgecolor='white', linewidth=1.5, height=0.6,
               error_kw={'elinewidth': 1.5, 'capthick': 1.5, 'alpha': 0.7})

ax.set_xlabel('Mean Fundamental Frequency (Hz)', fontsize=12)
ax.set_title('Horn Frequency by Country of Origin', fontsize=14, fontweight='bold', pad=15)
ax.axvline(440, color='#999999', linestyle='--', alpha=0.7, linewidth=1.5, label='A4 (440 Hz)')

# Add sample size and value annotations
for i, (_, row) in enumerate(country_stats.iterrows()):
    ax.annotate(f'{row["mean"]:.0f} Hz  (n={int(row["count"])})',
                xy=(row['mean'] + row['std'] + 15, i),
                va='center', fontsize=10, color='#444444')

ax.set_xlim(0, 700)
ax.legend(loc='lower right', framealpha=0.9)

plt.tight_layout()
plt.savefig('figures/fig2_country.png', dpi=150, bbox_inches='tight', facecolor='white')
plt.close()

# ============================================================
# Figure 3: Luxury Gap (refined bar chart)
# ============================================================
fig, ax = plt.subplots(figsize=(8, 6))
luxury_stats = df.groupby('is_luxury')['fundamental_hz'].agg(['mean', 'std', 'count']).reset_index()
luxury_stats = luxury_stats.sort_values('is_luxury', ascending=False)

labels = ['Luxury\n(BMW, Mercedes,\nAudi, Lexus)', 'Mass Market']
means = luxury_stats['mean'].values
stds = luxury_stats['std'].values
counts = luxury_stats['count'].values

bar_colors = ['#2171b5', '#969696']
x_pos = [0, 1]

bars = ax.bar(x_pos, means, yerr=stds, capsize=10,
              color=bar_colors, edgecolor='white', linewidth=2, width=0.5,
              error_kw={'elinewidth': 2, 'capthick': 2, 'alpha': 0.7})

ax.set_xticks(x_pos)
ax.set_xticklabels(labels, fontsize=12)
ax.set_ylabel('Mean Fundamental Frequency (Hz)', fontsize=12)
ax.set_title('The Luxury Gap', fontsize=14, fontweight='bold', pad=15)

# Reference line
ax.axhline(440, color='#999999', linestyle='--', alpha=0.7, linewidth=1.5)
ax.annotate('A4 (440 Hz)', xy=(1.35, 445), fontsize=10, color='#666666')

# Add values on bars
for i, (mean, count) in enumerate(zip(means, counts)):
    ax.annotate(f'{mean:.0f} Hz\n(n={count})', xy=(x_pos[i], mean + stds[i] + 15),
                ha='center', fontsize=11, fontweight='bold', color=bar_colors[i])

# Difference annotation with arrow
luxury_mean = means[0]
mass_mean = means[1]
diff = mass_mean - luxury_mean

# Draw bracket
mid_y = (luxury_mean + mass_mean) / 2
ax.annotate('', xy=(0.15, luxury_mean), xytext=(0.15, mass_mean),
            arrowprops=dict(arrowstyle='<->', color='#444444', lw=1.5))
ax.annotate(f'Δ {diff:.0f} Hz\n(~major third)', xy=(0.25, mid_y),
            fontsize=11, va='center', color='#444444',
            bbox=dict(boxstyle='round,pad=0.3', facecolor='#f0f0f0', edgecolor='none'))

ax.set_ylim(0, 650)
ax.set_xlim(-0.5, 1.8)

plt.tight_layout()
plt.savefig('figures/fig3_luxury.png', dpi=150, bbox_inches='tight', facecolor='white')
plt.close()

# ============================================================
# Figure 4: EV vs ICE comparison (if enough data)
# ============================================================
ev_count = df['is_ev'].sum()
if ev_count >= 3:
    fig, ax = plt.subplots(figsize=(8, 6))

    ev_stats = df.groupby('is_ev')['fundamental_hz'].agg(['mean', 'std', 'count']).reset_index()
    ev_stats = ev_stats.sort_values('is_ev', ascending=True)

    labels = ['Internal Combustion', 'Electric']
    means = ev_stats['mean'].values
    stds = ev_stats['std'].values
    counts = ev_stats['count'].values

    bar_colors = ['#525252', '#41ab5d']
    x_pos = [0, 1]

    bars = ax.bar(x_pos, means, yerr=stds, capsize=10,
                  color=bar_colors, edgecolor='white', linewidth=2, width=0.5,
                  error_kw={'elinewidth': 2, 'capthick': 2, 'alpha': 0.7})

    ax.set_xticks(x_pos)
    ax.set_xticklabels(labels, fontsize=12)
    ax.set_ylabel('Mean Fundamental Frequency (Hz)', fontsize=12)
    ax.set_title('Electric vs. Internal Combustion Vehicles', fontsize=14, fontweight='bold', pad=15)

    ax.axhline(440, color='#999999', linestyle='--', alpha=0.7, linewidth=1.5)

    for i, (mean, count) in enumerate(zip(means, counts)):
        ax.annotate(f'{mean:.0f} Hz\n(n={count})', xy=(x_pos[i], mean + stds[i] + 15),
                    ha='center', fontsize=11, fontweight='bold', color=bar_colors[i])

    ax.set_ylim(0, 650)
    ax.set_xlim(-0.5, 1.5)

    plt.tight_layout()
    plt.savefig('figures/fig4_ev_ice.png', dpi=150, bbox_inches='tight', facecolor='white')
    plt.close()
    print("Generated EV vs ICE figure")
else:
    print(f"Only {ev_count} EVs in dataset, skipping EV comparison figure")

print("Figures saved to figures/ directory")
print(f"Total vehicles: {len(df)}")
print(f"EVs: {ev_count}")
