"""
Consonance/Dissonance Analysis for Car Horn Frequencies

Uses the Sethares-Plomp-Levelt dissonance model to analyze what happens
when multiple cars honk simultaneously at an intersection.

Based on: Sethares, W. A. (1998). Tuning, Timbre, Spectrum, Scale.
"""

import numpy as np
import pandas as pd
from itertools import combinations
import matplotlib.pyplot as plt


def sethares_dissonance(f1, f2):
    """
    Compute dissonance between two pure tones using the Sethares
    parameterization of the Plomp-Levelt roughness curve.

    The model captures how our cochlea perceives "roughness" when two
    frequencies are close but not identical. Maximum roughness occurs
    when tones are ~25% of a critical bandwidth apart.

    Parameters:
        f1, f2: Frequencies in Hz

    Returns:
        Dissonance score (higher = more dissonant)
    """
    # Ensure f1 <= f2
    if f1 > f2:
        f1, f2 = f2, f1

    # Sethares model parameters
    Dstar = 0.24  # Critical bandwidth scaling
    S1, S2 = 0.0207, 18.96  # Critical bandwidth coefficients
    A1, A2 = -3.51, -5.75  # Exponential decay rates
    C1, C2 = 5.0, -5.0  # Amplitude coefficients

    # Scale by critical bandwidth at the lower frequency
    s = Dstar / (S1 * f1 + S2)
    SFdif = s * (f2 - f1)

    # Plomp-Levelt roughness curve (sum of two exponentials)
    d = C1 * np.exp(A1 * SFdif) + C2 * np.exp(A2 * SFdif)

    return max(0, d)  # Dissonance can't be negative


def chord_dissonance(frequencies):
    """
    Compute total dissonance of a chord by summing pairwise dissonance.

    Parameters:
        frequencies: List of frequencies in Hz

    Returns:
        Total dissonance score
    """
    return sum(sethares_dissonance(f1, f2)
               for f1, f2 in combinations(frequencies, 2))


def monte_carlo_analysis(frequencies, n_samples=10000, seed=42):
    """
    Sample random 3-car combinations and compute dissonance distribution.

    Parameters:
        frequencies: Array of horn frequencies
        n_samples: Number of random trios to sample
        seed: Random seed for reproducibility

    Returns:
        Array of dissonance scores
    """
    np.random.seed(seed)
    results = []

    for _ in range(n_samples):
        trio = np.random.choice(frequencies, 3, replace=False)
        d = chord_dissonance(trio)
        results.append(d)

    return np.array(results)


def find_worst_pairings(df, n_worst=10):
    """
    Find the manufacturer pairings that produce the most dissonance.

    Returns:
        DataFrame with worst pairings
    """
    # Get mean frequency per manufacturer
    make_means = df.groupby('make')['fundamental_hz'].mean()

    results = []
    for (m1, f1), (m2, f2) in combinations(make_means.items(), 2):
        d = sethares_dissonance(f1, f2)
        results.append({
            'make1': m1,
            'make2': m2,
            'freq1': f1,
            'freq2': f2,
            'diff': abs(f2 - f1),
            'dissonance': d
        })

    return pd.DataFrame(results).sort_values('dissonance', ascending=False).head(n_worst)


def compute_benchmarks():
    """
    Compute dissonance for reference musical chords.
    All based on A4 = 440 Hz using just intonation ratios.
    """
    # Just intonation ratios
    major_third = 5/4  # 1.25
    minor_third = 6/5  # 1.2
    perfect_fifth = 3/2  # 1.5
    tritone = 45/32  # ~1.406 (diminished fifth)

    base = 440  # A4

    benchmarks = {
        'Major triad (A-C#-E)': chord_dissonance([base, base * major_third, base * perfect_fifth]),
        'Minor triad (A-C-E)': chord_dissonance([base, base * minor_third, base * perfect_fifth]),
        'Diminished (A-C-Eb)': chord_dissonance([base, base * minor_third, base * tritone]),
        'Semitone cluster': chord_dissonance([440, 466, 494]),  # A-Bb-B (worst case)
        'Octave spread': chord_dissonance([220, 440, 660]),  # Well-spaced
    }

    return benchmarks


def generate_figure(dissonance_scores, benchmarks, output_path='figures/fig5_dissonance_monte_carlo.png'):
    """
    Generate histogram of dissonance scores with benchmark lines.
    """
    plt.style.use('seaborn-v0_8-whitegrid')
    fig, ax = plt.subplots(figsize=(10, 6))

    # Histogram
    ax.hist(dissonance_scores, bins=50, color='#6a51a3', alpha=0.7, edgecolor='white')

    # Benchmark lines
    colors = {
        'Major triad (A-C#-E)': '#238b45',
        'Minor triad (A-C-E)': '#41ab5d',
        'Diminished (A-C-Eb)': '#fd8d3c',
        'Semitone cluster': '#cb181d',
    }

    for name, value in benchmarks.items():
        if name in colors:
            ax.axvline(value, color=colors[name], linestyle='--', linewidth=2,
                      label=f'{name}: {value:.2f}')

    ax.set_xlabel('Dissonance Score (Sethares-Plomp-Levelt)', fontsize=12)
    ax.set_ylabel('Count (out of 10,000 random trios)', fontsize=12)
    ax.set_title('What Happens When Three Random Cars Honk Together?',
                fontsize=14, fontweight='bold')
    ax.legend(loc='upper right', fontsize=10)

    # Add median line
    median = np.median(dissonance_scores)
    ax.axvline(median, color='#2171b5', linestyle='-', linewidth=2.5,
              label=f'Median: {median:.2f}')

    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches='tight', facecolor='white')
    plt.close()

    return output_path


