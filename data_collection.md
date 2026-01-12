# Data Collection Strategy for Car Horn Frequencies

## Goal
Build a dataset of car horn frequencies by make/model to analyze patterns.

## Data Sources

### 1. YouTube Videos (Most Accessible)
Search terms:
- "[Make Model] horn sound"
- "[Make Model] honk test"
- "car horn comparison"
- "OEM horn vs aftermarket"

Examples to search:
- "Toyota Camry horn sound"
- "BMW 3 series horn"
- "Honda Civic OEM horn"

**Process:**
1. Download audio using `yt-dlp`
2. Run through `analyze_horn.py`
3. Record make/model/year + extracted frequency

### 2. Enthusiast Forums
Forums with horn discussions:
- Reddit r/cars, r/Cartalk
- Make-specific forums (Bimmerpost, Priuschat, etc.)
- People often share horn specs when upgrading

### 3. Sound Effect Libraries
- Soundsnap.com has labeled car horn samples
- Freesound.org (creative commons)
- May have make/model metadata

### 4. Field Recording (NYC)
Record at busy intersections, then:
- Use ML to classify vehicle type from video
- Match to horn audio timestamps
- More effort but captures real-world cacophony

## Data Schema

```csv
make,model,year,country,segment,horn_type,fundamental_hz,second_horn_hz,interval,source,notes
Toyota,Camry,2022,Japan,midsize_sedan,dual,420,500,minor_third,youtube_abc123,OEM horn
BMW,330i,2021,Germany,compact_luxury,dual,380,475,major_third,soundsnap_xyz,
```

## Hypotheses to Test

1. **Size hypothesis**: Larger vehicles have lower-pitched horns
   - Compare SUV/truck fundamentals vs compact cars

2. **Luxury hypothesis**: Premium brands use lower frequencies
   - BMW/Mercedes/Audi vs Toyota/Honda/Hyundai

3. **Country of origin**: Regional preferences
   - German cars vs Japanese vs American vs Korean

4. **Consonance**: Do manufacturers cluster around consonant intervals?
   - Minor thirds (1.2 ratio) vs major thirds (1.25) vs perfect fifths (1.5)

## Quick Start

```bash
# Install dependencies
pip install librosa soundfile matplotlib scipy

# Download a sample (requires yt-dlp)
yt-dlp -x --audio-format wav "https://youtube.com/watch?v=XXXXX" -o "samples/toyota_camry_2022.wav"

# Analyze
python analyze_horn.py samples/toyota_camry_2022.wav --plot

# Batch analyze
python analyze_horn.py samples/ --batch --output horn_data.csv
```

## Sample Size Target

- Minimum: 30 vehicles across different segments
- Ideal: 100+ vehicles for robust statistics
- Priority segments:
  - Compact (Civic, Corolla, Golf)
  - Midsize sedan (Camry, Accord, 3 Series)
  - Luxury sedan (S-Class, 7 Series, A8)
  - SUV (RAV4, CR-V, X5)
  - Pickup (F-150, Silverado, Tundra)
  - Economy (Fit, Yaris, Spark)
