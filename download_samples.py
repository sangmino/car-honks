"""
Download car horn audio samples from YouTube for analysis.

Usage:
    python download_samples.py "Toyota Camry 2022"
    python download_samples.py --from-list cars.txt

Requires: yt-dlp (pip install yt-dlp)
"""

import subprocess
import argparse
import re
from pathlib import Path


def sanitize_filename(name: str) -> str:
    """Convert car name to safe filename."""
    return re.sub(r'[^\w\-]', '_', name.lower()).strip('_')


def search_and_download(query: str, output_dir: Path, max_results: int = 1) -> list[str]:
    """Search YouTube and download audio for horn sounds."""

    search_query = f"{query} horn sound test"
    output_template = str(output_dir / f"{sanitize_filename(query)}.%(ext)s")

    cmd = [
        "yt-dlp",
        f"ytsearch{max_results}:{search_query}",
        "-x",  # extract audio
        "--audio-format", "wav",
        "--audio-quality", "0",
        "-o", output_template,
        "--no-playlist",
        "--max-downloads", str(max_results),
        "--match-filter", "duration < 120",  # skip long videos
    ]

    print(f"Searching for: {search_query}")

    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"  Downloaded to {output_dir}")
            return [str(output_dir / f"{sanitize_filename(query)}.wav")]
        else:
            print(f"  Error: {result.stderr[:200]}")
            return []
    except FileNotFoundError:
        print("Error: yt-dlp not found. Install with: pip install yt-dlp")
        return []


def main():
    parser = argparse.ArgumentParser(description="Download car horn samples from YouTube")
    parser.add_argument("query", nargs="?", help="Car make/model to search for")
    parser.add_argument("--from-list", help="Text file with car names (one per line)")
    parser.add_argument("--output-dir", "-o", default="samples", help="Output directory")
    parser.add_argument("--max-results", "-n", type=int, default=1, help="Max videos per car")

    args = parser.parse_args()

    output_dir = Path(args.output_dir)
    output_dir.mkdir(exist_ok=True)

    cars = []
    if args.from_list:
        with open(args.from_list) as f:
            cars = [line.strip() for line in f if line.strip() and not line.strip().startswith('#')]
    elif args.query:
        cars = [args.query]
    else:
        # Default sample list
        cars = [
            "Toyota Camry 2022",
            "Honda Civic 2022",
            "BMW 3 Series 2022",
            "Mercedes C Class 2022",
            "Ford F-150 2022",
            "Tesla Model 3",
            "Hyundai Elantra 2022",
            "Volkswagen Golf 2022",
        ]
        print("Using default car list. Specify --from-list or a query for custom cars.\n")

    downloaded = []
    for car in cars:
        files = search_and_download(car, output_dir, args.max_results)
        downloaded.extend(files)

    print(f"\nDownloaded {len(downloaded)} samples to {output_dir}/")
    print("Run analysis with: python analyze_horn.py samples/ --batch --output horn_data.csv")


if __name__ == "__main__":
    main()