def main():
    """Run the full consonance analysis."""

    # Load data
    df = pd.read_csv('horn_data_cleaned.csv')
    frequencies = df['fundamental_hz'].values

    print("=" * 60)
    print("CONSONANCE ANALYSIS: Car Horn Frequencies")
    print("=" * 60)
    print(f"\nDataset: {len(df)} vehicles from {df['make'].nunique()} manufacturers")
    print(f"Frequency range: {frequencies.min():.0f} - {frequencies.max():.0f} Hz")

    # Compute benchmarks
    print("\n" + "-" * 40)
    print("REFERENCE BENCHMARKS (Musical Chords)")
    print("-" * 40)
    benchmarks = compute_benchmarks()
    for name, value in benchmarks.items():
        print(f"  {name}: {value:.3f}")

    # Monte Carlo simulation
    print("\n" + "-" * 40)
    print("MONTE CARLO SIMULATION (10,000 random 3-car combinations)")
    print("-" * 40)

    dissonance_scores = monte_carlo_analysis(frequencies, n_samples=10000)

    # Statistics
    median = np.median(dissonance_scores)
    mean = np.mean(dissonance_scores)
    std = np.std(dissonance_scores)

    major_threshold = benchmarks['Major triad (A-C#-E)']
    minor_threshold = benchmarks['Minor triad (A-C-E)']
    diminished_threshold = benchmarks['Diminished (A-C-Eb)']
    semitone_threshold = benchmarks['Semitone cluster']

    pct_consonant = (dissonance_scores <= major_threshold).mean() * 100
    pct_minor = ((dissonance_scores > major_threshold) & (dissonance_scores <= minor_threshold)).mean() * 100
    pct_moderate = ((dissonance_scores > minor_threshold) & (dissonance_scores <= diminished_threshold)).mean() * 100
    pct_dissonant = (dissonance_scores > diminished_threshold).mean() * 100
    pct_terrible = (dissonance_scores > semitone_threshold).mean() * 100

    print(f"\n  Mean dissonance: {mean:.3f}")
    print(f"  Median dissonance: {median:.3f}")
    print(f"  Std deviation: {std:.3f}")
    print(f"\n  Distribution:")
    print(f"    Consonant (≤ major triad): {pct_consonant:.1f}%")
    print(f"    Mild (major to minor triad): {pct_minor:.1f}%")
    print(f"    Moderate (minor to diminished): {pct_moderate:.1f}%")
    print(f"    Dissonant (> diminished): {pct_dissonant:.1f}%")
    print(f"    Terrible (> semitone cluster): {pct_terrible:.1f}%")

    # Worst pairings
    print("\n" + "-" * 40)
    print("WORST MANUFACTURER PAIRINGS (by mean frequency)")
    print("-" * 40)
    worst = find_worst_pairings(df)
    for _, row in worst.head(5).iterrows():
        print(f"  {row['make1']} ({row['freq1']:.0f} Hz) + {row['make2']} ({row['freq2']:.0f} Hz)")
        print(f"    Difference: {row['diff']:.0f} Hz, Dissonance: {row['dissonance']:.3f}")

    # Best pairings (most consonant)
    print("\n" + "-" * 40)
    print("BEST MANUFACTURER PAIRINGS (most consonant)")
    print("-" * 40)
    best = find_worst_pairings(df, n_worst=100).sort_values('dissonance').head(5)
    for _, row in best.iterrows():
        print(f"  {row['make1']} ({row['freq1']:.0f} Hz) + {row['make2']} ({row['freq2']:.0f} Hz)")
        print(f"    Difference: {row['diff']:.0f} Hz, Dissonance: {row['dissonance']:.3f}")

    # Generate figure
    print("\n" + "-" * 40)
    print("GENERATING FIGURE")
    print("-" * 40)
    output_path = generate_figure(dissonance_scores, benchmarks)
    print(f"  Saved to: {output_path}")

    # Summary for blog
    print("\n" + "=" * 60)
    print("SUMMARY FOR BLOG POST")
    print("=" * 60)
    print(f"""
When three random cars from our dataset honk simultaneously:

- Only {pct_consonant:.0f}% of combinations sound as consonant as a major chord
- {pct_dissonant:.0f}% sound worse than a diminished chord (notably dissonant)
- {pct_terrible:.0f}% approach the dissonance of a semitone cluster (painful)

The median intersection ({median:.2f}) falls between a minor triad ({minor_threshold:.2f})
and a diminished chord ({diminished_threshold:.2f}) - not terrible, but not pleasant either.

Worst pairing: {worst.iloc[0]['make1']} + {worst.iloc[0]['make2']}
  ({worst.iloc[0]['diff']:.0f} Hz apart, dissonance = {worst.iloc[0]['dissonance']:.2f})
""")

    return {
        'dissonance_scores': dissonance_scores,
        'benchmarks': benchmarks,
        'worst_pairings': worst,
        'pct_consonant': pct_consonant,
        'pct_dissonant': pct_dissonant,
        'median': median
    }


if __name__ == '__main__':
    results = main()
