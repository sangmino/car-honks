"""
Car Horn Frequency Analyzer
Extracts fundamental frequency and harmonics from car horn audio samples.

Usage:
    python analyze_horn.py <audio_file>
    python analyze_horn.py --batch <directory>
"""

import numpy as np
import argparse
from pathlib import Path

# Check for required packages
try:
    import librosa
    import librosa.display
except ImportError:
    print("Install required packages: pip install librosa soundfile")
    exit(1)

try:
    import matplotlib.pyplot as plt
except ImportError:
    plt = None
    print("Warning: matplotlib not installed, plotting disabled")


def load_audio(filepath: str, sr: int = 22050) -> tuple[np.ndarray, int]:
    """Load audio file and return samples + sample rate."""
    y, sr = librosa.load(filepath, sr=sr)
    return y, sr


def find_horn_segment(y: np.ndarray, sr: int, threshold_db: float = -20) -> tuple[int, int]:
    """Find the loudest segment (likely the horn) in the audio."""
    # Compute RMS energy
    rms = librosa.feature.rms(y=y)[0]
    rms_db = librosa.amplitude_to_db(rms)

    # Find segments above threshold
    above_threshold = rms_db > threshold_db

    if not above_threshold.any():
        # Use whole signal if nothing above threshold
        return 0, len(y)

    # Find start and end of loudest continuous segment
    starts = np.where(np.diff(above_threshold.astype(int)) == 1)[0]
    ends = np.where(np.diff(above_threshold.astype(int)) == -1)[0]

    if len(starts) == 0:
        starts = np.array([0])
    if len(ends) == 0:
        ends = np.array([len(rms) - 1])
    if ends[0] < starts[0]:
        starts = np.insert(starts, 0, 0)
    if starts[-1] > ends[-1]:
        ends = np.append(ends, len(rms) - 1)

    # Convert frame indices to samples
    hop_length = 512  # librosa default
    start_sample = starts[0] * hop_length
    end_sample = ends[0] * hop_length

    return int(start_sample), int(end_sample)


def extract_frequencies(y: np.ndarray, sr: int, n_fft: int = 4096) -> dict:
    """Extract fundamental frequency and harmonics from audio segment."""

    # Compute spectrogram
    D = np.abs(librosa.stft(y, n_fft=n_fft))
    freqs = librosa.fft_frequencies(sr=sr, n_fft=n_fft)

    # Average spectrum across time
    avg_spectrum = np.mean(D, axis=1)

    # Find peaks (potential fundamental and harmonics)
    from scipy.signal import find_peaks

    # Normalize spectrum
    avg_spectrum_db = librosa.amplitude_to_db(avg_spectrum)

    # Find peaks at least 10dB above local noise floor
    peaks, properties = find_peaks(avg_spectrum_db, height=-40, distance=20, prominence=10)

    if len(peaks) == 0:
        return {"error": "No clear peaks found"}

    # Get frequencies and amplitudes of peaks
    peak_freqs = freqs[peaks]
    peak_amps = avg_spectrum_db[peaks]

    # Sort by amplitude (loudest first)
    sort_idx = np.argsort(peak_amps)[::-1]
    peak_freqs = peak_freqs[sort_idx]
    peak_amps = peak_amps[sort_idx]

    # Filter to car horn frequency range (200-800 Hz for fundamentals)
    horn_mask = (peak_freqs >= 200) & (peak_freqs <= 800)
    horn_freqs = peak_freqs[horn_mask]
    horn_amps = peak_amps[horn_mask]

    # Estimate fundamental (lowest strong peak in horn range)
    if len(horn_freqs) > 0:
        fundamental = horn_freqs[np.argmax(horn_amps)]
    else:
        fundamental = peak_freqs[0]  # fallback to loudest peak

    # Find harmonics
    harmonics = []
    for f in peak_freqs:
        ratio = f / fundamental
        if 1.8 < ratio < 6.2 and abs(ratio - round(ratio)) < 0.1:
            harmonics.append((f, round(ratio)))

    # Check for dual-horn (two fundamentals)
    dual_horn = None
    for f in horn_freqs:
        if f != fundamental:
            # Check if it's a musical interval from fundamental
            ratio = f / fundamental if f > fundamental else fundamental / f
            if 1.15 < ratio < 1.35:  # minor or major third
                interval = "minor third" if ratio < 1.28 else "major third"
                dual_horn = {"frequency": f, "interval": interval, "ratio": ratio}
                break

    return {
        "fundamental_hz": float(fundamental),
        "fundamental_note": freq_to_note(fundamental),
        "dual_horn": dual_horn,
        "harmonics": harmonics,
        "all_peaks_hz": peak_freqs[:10].tolist(),
        "peak_amplitudes_db": peak_amps[:10].tolist()
    }


