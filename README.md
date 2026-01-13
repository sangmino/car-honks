# Car Horn Frequency Analysis

Analysis of car horn frequencies across 68 vehicles from 10 manufacturers. Data and code for the Better Know A Dataset blog post: "The Optimal Pitch of the Car Honk."

## Key Findings

- **German cars (BMW, Mercedes)**: 384 Hz average (lowest)
- **Japanese cars (Toyota, Honda, Nissan)**: 453 Hz average
- **Korean cars (Hyundai, Kia)**: 498 Hz average
- **American cars (Ford, Chevrolet, Tesla)**: 460 Hz average

Luxury vehicles average 384 Hz vs. 467 Hz for mass market. EVs show no systematic difference from ICE vehicles (459 Hz vs 450 Hz).

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
