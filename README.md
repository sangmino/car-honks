# Car Horn Frequency Analysis

Analysis of car horn frequencies across 157 vehicles from 15 manufacturers. Data and code for the Better Know A Dataset blog post: "The Optimal Pitch of the Car Honk."

## Key Findings

- **German cars (BMW, Mercedes, Audi, VW)**: 412 Hz average (lowest)
- **American cars (Ford, Chevrolet, Tesla)**: 440 Hz average
- **Japanese cars (Toyota, Honda, Nissan, Mazda, Subaru, Lexus)**: 449 Hz average
- **Korean cars (Hyundai, Kia)**: 466 Hz average (highest)

Luxury vehicles average 426 Hz vs. 445 Hz for mass market (20 Hz gap). EVs average 387 Hz vs 448 Hz for ICE (61 Hz gap), suggesting EVs have lower-pitched horns.

## Files

- `draft.md` - Blog post
- `horn_data_cleaned.csv` - Cleaned dataset with frequencies by make/model
- `analyze_horn.py` - Spectral analysis script
- `make_figures.py` - Generate figures
- `figures/` - PNG figures for the blog post

## Usage

```bash
# Install dependencies
pip install librosa soundfile matplotlib pandas scipy

# Analyze a single audio file
python analyze_horn.py path/to/horn.wav --plot

# Batch analyze
python analyze_horn.py samples/ --batch --output results.csv

# Generate figures
python make_figures.py
```

## Data Collection

Audio samples collected from YouTube horn test videos. Frequencies extracted via FFT using librosa.

## License

MIT