def freq_to_note(freq: float) -> str:
    """Convert frequency to musical note name."""
    if freq <= 0:
        return "N/A"

    notes = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']

    # A4 = 440 Hz
    semitones_from_a4 = 12 * np.log2(freq / 440)
    semitone_idx = int(round(semitones_from_a4)) + 9  # A is 9 semitones from C

    note = notes[semitone_idx % 12]
    octave = 4 + (semitone_idx + 3) // 12

    cents_off = int((semitones_from_a4 - round(semitones_from_a4)) * 100)

    return f"{note}{octave} ({cents_off:+d} cents)"


def plot_spectrum(y: np.ndarray, sr: int, results: dict, save_path: str = None):
    """Plot the frequency spectrum with annotated peaks."""
    if plt is None:
        return

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8))

    # Waveform
    times = np.arange(len(y)) / sr
    ax1.plot(times, y, linewidth=0.5)
    ax1.set_xlabel("Time (s)")
    ax1.set_ylabel("Amplitude")
    ax1.set_title("Waveform")

    # Spectrum
    D = np.abs(librosa.stft(y, n_fft=4096))
    freqs = librosa.fft_frequencies(sr=sr, n_fft=4096)
    avg_spectrum = np.mean(D, axis=1)
    avg_spectrum_db = librosa.amplitude_to_db(avg_spectrum)

    ax2.plot(freqs, avg_spectrum_db)
    ax2.set_xlim(0, 2000)
    ax2.set_xlabel("Frequency (Hz)")
    ax2.set_ylabel("Amplitude (dB)")
    ax2.set_title("Frequency Spectrum")

    # Annotate fundamental
    if "fundamental_hz" in results:
        f0 = results["fundamental_hz"]
        ax2.axvline(f0, color='r', linestyle='--', label=f'Fundamental: {f0:.0f} Hz')

        if results.get("dual_horn"):
            f1 = results["dual_horn"]["frequency"]
            ax2.axvline(f1, color='g', linestyle='--',
                       label=f'Second horn: {f1:.0f} Hz ({results["dual_horn"]["interval"]})')

    ax2.legend()

    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=150)
        print(f"Saved plot to {save_path}")
    else:
        plt.show()


def analyze_file(filepath: str, plot: bool = False) -> dict:
    """Analyze a single audio file."""
    print(f"\nAnalyzing: {filepath}")

    y, sr = load_audio(filepath)

    # Find horn segment
    start, end = find_horn_segment(y, sr)
    y_horn = y[start:end]

    print(f"  Audio length: {len(y)/sr:.2f}s, Horn segment: {(end-start)/sr:.2f}s")

    # Extract frequencies
    results = extract_frequencies(y_horn, sr)

    if "error" in results:
        print(f"  Error: {results['error']}")
        return results

    print(f"  Fundamental: {results['fundamental_hz']:.1f} Hz ({results['fundamental_note']})")

    if results.get("dual_horn"):
        dh = results["dual_horn"]
        print(f"  Dual horn: {dh['frequency']:.1f} Hz ({dh['interval']}, ratio {dh['ratio']:.3f})")

    if plot:
        plot_path = Path(filepath).with_suffix('.png')
        plot_spectrum(y_horn, sr, results, str(plot_path))

    return results


def main():
    parser = argparse.ArgumentParser(description="Analyze car horn frequencies")
    parser.add_argument("input", help="Audio file or directory (with --batch)")
    parser.add_argument("--batch", action="store_true", help="Process all audio files in directory")
    parser.add_argument("--plot", action="store_true", help="Generate spectrum plots")
    parser.add_argument("--output", "-o", help="Output CSV file for batch results")

    args = parser.parse_args()

    if args.batch:
        input_dir = Path(args.input)
        audio_files = list(input_dir.glob("*.wav")) + list(input_dir.glob("*.mp3")) + \
                      list(input_dir.glob("*.m4a")) + list(input_dir.glob("*.flac")) + \
                      list(input_dir.glob("*.webm")) + list(input_dir.glob("*.opus"))

        results = []
        for f in audio_files:
            r = analyze_file(str(f), plot=args.plot)
            r["filename"] = f.name
            results.append(r)

        if args.output:
            import csv
            with open(args.output, 'w', newline='') as csvfile:
                writer = csv.DictWriter(csvfile,
                    fieldnames=["filename", "fundamental_hz", "fundamental_note", "dual_horn"])
                writer.writeheader()
                for r in results:
                    writer.writerow({
                        "filename": r.get("filename", ""),
                        "fundamental_hz": r.get("fundamental_hz", ""),
                        "fundamental_note": r.get("fundamental_note", ""),
                        "dual_horn": r.get("dual_horn", {}).get("frequency", "") if r.get("dual_horn") else ""
                    })
            print(f"\nResults saved to {args.output}")
    else:
        analyze_file(args.input, plot=args.plot)


if __name__ == "__main__":
    main()
